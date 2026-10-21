import 'reflect-metadata';
import jwt from 'jsonwebtoken';
import { signActor, verifyActor, requireRole, Actor } from '../src/common/auth.js';
import { hashPassword, verifyPassword } from '../src/identity/password.js';
import { providerSchema, searchSchema } from '../src/catalog/provider.schema.js';
import { inquirySchema } from '../src/inquiries/inquiry.schema.js';
import { fingerprint } from '../src/inquiries/inquiries.service.js';
const actor: Actor = {
  id: 'client@example.com',
  email: 'client@example.com',
  name: 'Client',
  role: 'CLIENT',
};
beforeAll(() => {
  process.env.JWT_SECRET = 'test-only-secret-at-least-32-bytes-long';
});
describe('JWT trust boundary', () => {
  test('verifies correct claims', () => expect(verifyActor(signActor(actor))).toEqual(actor));
  test('rejects unsigned/tampered tokens', () =>
    expect(() => verifyActor('invalid.token.signature')).toThrow('Invalid or expired'));
  test('rejects a different audience despite a valid signature', () => {
    const token = jwt.sign(actor, process.env.JWT_SECRET!, {
      issuer: 'marketplace',
      audience: 'other',
      subject: actor.email,
    });
    expect(() => verifyActor(token)).toThrow();
  });
  test('rejects expired tokens', () => {
    const token = jwt.sign(actor, process.env.JWT_SECRET!, {
      issuer: 'marketplace',
      audience: 'marketplace',
      subject: actor.email,
      expiresIn: -1,
    });
    expect(() => verifyActor(token)).toThrow();
  });
  test('does not permit a role escalation', () =>
    expect(() => requireRole(actor, 'PROVIDER')).toThrow());
});
describe('password storage', () => {
  test('salt differs, correct password verifies, wrong password fails', async () => {
    const first = await hashPassword('DemoPass123!');
    const second = await hashPassword('DemoPass123!');
    expect(first).not.toEqual(second);
    expect(first).not.toContain('DemoPass');
    expect(await verifyPassword('DemoPass123!', first)).toBe(true);
    expect(await verifyPassword('wrong', first)).toBe(false);
  });
  test('malformed stored hash is denied', async () =>
    expect(await verifyPassword('anything', 'scrypt:bad:bad')).toBe(false));
});
describe('input boundaries', () => {
  test.each([
    { available: 'yes' },
    { page: -1 },
    { size: 51 },
    { sort: 'arbitrary' },
    { maxRate: 'abc' },
    { q: ['one', 'two'] },
  ])('invalid search %j', (query) => expect(searchSchema.safeParse(query).success).toBe(false));
  const body = {
    providerId: 'ava-martinez',
    subject: 'New project',
    message: 'Please build a reliable application for our team.',
    budget: 100,
    clientType: 'COMPANY' as const,
  };
  test.each([-1, 0, 100.123, Infinity])('invalid budget %s', (budget) =>
    expect(inquirySchema.safeParse({ ...body, budget }).success).toBe(false),
  );
  test('fingerprint ignores object key order but detects content changes', () => {
    expect(fingerprint(body)).toBe(fingerprint({ ...body, providerId: body.providerId }));
    expect(fingerprint(body)).not.toBe(fingerprint({ ...body, budget: 101 }));
  });
  test('a private ownerEmail cannot be smuggled into an update', () => {
    expect(providerSchema.safeParse({ ownerEmail: 'other@example.com' }).success).toBe(false);
  });
});
