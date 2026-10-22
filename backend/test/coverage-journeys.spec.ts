import 'reflect-metadata';
import { jest } from '@jest/globals';
import { randomUUID } from 'node:crypto';
import { BadRequestException, Logger, NotFoundException } from '@nestjs/common';
import type { ExecutionContext } from '@nestjs/common';
import { Kafka } from 'kafkajs';
import { Actor, AuthGuard, signActor } from '../src/common/auth.js';
import { Database } from '../src/common/database.js';
import { ErrorFilter } from '../src/common/errors.js';
import { HealthController, WorkerHealth } from '../src/common/health.js';
import { CatalogController } from '../src/catalog/catalog.controller.js';
import { CatalogService } from '../src/catalog/catalog.service.js';
import { IdentityController } from '../src/identity/identity.controller.js';
import { IdentityService } from '../src/identity/identity.service.js';
import { hashPassword } from '../src/identity/password.js';
import { InquiriesController } from '../src/inquiries/inquiries.controller.js';
import { InquiriesService } from '../src/inquiries/inquiries.service.js';
import { NotificationsController } from '../src/notifications/notifications.controller.js';
import { NotificationsService } from '../src/notifications/notifications.service.js';
import { InquiryConsumer, OutboxPublisher } from '../src/common/messaging.js';

const client: Actor = {
  id: 'company@demo.local',
  email: 'company@demo.local',
  name: 'Morgan',
  role: 'CLIENT',
};
const provider: Actor = {
  id: 'ava@demo.local',
  email: 'ava@demo.local',
  name: 'Ava',
  role: 'PROVIDER',
};
const profile = {
  id: 'ava-martinez',
  name: 'Ava Martinez',
  headline: 'Developer',
  location: 'New York',
  category: 'Software Development',
  about: 'Builds resilient software for clients.',
  avatarUrl: '/avatar.png',
  coverColor: '#336699',
  skills: ['TypeScript'],
  tools: ['React'],
  services: ['Web applications'],
  experience: [],
  portfolio: [],
  hourlyRate: 95,
  currency: 'USD',
  available: true,
  rating: 4.8,
  reviewCount: 12,
  completedProjects: 7,
  responseTime: 'Within a day',
};
const body = {
  providerId: profile.id,
  subject: 'Platform build',
  message: 'Build a reliable product for our growing business.',
  budget: 500,
  clientType: 'COMPANY',
};

function fakeDb(responses: unknown[][] = []) {
  let index = 0;
  const query = jest.fn(async (...args: [string, unknown[]?]) => {
    void args;
    const rows = responses[index++] ?? [];
    return { rows, rowCount: rows.length };
  });
  const transaction = jest.fn(async <T>(fn: (tx: { query: typeof query }) => Promise<T>) =>
    fn({ query }),
  );
  return { db: { query, transaction } as unknown as Database, query, transaction };
}

beforeEach(() => {
  process.env.JWT_SECRET = 'test-only-secret-at-least-32-bytes-long';
  process.env.INTERNAL_API_KEY = 'test-only-internal-secret-at-least-32-characters';
  process.env.CATALOG_URL = 'http://catalog:8182';
  process.env.SERVICE = 'catalog';
  process.env.SEED_DEMO = 'false';
});

