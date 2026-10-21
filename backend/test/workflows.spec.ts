import { jest } from '@jest/globals';
import 'reflect-metadata';
import { randomUUID } from 'node:crypto';
import { Actor } from '../src/common/auth.js';
import { Database } from '../src/common/database.js';
import { InquiriesService, fingerprint } from '../src/inquiries/inquiries.service.js';
import { NotificationsService } from '../src/notifications/notifications.service.js';
import { CatalogService } from '../src/catalog/catalog.service.js';
const client: Actor = {
  id: 'client@example.com',
  email: 'client@example.com',
  name: 'Client',
  role: 'CLIENT',
};
const provider: Actor = {
  id: 'ava@example.com',
  email: 'ava@example.com',
  name: 'Ava',
  role: 'PROVIDER',
};
const input = {
  providerId: 'ava-martinez',
  subject: 'Platform build',
  message: 'Build a reliable product for a growing business.',
  budget: 500,
  clientType: 'COMPANY' as const,
};
const row = {
  id: randomUUID(),
  provider_id: 'ava-martinez',
  provider_email: provider.email,
  provider_name: 'Ava',
  client_email: client.email,
  client_name: 'Client',
  subject: input.subject,
  message: input.message,
  budget: '500.00',
  client_type: 'COMPANY',
  status: 'PENDING',
  created_at: new Date(),
  request_hash: fingerprint(input),
};
function database(rows: unknown[] = []) {
  const query = jest.fn<(...args: any[]) => Promise<any>>().mockResolvedValue({ rows });
  const db = {
    query,
    transaction: jest.fn(async (fn: (tx: { query: typeof query }) => Promise<unknown>) =>
      fn({ query }),
    ),
  };
  return { query, db: db as unknown as Database };
}
describe('inquiry workflow', () => {
  test('duplicate request returns original and emits no additional outbox event', async () => {
    const { query, db } = database([row]);
    const result = await new InquiriesService(db).create(client, 'request-key', input);
    expect(result.id).toBe(row.id);
    expect(query.mock.calls.some(([sql]) => sql.startsWith('INSERT'))).toBe(false);
  });
  test('same key with changed body conflicts', async () => {
    const { db } = database([row]);
    await expect(
      new InquiriesService(db).create(client, 'request-key', { ...input, budget: 999 }),
    ).rejects.toThrow('different inquiry');
  });
  test('missing idempotency key is rejected before DB access', async () => {
    const { query, db } = database();
    await expect(new InquiriesService(db).create(client, undefined, input)).rejects.toThrow(
      'Idempotency-Key',
    );
    expect(query).not.toHaveBeenCalled();
  });
  test('provider cannot send inquiries', async () => {
    const { db } = database();
    await expect(new InquiriesService(db).create(provider, 'request-key', input)).rejects.toThrow(
      'Only client',
    );
  });
  test('cross-owner status update denied before modification', async () => {
    const { query, db } = database([row]);
    await expect(
      new InquiriesService(db).respond({ ...provider, email: 'other@example.com' }, row.id, {
        status: 'ACCEPTED',
      }),
    ).rejects.toThrow('another provider');
    expect(query).toHaveBeenCalledTimes(1);
  });
  test('accepted inquiry cannot later be declined', async () => {
    const { query, db } = database([{ ...row, status: 'ACCEPTED' }]);
    await expect(
      new InquiriesService(db).respond(provider, row.id, { status: 'DECLINED' }),
    ).rejects.toThrow('already resolved');
    expect(query).toHaveBeenCalledTimes(1);
  });
  test('invalid status denied', async () => {
    const { db } = database([row]);
    await expect(
      new InquiriesService(db).respond(provider, row.id, { status: 'HACKED' }),
    ).rejects.toThrow();
  });
  test('participant query binds actor identity and never returns private emails', async () => {
    const { query, db } = database([row]);
    const result = await new InquiriesService(db).list(client);
    expect(query.mock.calls[0][1]).toEqual([client.email]);
    expect(result[0]).not.toHaveProperty('client_email');
    expect(result[0]).not.toHaveProperty('provider_email');
  });
  test('catalog downtime is a retryable 503 and creates nothing', async () => {
    process.env.CATALOG_URL = 'http://catalog:8182';
    process.env.INTERNAL_API_KEY = 'test-only-32-character-internal-key';
    const { query, db } = database();
    const spy = jest.spyOn(global, 'fetch').mockRejectedValueOnce(new Error('connection refused'));
    await expect(new InquiriesService(db).create(client, 'request-key', input)).rejects.toThrow(
      'Catalog is unavailable',
    );
    expect(query.mock.calls.some(([sql]) => sql.startsWith('INSERT'))).toBe(false);
    spy.mockRestore();
  });
});
describe('notification boundaries', () => {
  test('consumer uses unique event identity to deduplicate deliveries', async () => {
    const { query, db } = database();
    const event = {
      eventId: randomUUID(),
      inquiryId: row.id,
      recipientEmail: provider.email,
      providerName: 'Ava',
      clientName: 'Client',
      subject: input.subject,
      createdAt: new Date().toISOString(),
    };
    const service = new NotificationsService(db);
    await service.consume(event);
    await service.consume(event);
    expect(query.mock.calls[0][0]).toContain('ON CONFLICT(event_id) DO NOTHING');
    expect(query.mock.calls[0][1][1]).toBe(query.mock.calls[1][1][1]);
  });
  test('malformed event fails before database or Kafka acknowledgment', async () => {
    const { query, db } = database();
    await expect(new NotificationsService(db).consume({ eventId: 'invalid' })).rejects.toThrow();
    expect(query).not.toHaveBeenCalled();
  });
  test('other recipient cannot change read state', async () => {
    const { query, db } = database([{ id: row.id, recipient_email: 'someone@example.com' }]);
    await expect(new NotificationsService(db).read(provider, row.id)).rejects.toThrow(
      'another account',
    );
    expect(query).toHaveBeenCalledTimes(1);
  });
});
describe('catalog ownership and reputation', () => {
  test('provider cannot edit another profile', async () => {
    const fs = await import('node:fs/promises');
    const raw = JSON.parse(await fs.readFile('seeds/providers.json', 'utf8'))[0];
    const profile = { ...raw };
    delete profile.ownerEmail;
    const { db } = database([{ id: 'other-provider', document: profile }]);
    await expect(new CatalogService(db).update('other@example.com', profile)).rejects.toThrow(
      'another provider',
    );
  });
  test('self-edit cannot fabricate reputation', async () => {
    const fs = await import('node:fs/promises');
    const raw = JSON.parse(await fs.readFile('seeds/providers.json', 'utf8'))[0];
    const { ownerEmail, ...profile } = raw;
    const { db } = database([{ id: profile.id, document: profile }]);
    const result = await new CatalogService(db).update(ownerEmail, {
      ...profile,
      rating: 5,
      completedProjects: 99999,
    });
    expect(result.rating).toBe(profile.rating);
    expect(result.completedProjects).toBe(profile.completedProjects);
  });
});
