import { Controller, Get, Injectable, ServiceUnavailableException } from '@nestjs/common';
import { Database } from './database.js';
import { serviceName } from './config.js';
@Injectable()
export class WorkerHealth {
  ready = !['inquiries', 'notifications'].includes(serviceName());
}
@Controller()
export class HealthController {
  constructor(
    private readonly db: Database,
    private readonly worker: WorkerHealth,
  ) {}
  @Get(['health/live', 'actuator/health/liveness']) live() {
    return { status: 'UP', service: serviceName() };
  }
  // Routing readiness preserves durable inquiry writes while Kafka retries asynchronously.
  @Get('health/serve') async serving() {
    try {
      await this.db.query('SELECT 1');
    } catch {
      throw new ServiceUnavailableException('Database dependency unavailable');
    }
    return { status: 'UP', service: serviceName(), database: 'UP' };
  }
  @Get(['health/ready', 'health', 'actuator/health', 'actuator/health/readiness']) async ready() {
    try {
      await this.db.query('SELECT 1');
      if (!this.worker.ready) throw new Error('Messaging worker not ready');
    } catch {
      throw new ServiceUnavailableException('Database or messaging dependency unavailable');
    }
    return {
      status: 'UP',
      service: serviceName(),
      database: 'UP',
      messaging: this.worker.ready ? 'UP' : 'DOWN',
    };
  }
}
