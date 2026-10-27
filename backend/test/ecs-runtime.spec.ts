import 'reflect-metadata';
import { jest } from '@jest/globals';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';
import { connect, createServer } from 'node:tls';
import type { Client } from 'pg';
import { databaseOptions, kafkaOptions } from '../src/common/connections.js';
import { bootstrapDatabases } from '../src/operations/database-bootstrap.js';
import { replayPublishedOutbox } from '../src/operations/replay-outbox.js';
import { HealthController, WorkerHealth } from '../src/common/health.js';
import type { Database } from '../src/common/database.js';
const original = { ...process.env };
beforeEach(() => {
  for (const key of Object.keys(process.env))
    if (/^(DB_|KAFKA_|DEPLOYMENT_MODE)/.test(key)) delete process.env[key];
  Object.assign(process.env, {
    SERVICE: 'inquiries',
    DB_HOST: 'database.internal',
    DB_NAME: 'inquiries',
    DB_USER: 'inquiries',
    DB_PASSWORD: 'password/with:@reserved?characters#%',
    KAFKA_BROKERS: 'kafka.internal:9093',
  });
});
afterEach(() => {
  for (const key of Object.keys(process.env)) if (!(key in original)) delete process.env[key];
  Object.assign(process.env, original);
});
describe('private ECS connection boundaries', () => {
  test('passes reserved characters as a password field without URI interpolation', () => {
    expect(databaseOptions()).toMatchObject({
      password: process.env.DB_PASSWORD,
      host: 'database.internal',
      database: 'inquiries',
      port: 5432,
    });
    expect(databaseOptions()).not.toHaveProperty('connectionString');
  });
  test.each(['0', '65536', 'x'])('rejects invalid DB port %s', (port) => {
    process.env.DB_PORT = port;
    expect(databaseOptions).toThrow('DB_PORT');
  });
  test.each(['sslmode=disable', 'sslmode=no-verify', 'sslrootcert=/tmp/ca'])(
    'rejects URI TLS override %s',
    (query) => {
      process.env.DB_URL = `postgres://user:password@localhost/db?${query}`;
      expect(databaseOptions).toThrow('DB_URL ssl parameters');
    },
  );
  test('ECS fails closed for missing TLS and missing explicit CA', () => {
    process.env.DEPLOYMENT_MODE = 'aws-ecs';
    expect(databaseOptions).toThrow('verified TLS');
    process.env.DB_SSL = 'true';
    expect(databaseOptions).toThrow('explicit CA');
    process.env.DB_SSL_CA_FILE = 'certs/rds-us-east-2-bundle.pem';
    expect(databaseOptions().ssl).toMatchObject({
      rejectUnauthorized: true,
      ca: expect.stringContaining('BEGIN CERTIFICATE'),
    });
  });
  test('rejects typo TLS switches and CA attached to plaintext', () => {
    process.env.DB_SSL = 'yes';
    expect(databaseOptions).toThrow('true or false');
    process.env.DB_SSL = 'false';
    process.env.DB_SSL_CA = 'CA';
    expect(databaseOptions).toThrow('requires DB_SSL');
  });
  test('Kafka SCRAM fails closed without TLS/CA or with unsupported mechanism', () => {
    process.env.KAFKA_SASL_MECHANISM = 'scram-sha-512';
    process.env.KAFKA_USERNAME = 'inquiries';
    process.env.KAFKA_PASSWORD = 'test-password';
    expect(kafkaOptions).toThrow('verified TLS');
    process.env.KAFKA_SSL = 'true';
    expect(kafkaOptions).toThrow('explicit CA');
    process.env.KAFKA_SSL_CA = 'trusted lab CA';
    expect(kafkaOptions()).toMatchObject({
      ssl: { rejectUnauthorized: true, ca: ['trusted lab CA'] },
      sasl: { mechanism: 'scram-sha-512', username: 'inquiries', password: 'test-password' },
    });
    process.env.KAFKA_SASL_MECHANISM = 'plain';
    expect(kafkaOptions).toThrow('scram-sha-512');
  });
  test('ECS rejects anonymous Kafka and absent password', () => {
    Object.assign(process.env, {
      DEPLOYMENT_MODE: 'aws-ecs',
      KAFKA_SSL: 'true',
      KAFKA_SSL_CA: 'CA',
    });
    expect(kafkaOptions).toThrow('SCRAM authentication');
    Object.assign(process.env, {
      KAFKA_SASL_MECHANISM: 'scram-sha-512',
      KAFKA_USERNAME: 'inquiries',
    });
    expect(kafkaOptions).toThrow('KAFKA_PASSWORD is required');
  });
  test.each(['', 'kafka:9093,', 'http://kafka:9093'])('rejects malformed brokers %s', (value) => {
    process.env.KAFKA_BROKERS = value;
    expect(kafkaOptions).toThrow();
  });
  test('routing stays ready while broker is down, strict readiness reports degraded', async () => {
    const db = {
      query: jest.fn<() => Promise<unknown>>().mockResolvedValue({ rows: [] }),
    } as unknown as Database;
    const health = new HealthController(db, { ready: false } as WorkerHealth);
    await expect(health.serving()).resolves.toMatchObject({ status: 'UP' });
    await expect(health.ready()).rejects.toThrow('messaging dependency');
    (db.query as jest.Mock).mockRejectedValueOnce(new Error('DB unavailable') as never);
    await expect(health.serving()).rejects.toThrow('Database dependency unavailable');
  });
});
describe('TLS certificate verification executes against a local TLS server', () => {
  let directory: string;
  let ca: string;
  let key: string;
  beforeAll(() => {
    directory = mkdtempSync(join(tmpdir(), 'marketplace-tls-'));
    execFileSync(
      'openssl',
      [
        'req',
        '-x509',
        '-newkey',
        'rsa:2048',
        '-nodes',
        '-days',
        '1',
        '-subj',
        '/CN=localhost',
        '-addext',
        'subjectAltName=DNS:localhost',
        '-keyout',
        join(directory, 'key.pem'),
        '-out',
        join(directory, 'cert.pem'),
      ],
      { stdio: 'ignore' },
    );
    ca = readFileSync(join(directory, 'cert.pem'), 'utf8');
    key = readFileSync(join(directory, 'key.pem'), 'utf8');
  });
  afterAll(() => rmSync(directory, { recursive: true, force: true }));
  async function handshake(trust: string | undefined, name: string): Promise<void> {
    const server = createServer({ key, cert: ca }, (socket) => socket.end());
    server.on('tlsClientError', () => undefined);
    await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
    const address = server.address() as { port: number };
    try {
      await new Promise<void>((resolve, reject) => {
        const socket = connect(
          {
            host: '127.0.0.1',
            port: address.port,
            servername: name,
            rejectUnauthorized: true,
            ...(trust ? { ca: trust } : {}),
          },
          () => {
            socket.end();
            resolve();
          },
        );
        socket.on('error', reject);
      });
    } finally {
      await new Promise<void>((resolve) => server.close(() => resolve()));
    }
  }
  test('accepts trusted CA and exact hostname', async () => {
    await expect(handshake(ca, 'localhost')).resolves.toBeUndefined();
  });
  test('rejects untrusted CA with verification enabled', async () => {
    await expect(handshake(undefined, 'localhost')).rejects.toThrow();
  });
  test('rejects wrong hostname even with the trusted CA', async () => {
    await expect(handshake(ca, 'other.internal')).rejects.toThrow('not in the cert');
  });
});
describe('one-shot RDS ownership bootstrap', () => {
  function setup(existing = false, owner = 'identity') {
    Object.assign(process.env, { DB_SSL: 'true', DB_SSL_CA: 'test CA', DB_NAME: 'postgres' });
    for (const service of ['IDENTITY', 'CATALOG', 'INQUIRIES', 'NOTIFICATIONS'])
      process.env[`${service}_DB_PASSWORD`] = "long-owned-password-with-'quote-at-least-32-bytes";
    const query = jest
      .fn<(sql: string, params?: unknown[]) => Promise<any>>()
      .mockImplementation(async (sql, params) => {
        if (sql.startsWith('SELECT 1 FROM pg_roles'))
          return { rowCount: existing ? 1 : 0, rows: [] };
        if (sql.startsWith('SELECT pg_get_userbyid'))
          return {
            rowCount: existing ? 1 : 0,
            rows: [{ owner: owner === 'identity' ? params?.[0] : owner }],
          };
        return { rowCount: 0, rows: [] };
      });
    const admin = {
      connect: jest.fn<() => Promise<void>>().mockResolvedValue(),
      query,
      end: jest.fn<() => Promise<void>>().mockResolvedValue(),
    };
    return { admin, query };
  }
  test('creates four owned databases and denies PUBLIC connections with escaped passwords', async () => {
    const { admin, query } = setup();
    await bootstrapDatabases(admin as unknown as Client);
    expect(query.mock.calls.filter(([sql]) => sql.startsWith('CREATE DATABASE'))).toHaveLength(4);
    expect(query.mock.calls.filter(([sql]) => sql.startsWith('REVOKE ALL'))).toHaveLength(4);
    expect(query.mock.calls.find(([sql]) => sql.startsWith('CREATE ROLE'))?.[0]).toContain(
      "with-''quote",
    );
    expect(admin.end).toHaveBeenCalledTimes(1);
  });
  test('idempotent rerun alters existing logins without recreating databases', async () => {
    const { admin, query } = setup(true);
    await bootstrapDatabases(admin as unknown as Client);
    expect(query.mock.calls.some(([sql]) => sql.startsWith('CREATE DATABASE'))).toBe(false);
    expect(query.mock.calls.filter(([sql]) => sql.startsWith('ALTER ROLE'))).toHaveLength(4);
  });
  test('unexpected owner fails before changing that database and closes admin connection', async () => {
    const { admin } = setup(true, 'unexpected');
    await expect(bootstrapDatabases(admin as unknown as Client)).rejects.toThrow(
      'unexpected owner',
    );
    expect(admin.end).toHaveBeenCalledTimes(1);
  });
  test('requires TLS and strong complete credentials before connecting', async () => {
    const { admin } = setup();
    process.env.DB_SSL = 'false';
    delete process.env.DB_SSL_CA;
    await expect(bootstrapDatabases(admin as unknown as Client)).rejects.toThrow('verified TLS');
    process.env.DB_SSL = 'true';
    process.env.IDENTITY_DB_PASSWORD = 'weak';
    await expect(bootstrapDatabases(admin as unknown as Client)).rejects.toThrow('at least 32');
    expect(admin.connect).not.toHaveBeenCalled();
  });
});

describe('explicit controlled outbox recovery', () => {
  test('requires exact confirmation and the inquiries capability before database access', async () => {
    await expect(replayPublishedOutbox()).rejects.toThrow('REPLAY_OUTBOX_CONFIRM');
    process.env.REPLAY_OUTBOX_CONFIRM = 'replay-all-published-events';
    process.env.SERVICE = 'notifications';
    await expect(replayPublishedOutbox()).rejects.toThrow('inquiries capability');
  });
  test('resets only delivery metadata and reports count without changing event identity or payload', async () => {
    process.env.REPLAY_OUTBOX_CONFIRM = 'replay-all-published-events';
    const query = jest
      .fn<() => Promise<unknown>>()
      .mockResolvedValue({ rows: [{ replay_count: '3' }] });
    const db = { query } as unknown as Database;
    await expect(replayPublishedOutbox(db)).resolves.toBe(3);
    expect(query).toHaveBeenCalledWith(
      'WITH replay AS (UPDATE outbox SET published_at=NULL WHERE published_at IS NOT NULL RETURNING event_id) SELECT count(*) AS replay_count FROM replay',
    );
  });
});