describe('catalog HTTP boundary and persistence', () => {
  test('public search binds escaped filters and stable paging', async () => {
    const { db, query } = fakeDb([[{ total: 1, items: [profile] }]]);
    const result = await new CatalogController(new CatalogService(db)).search({
      q: '100%_\\',
      category: profile.category,
      skill: 'TypeScript',
      maxRate: '100',
      available: 'true',
      sort: 'rate-asc',
      page: '1',
      size: '2',
    });
    expect(result).toEqual({ total: 1, items: [profile] });
    expect(query.mock.calls[0][0]).toContain('jsonb_array_elements_text');
    expect(query.mock.calls[0][0]).toContain('hourlyRate');
    expect(query.mock.calls[0][1]).toEqual([
      '%100\\%\\_\\\\%',
      profile.category,
      'TypeScript',
      100,
      true,
      2,
      2,
    ]);
  });
  test('own profile, public profile and missing profile are distinguished', async () => {
    const { db, query } = fakeDb([
      [{ document: profile }],
      [{ id: profile.id, owner_email: provider.email, document: profile }],
      [],
    ]);
    const api = new CatalogController(new CatalogService(db));
    expect(await api.mine({ actor: provider } as never)).toEqual(profile);
    expect(await api.get(profile.id)).toEqual(profile);
    await expect(api.get('unknown')).rejects.toBeInstanceOf(NotFoundException);
    expect(query.mock.calls[0][1]).toEqual([provider.email]);
  });
  test('internal owner lookup requires the independent shared key', async () => {
    const { db } = fakeDb([[{ id: profile.id, owner_email: provider.email, document: profile }]]);
    const api = new CatalogController(new CatalogService(db));
    await expect(api.internal(profile.id, 'wrong')).rejects.toThrow('Internal service key');
    await expect(
      api.internal(profile.id, 'x'.repeat(process.env.INTERNAL_API_KEY!.length)),
    ).rejects.toThrow('Internal service key');
    expect(await api.internal(profile.id, process.env.INTERNAL_API_KEY)).toEqual({
      id: profile.id,
      ownerEmail: provider.email,
      name: profile.name,
    });
  });
  test('profile edit preserves server-owned reputation', async () => {
    const { db, query } = fakeDb([[{ id: profile.id, document: profile }], []]);
    const api = new CatalogController(new CatalogService(db));
    const result = await api.update({ actor: provider } as never, {
      ...profile,
      headline: 'Architect',
      rating: 5,
      completedProjects: 999,
    });
    expect(result.headline).toBe('Architect');
    expect(result.rating).toBe(profile.rating);
    expect(result.completedProjects).toBe(profile.completedProjects);
    expect(query.mock.calls[1][0]).toContain('UPDATE providers');
    expect(() => api.mine({ actor: client } as never)).toThrow('Only provider');
  });
});

describe('identity and authentication HTTP boundary', () => {
  test('login verifies password and signs the actual stored role', async () => {
    const passwordHash = await hashPassword('DemoPass123!');
    const { db, query } = fakeDb([
      [{ email: client.email, name: client.name, role: client.role, password_hash: passwordHash }],
    ]);
    const api = new IdentityController(new IdentityService(db));
    const result = await api.login({ email: client.email, password: 'DemoPass123!' }, {
      ip: '203.0.113.10',
    } as never);
    expect(result).toMatchObject(client);
    expect(result.token).toEqual(expect.any(String));
    expect(query.mock.calls[0][1]).toEqual([client.email]);
    expect(api.me({ actor: client } as never)).toEqual(client);
  });
  test('unknown account and wrong password are denied alike', async () => {
    const passwordHash = await hashPassword('DemoPass123!');
    const { db } = fakeDb([
      [],
      [{ email: client.email, name: client.name, role: client.role, password_hash: passwordHash }],
    ]);
    const api = new IdentityController(new IdentityService(db));
    await expect(
      api.login({ email: client.email, password: 'wrong' }, { ip: '203.0.113.11' } as never),
    ).rejects.toThrow('Invalid email or password');
    await expect(
      api.login({ email: client.email, password: 'wrong' }, { ip: '203.0.113.11' } as never),
    ).rejects.toThrow('Invalid email or password');
  });
  test('throttle limits repeated attempts per address', async () => {
    const { db, query } = fakeDb();
    const api = new IdentityController(new IdentityService(db));
    for (let i = 0; i < 30; i++)
      await expect(
        api.login({ email: client.email, password: 'bad' }, { ip: '198.51.100.2' } as never),
      ).rejects.toThrow();
    await expect(
      api.login({ email: client.email, password: 'bad' }, { ip: '198.51.100.2' } as never),
    ).rejects.toThrow('Too many login attempts');
    expect(query).toHaveBeenCalledTimes(30);
  });
  test('bearer guard attaches only a verified principal', () => {
    const guard = new AuthGuard();
    const request = {
      headers: {} as { authorization?: string },
      actor: undefined as Actor | undefined,
    };
    const context = { switchToHttp: () => ({ getRequest: () => request }) } as ExecutionContext;
    expect(() => guard.canActivate(context)).toThrow('Bearer token required');
    request.headers.authorization = `Bearer ${signActor(client)}`;
    expect(guard.canActivate(context)).toBe(true);
    expect(request.actor).toEqual(client);
  });
});

