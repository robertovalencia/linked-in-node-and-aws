export const SERVICES = ['identity', 'catalog', 'inquiries', 'notifications'] as const;
export type ServiceName = (typeof SERVICES)[number];
export function serviceName(): ServiceName {
  const value = process.env.SERVICE;
  if (!SERVICES.includes(value as ServiceName))
    throw new Error('SERVICE must be identity, catalog, inquiries, or notifications');
  return value as ServiceName;
}
export function required(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`${name} is required`);
  return value;
}
export function validateConfig(): void {
  const service = serviceName();
  const secret = required('JWT_SECRET');
  if (Buffer.byteLength(secret) < 32) throw new Error('JWT_SECRET requires at least 32 bytes');
  const url = new URL(required('DB_URL'));
  if (!['postgres:', 'postgresql:'].includes(url.protocol))
    throw new Error('DB_URL must be PostgreSQL');
  if (['catalog', 'inquiries'].includes(service) && required('INTERNAL_API_KEY').length < 32)
    throw new Error('INTERNAL_API_KEY requires at least 32 characters');
  if (service === 'inquiries') {
    const catalog = new URL(required('CATALOG_URL'));
    if (!['http:', 'https:'].includes(catalog.protocol))
      throw new Error('CATALOG_URL must use HTTP or HTTPS');
  }
  if (['inquiries', 'notifications'].includes(service)) required('KAFKA_BROKERS');
}
