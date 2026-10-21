import { validateConfig, serviceName, required } from '../src/common/config.js';
const original = { ...process.env };
beforeEach(() => {
  process.env.SERVICE = 'inquiries';
  process.env.JWT_SECRET = 'test-secret-with-at-least-thirty-two-bytes';
  process.env.INTERNAL_API_KEY = 'test-internal-key-with-at-least-thirty-two-bytes';
  process.env.DB_URL = 'postgresql://inquiries:password@localhost:5432/inquiries';
  process.env.CATALOG_URL = 'http://catalog:8182';
  process.env.KAFKA_BROKERS = 'kafka:9092';
});
afterEach(() => {
  for (const key of [
    'SERVICE',
    'JWT_SECRET',
    'INTERNAL_API_KEY',
    'DB_URL',
    'CATALOG_URL',
    'KAFKA_BROKERS',
  ]) {
    if (original[key] === undefined) delete process.env[key];
    else process.env[key] = original[key];
  }
});
describe('runtime environment trust boundaries', () => {
  test('accepts complete inquiry configuration and HTTPS catalog', () => {
    expect(validateConfig()).toBeUndefined();
    process.env.CATALOG_URL = 'https://catalog.internal';
    expect(validateConfig()).toBeUndefined();
    expect(serviceName()).toBe('inquiries');
    expect(required('KAFKA_BROKERS')).toBe('kafka:9092');
  });
  test('rejects an unknown service instead of booting the wrong capability', () => {
    process.env.SERVICE = 'admin';
    expect(validateConfig).toThrow('SERVICE must');
  });
  test('rejects missing and undersized JWT secrets', () => {
    delete process.env.JWT_SECRET;
    expect(validateConfig).toThrow('JWT_SECRET is required');
    process.env.JWT_SECRET = 'short';
    expect(validateConfig).toThrow('at least 32 bytes');
  });
  test('rejects a non-Postgres database URI', () => {
    process.env.DB_URL = 'https://not-a-database';
    expect(validateConfig).toThrow('DB_URL must be PostgreSQL');
  });
  test('rejects malformed URI and insufficient internal authentication', () => {
    process.env.DB_URL = 'malformed';
    expect(validateConfig).toThrow();
    process.env.DB_URL = 'postgres://inquiries@localhost/inquiries';
    process.env.INTERNAL_API_KEY = 'short';
    expect(validateConfig).toThrow('INTERNAL_API_KEY requires');
  });
  test('rejects non-HTTP catalog URL and missing broker configuration', () => {
    process.env.CATALOG_URL = 'file:///etc/passwd';
    expect(validateConfig).toThrow('HTTP or HTTPS');
    process.env.CATALOG_URL = 'http://catalog:8182';
    delete process.env.KAFKA_BROKERS;
    expect(validateConfig).toThrow('KAFKA_BROKERS is required');
  });
  test('identity does not require unrelated catalog, broker or internal key', () => {
    process.env.SERVICE = 'identity';
    delete process.env.INTERNAL_API_KEY;
    delete process.env.CATALOG_URL;
    delete process.env.KAFKA_BROKERS;
    expect(validateConfig()).toBeUndefined();
  });
});