describe('inquiry and notification API journeys', () => {
  test('participants and recipients see only their own mapped records', async () => {
    const id = randomUUID();
    const created_at = new Date();
    const inquiry = {
      id,
      provider_id: profile.id,
      provider_name: profile.name,
      client_name: client.name,
      subject: body.subject,
      message: body.message,
      budget: '500.00',
      client_type: 'COMPANY',
      status: 'PENDING',
      created_at,
    };
    const notification = {
      id: randomUUID(),
      inquiry_id: id,
      message: 'New inquiry',
      created_at,
      read: false,
    };
    const { db, query } = fakeDb([[inquiry], [notification]]);
    const inquiries = await new InquiriesController(new InquiriesService(db)).list({
      actor: client,
    } as never);
    const notifications = await new NotificationsController(new NotificationsService(db)).list({
      actor: provider,
    } as never);
    expect(inquiries[0]).toMatchObject({ id, providerId: profile.id, budget: 500 });
    expect(notifications[0]).toMatchObject({ inquiryId: id, read: false });
    expect(query.mock.calls[0][1]).toEqual([client.email]);
    expect(query.mock.calls[1][1]).toEqual([provider.email]);
    expect(inquiries[0]).not.toHaveProperty('provider_email');
    expect(notifications[0]).not.toHaveProperty('recipient_email');
  });
  test('missing notification cannot be marked read', async () => {
    const id = randomUUID();
    const { db, query } = fakeDb([[]]);
    await expect(new NotificationsService(db).read(provider, id)).rejects.toThrow(
      'Notification not found',
    );
    expect(query.mock.calls).toHaveLength(1);
    expect(query.mock.calls[0][1]).toEqual([id]);
  });
  test('new inquiry commits an outbox event in the same transaction', async () => {
    const id = randomUUID();
    const { db, query, transaction } = fakeDb([
      [],
      [],
      [
        {
          id,
          provider_id: profile.id,
          provider_name: profile.name,
          client_name: client.name,
          subject: body.subject,
          message: body.message,
          budget: '500.00',
          client_type: 'COMPANY',
          status: 'PENDING',
          created_at: new Date(),
        },
      ],
      [],
    ]);
    const fetchSpy = jest.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ id: profile.id, ownerEmail: provider.email, name: profile.name }),
    } as Response);
    try {
      const api = new InquiriesController(new InquiriesService(db));
      const result = await api.create({ actor: client } as never, 'request-key-123', body);
      expect(result.id).toBe(id);
      expect(result).not.toHaveProperty('provider_email');
      expect(transaction).toHaveBeenCalledTimes(1);
      expect(query.mock.calls.map(([sql]) => sql)).toEqual([
        expect.stringContaining('pg_advisory_xact_lock'),
        expect.stringContaining('SELECT * FROM inquiries'),
        expect.stringContaining('INSERT INTO inquiries'),
        expect.stringContaining('INSERT INTO outbox'),
      ]);
      expect(query.mock.calls[3][1]?.[2]).toMatchObject({
        inquiryId: query.mock.calls[2][1]?.[0],
        recipientEmail: provider.email,
      });
    } finally {
      fetchSpy.mockRestore();
    }
  });
  test('provider lookup failure does not insert inquiry or outbox', async () => {
    const { db, query } = fakeDb([[], []]);
    const fetchSpy = jest
      .spyOn(global, 'fetch')
      .mockResolvedValue({ ok: false, status: 404 } as Response);
    try {
      await expect(
        new InquiriesService(db).create(client, 'request-key-123', body),
      ).rejects.toThrow('Provider not found');
      expect(query.mock.calls.some(([sql]) => sql.startsWith('INSERT'))).toBe(false);
    } finally {
      fetchSpy.mockRestore();
    }
  });
  test('provider decision and inbox read enforce owner and persist result', async () => {
    const id = randomUUID();
    const pending = {
      id,
      provider_id: profile.id,
      provider_email: provider.email,
      provider_name: profile.name,
      client_name: client.name,
      subject: body.subject,
      message: body.message,
      budget: '500.00',
      client_type: 'COMPANY',
      status: 'PENDING',
      created_at: new Date(),
    };
    const { db, query } = fakeDb([
      [pending],
      [{ ...pending, status: 'ACCEPTED' }],
      [{ id, recipient_email: provider.email }],
      [{ id, inquiry_id: id, message: 'New inquiry', created_at: new Date(), read: true }],
    ]);
    const inquiryApi = new InquiriesController(new InquiriesService(db));
    const accepted = await inquiryApi.respond({ actor: provider } as never, id, {
      status: 'ACCEPTED',
    });
    expect(accepted.status).toBe('ACCEPTED');
    const notificationApi = new NotificationsController(new NotificationsService(db));
    const read = await notificationApi.read({ actor: provider } as never, id);
    expect(read.read).toBe(true);
    expect(query.mock.calls[3][0]).toContain('UPDATE notifications');
  });
});

