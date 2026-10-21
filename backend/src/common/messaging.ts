import { Injectable, Logger, OnApplicationBootstrap, OnModuleDestroy } from '@nestjs/common';
import { Kafka, Producer, Consumer, logLevel } from 'kafkajs';
import { Database } from './database.js';
import { WorkerHealth } from './health.js';
import { required, serviceName } from './config.js';
import { NotificationsService } from '../notifications/notifications.service.js';
export const INQUIRY_TOPIC = 'inquiry.created.v1';
const pause = (ms: number) =>
  new Promise<void>((resolve) => {
    setTimeout(resolve, ms).unref();
  });

@Injectable()
export class OutboxPublisher implements OnApplicationBootstrap, OnModuleDestroy {
  private readonly logger = new Logger('OutboxPublisher');
  private producer?: Producer;
  private stopping = false;
  constructor(
    private readonly db: Database,
    private readonly health: WorkerHealth,
  ) {}
  onApplicationBootstrap(): void {
    void this.run();
  }
  async publishBatch(): Promise<void> {
    await this.db.transaction(async (client) => {
      const pending = await client.query(
        'SELECT event_id,inquiry_id,payload FROM outbox WHERE published_at IS NULL ORDER BY created_at LIMIT 25 FOR UPDATE SKIP LOCKED',
      );
      for (const event of pending.rows) {
        await this.producer!.send({
          topic: process.env.KAFKA_TOPIC ?? INQUIRY_TOPIC,
          acks: -1,
          messages: [{ key: event.inquiry_id, value: JSON.stringify(event.payload) }],
        });
        await client.query('UPDATE outbox SET published_at=now() WHERE event_id=$1', [
          event.event_id,
        ]);
      }
    });
  }
  private async run(): Promise<void> {
    while (!this.stopping) {
      try {
        this.producer = kafka().producer({ allowAutoTopicCreation: true });
        await this.producer.connect();
        while (!this.stopping) {
          await this.publishBatch();
          this.health.ready = true;
          await pause(500);
        }
      } catch (error) {
        this.health.ready = false;
        this.logger.error(
          `Outbox retry: ${error instanceof Error ? error.message : String(error)}`,
        );
      } finally {
        await this.producer?.disconnect().catch(() => undefined);
      }
      if (!this.stopping) await pause(2000);
    }
  }
  async onModuleDestroy(): Promise<void> {
    this.stopping = true;
    this.health.ready = false;
    await this.producer?.disconnect();
  }
}

@Injectable()
export class InquiryConsumer implements OnApplicationBootstrap, OnModuleDestroy {
  private readonly logger = new Logger('InquiryConsumer');
  private consumer?: Consumer;
  private stopping = false;
  constructor(
    private readonly notifications: NotificationsService,
    private readonly health: WorkerHealth,
  ) {}
  onApplicationBootstrap(): void {
    void this.run();
  }
  private async run(): Promise<void> {
    while (!this.stopping) {
      try {
        this.consumer = kafka().consumer({
          groupId: 'marketplace-notifications-v1',
          allowAutoTopicCreation: true,
          retry: { retries: 5 },
        });
        this.consumer.on(this.consumer.events.CRASH, (event) => {
          this.health.ready = false;
          this.logger.error(`Consumer crash: ${event.payload.error.message}`);
        });
        this.consumer.on(this.consumer.events.GROUP_JOIN, () => {
          this.health.ready = true;
        });
        this.consumer.on(this.consumer.events.DISCONNECT, () => {
          this.health.ready = false;
        });
        await this.consumer.connect();
        await this.consumer.subscribe({
          topic: process.env.KAFKA_TOPIC ?? INQUIRY_TOPIC,
          fromBeginning: true,
        });
        await this.consumer.run({
          eachMessage: async ({ message }) => {
            if (!message.value)
              throw new Error('Event payload missing; offset is not acknowledged');
            // Await durable insert before KafkaJS acknowledges the offset. Replays are deduplicated in SQL.
            await this.notifications.consume(JSON.parse(message.value.toString('utf8')));
          },
        });
        // KafkaJS runs processing in the background; retain the connection until shutdown.
        while (!this.stopping) await pause(1000);
      } catch (error) {
        this.health.ready = false;
        this.logger.error(
          `Consumer retry: ${error instanceof Error ? error.message : String(error)}`,
        );
      } finally {
        await this.consumer?.disconnect().catch(() => undefined);
      }
      if (!this.stopping) await pause(2000);
    }
  }
  async onModuleDestroy(): Promise<void> {
    this.stopping = true;
    this.health.ready = false;
    await this.consumer?.disconnect();
  }
}
function kafka(): Kafka {
  return new Kafka({
    clientId: `marketplace-${serviceName()}`,
    brokers: required('KAFKA_BROKERS')
      .split(',')
      .map((v) => v.trim()),
    logLevel: logLevel.ERROR,
    connectionTimeout: 5000,
    requestTimeout: 10000,
    retry: { retries: 4 },
    ssl: process.env.KAFKA_SSL === 'true',
  });
}