describe('health, error and outbox behavior', () => {
  test('readiness reports database and messaging failures as 503', async () => {
    process.env.SERVICE = 'inquiries';
    const { db, query } = fakeDb([[]]);
    const worker = new WorkerHealth();
    const health = new HealthController(db, worker);
    expect(health.live()).toMatchObject({ status: 'UP', service: 'inquiries' });
    await expect(health.ready()).rejects.toThrow('Database or messaging');
    worker.ready = true;
    expect(await health.ready()).toMatchObject({ database: 'UP', messaging: 'UP' });
    query.mockRejectedValueOnce(new Error('connection down'));
    await expect(health.ready()).rejects.toThrow('Database or messaging');
  });
  test('error filter maps validation and hides internal failures', () => {
    const status = jest.fn().mockReturnThis();
    const json = jest.fn().mockReturnThis();
    const host = { switchToHttp: () => ({ getResponse: () => ({ status, json }) }) } as never;
    const filter = new ErrorFilter();
    filter.catch(new BadRequestException('Bad input'), host);
    expect(status).toHaveBeenLastCalledWith(400);
    expect(json).toHaveBeenLastCalledWith({ status: 400, detail: 'Bad input' });
    const log = jest.spyOn(Logger.prototype, 'error').mockImplementation(() => undefined);
    try {
      filter.catch(new Error('private database password'), host);
      expect(log).toHaveBeenCalledTimes(1);
    } finally {
      log.mockRestore();
    }
    expect(status).toHaveBeenLastCalledWith(500);
    expect(json).toHaveBeenLastCalledWith({ status: 500, detail: 'Internal server error' });
  });
  test('outbox marks each event delivered only after broker acknowledgment', async () => {
    const id = randomUUID();
    const eventId = randomUUID();
    const event = { event_id: eventId, inquiry_id: id, payload: { eventId, inquiryId: id } };
    const { db, query } = fakeDb([[event], []]);
    const send = jest.fn<() => Promise<void>>().mockResolvedValue();
    const publisher = new OutboxPublisher(db, { ready: false } as WorkerHealth);
    (publisher as unknown as { producer: { send: typeof send } }).producer = { send };
    await publisher.publishBatch();
    expect(send).toHaveBeenCalledWith({
      topic: 'inquiry.created.v1',
      acks: -1,
      messages: [{ key: id, value: JSON.stringify(event.payload) }],
    });
    expect(query.mock.calls[1]).toEqual([expect.stringContaining('UPDATE outbox'), [eventId]]);
  });
  test('broker rejection leaves the outbox row pending for retry', async () => {
    const event = {
      event_id: randomUUID(),
      inquiry_id: randomUUID(),
      payload: { subject: 'Retry' },
    };
    const { db, query } = fakeDb([[event]]);
    const send = jest.fn<() => Promise<void>>().mockRejectedValue(new Error('broker unavailable'));
    const publisher = new OutboxPublisher(db, { ready: false } as WorkerHealth);
    (publisher as unknown as { producer: { send: typeof send } }).producer = { send };
    await expect(publisher.publishBatch()).rejects.toThrow('broker unavailable');
    expect(query.mock.calls).toHaveLength(1);
    expect(query.mock.calls[0][0]).toContain('FOR UPDATE SKIP LOCKED');
  });
  test('publisher connects, drains pending events, and turns readiness off at shutdown', async () => {
    process.env.SERVICE = 'inquiries';
    process.env.KAFKA_BROKERS = '127.0.0.1:19092';
    const event = {
      event_id: randomUUID(),
      inquiry_id: randomUUID(),
      payload: { subject: 'Ready' },
    };
    const { db, query } = fakeDb([[event], []]);
    const producer = {
      connect: jest.fn(async () => undefined),
      send: jest.fn(async () => undefined),
      disconnect: jest.fn(async () => undefined),
    };
    const spy = jest.spyOn(Kafka.prototype, 'producer').mockReturnValue(producer as never);
    const health = { ready: false } as WorkerHealth;
    const publisher = new OutboxPublisher(db, health);
    try {
      publisher.onApplicationBootstrap();
      for (let i = 0; i < 20 && !health.ready; i++) await new Promise((r) => setTimeout(r, 10));
      expect(health.ready).toBe(true);
      expect(producer.connect).toHaveBeenCalledTimes(1);
      expect(producer.send).toHaveBeenCalledTimes(1);
      expect(query.mock.calls[1][0]).toContain('UPDATE outbox');
      await publisher.onModuleDestroy();
      expect(health.ready).toBe(false);
      expect(producer.disconnect).toHaveBeenCalled();
    } finally {
      spy.mockRestore();
    }
  });
  test('consumer acknowledges only a durable inbox insert and tracks broker health', async () => {
    process.env.SERVICE = 'notifications';
    process.env.KAFKA_BROKERS = '127.0.0.1:19092';
    const callbacks = new Map<string, (event: any) => void>();
    let eachMessage: ((input: { message: { value: Buffer | null } }) => Promise<void>) | undefined;
    const kafkaConsumer = {
      events: { CRASH: 'CRASH', GROUP_JOIN: 'GROUP_JOIN', DISCONNECT: 'DISCONNECT' },
      on: jest.fn((type: string, callback: (event: any) => void) => {
        callbacks.set(type, callback);
      }),
      connect: jest.fn(async () => undefined),
      subscribe: jest.fn(async () => undefined),
      run: jest.fn(async (options: { eachMessage: typeof eachMessage }) => {
        eachMessage = options.eachMessage;
      }),
      disconnect: jest.fn(async () => undefined),
    };
    const spy = jest.spyOn(Kafka.prototype, 'consumer').mockReturnValue(kafkaConsumer as never);
    const consume = jest.fn(async (...args: [unknown]) => {
      void args;
    });
    const health = { ready: false } as WorkerHealth;
    const worker = new InquiryConsumer({ consume } as unknown as NotificationsService, health);
    try {
      worker.onApplicationBootstrap();
      for (let i = 0; i < 20 && !eachMessage; i++) await new Promise((r) => setTimeout(r, 10));
      expect(eachMessage).toBeDefined();
      callbacks.get('GROUP_JOIN')?.({});
      expect(health.ready).toBe(true);
      const event = { eventId: randomUUID() };
      await eachMessage!({ message: { value: Buffer.from(JSON.stringify(event)) } });
      expect(consume).toHaveBeenCalledWith(event);
      await expect(eachMessage!({ message: { value: null } })).rejects.toThrow(
        'Event payload missing',
      );
      callbacks.get('DISCONNECT')?.({});
      expect(health.ready).toBe(false);
      await worker.onModuleDestroy();
      expect(kafkaConsumer.disconnect).toHaveBeenCalled();
    } finally {
      spy.mockRestore();
    }
  });
});

describe('database migrations and transaction boundaries', () => {
  test('applies the identity migration under an advisory lock and commits', async () => {
    process.env.SERVICE = 'identity';
    process.env.DB_URL = 'postgresql://local:local@127.0.0.1:55432/identity';
    const db = new Database();
    const query = jest.fn(async (...args: [string, unknown[]?]) => {
      void args;
      return { rows: [], rowCount: 0 };
    });
    const release = jest.fn();
    const connect = jest.spyOn(db.pool, 'connect').mockResolvedValue({ query, release } as never);
    const end = jest.spyOn(db.pool, 'end').mockResolvedValue(undefined as never);
    try {
      await db.onModuleInit();
      expect(query.mock.calls.map(([sql]) => sql)).toEqual([
        'BEGIN',
        expect.stringContaining('pg_advisory_xact_lock'),
        expect.stringContaining('CREATE TABLE IF NOT EXISTS schema_migrations'),
        expect.stringContaining('SELECT checksum FROM schema_migrations'),
        expect.stringContaining('CREATE TABLE'),
        expect.stringContaining('INSERT INTO schema_migrations'),
        'COMMIT',
      ]);
      expect(query.mock.calls[1][1]).toEqual(['marketplace-migrations-identity']);
      expect(release).toHaveBeenCalledTimes(1);
      await db.onModuleDestroy();
      expect(end).toHaveBeenCalledTimes(1);
    } finally {
      connect.mockRestore();
      end.mockRestore();
    }
  });
  test('a failed operation rolls back and releases its connection', async () => {
    process.env.DB_URL = 'postgresql://local:local@127.0.0.1:55432/identity';
    const db = new Database();
    const query = jest.fn(async (...args: [string]) => {
      void args;
      return { rows: [], rowCount: 0 };
    });
    const release = jest.fn();
    const connect = jest.spyOn(db.pool, 'connect').mockResolvedValue({ query, release } as never);
    try {
      await expect(
        db.transaction(async () => {
          throw new Error('operation failed');
        }),
      ).rejects.toThrow('operation failed');
      expect(query.mock.calls.map(([sql]) => sql)).toEqual(['BEGIN', 'ROLLBACK']);
      expect(release).toHaveBeenCalledTimes(1);
    } finally {
      connect.mockRestore();
    }
  });
  test('rejects an edited migration checksum before applying SQL', async () => {
    process.env.SERVICE = 'identity';
    process.env.DB_URL = 'postgresql://local:local@127.0.0.1:55432/identity';
    const db = new Database();
    const query = jest.fn(async (sql: string) =>
      sql.startsWith('SELECT checksum')
        ? { rows: [{ checksum: 'wrong-checksum' }], rowCount: 1 }
        : { rows: [], rowCount: 0 },
    );
    const release = jest.fn();
    const connect = jest.spyOn(db.pool, 'connect').mockResolvedValue({ query, release } as never);
    try {
      await expect(db.onModuleInit()).rejects.toThrow('changed after application');
      expect(query.mock.calls.at(-1)?.[0]).toBe('ROLLBACK');
      expect(release).toHaveBeenCalledTimes(1);
    } finally {
      connect.mockRestore();
    }
  });
});

describe('first-run seed behavior', () => {
  test('seeds provider profiles without overwriting owner edits', async () => {
    process.env.SEED_DEMO = 'true';
    const { db, query, transaction } = fakeDb();
    await new CatalogService(db).onApplicationBootstrap();
    expect(transaction).toHaveBeenCalledTimes(1);
    expect(query.mock.calls.length).toBeGreaterThanOrEqual(6);
    expect(query.mock.calls[0][0]).toContain('ON CONFLICT(id) DO NOTHING');
  });
  test('seeds provider and client logins without replacing passwords', async () => {
    process.env.SEED_DEMO = 'true';
    const { db, query, transaction } = fakeDb();
    await new IdentityService(db).onApplicationBootstrap();
    expect(transaction).toHaveBeenCalledTimes(1);
    expect(query.mock.calls.length).toBeGreaterThanOrEqual(8);
    expect(query.mock.calls[0][0]).toContain('ON CONFLICT(email) DO NOTHING');
    expect(query.mock.calls.some(([, values]) => values?.[0] === client.email)).toBe(true);
  });
});
