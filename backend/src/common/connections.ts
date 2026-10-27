import { readFileSync } from 'node:fs';
import type { PoolConfig } from 'pg';
import type { KafkaConfig } from 'kafkajs';
import { required, serviceName } from './config.js';

function enabled(name: string): boolean {
  const value = process.env[name];
  if (value !== undefined && !['true', 'false'].includes(value))
    throw new Error(`${name} must be true or false`);
  return value === 'true';
}
export function databaseOptions(): PoolConfig {
  const sslEnabled = enabled('DB_SSL');
  let connection: PoolConfig;
  if (process.env.DB_URL) {
    const url = new URL(process.env.DB_URL);
    if (!['postgres:', 'postgresql:'].includes(url.protocol))
      throw new Error('DB_URL must be PostgreSQL');
    // pg connection-string ssl parameters override the explicit TLS object.
    if ([...url.searchParams.keys()].some((key) => key.toLowerCase().startsWith('ssl')))
      throw new Error('Use DB_SSL and its CA settings instead of DB_URL ssl parameters');
    connection = { connectionString: process.env.DB_URL };
  } else {
    const port = Number(process.env.DB_PORT ?? '5432');
    if (!Number.isInteger(port) || port < 1 || port > 65535)
      throw new Error('DB_PORT must be a valid TCP port');
    connection = {
      host: required('DB_HOST'),
      port,
      database: required('DB_NAME'),
      user: required('DB_USER'),
      password: required('DB_PASSWORD'),
    };
  }
  const ca =
    process.env.DB_SSL_CA ??
    (process.env.DB_SSL_CA_FILE ? readFileSync(process.env.DB_SSL_CA_FILE, 'utf8') : undefined);
  if (!sslEnabled && ca) throw new Error('DB_SSL CA requires DB_SSL=true');
  if (process.env.DEPLOYMENT_MODE === 'aws-ecs' && (!sslEnabled || !ca))
    throw new Error('AWS ECS database connections require verified TLS with an explicit CA');
  return {
    ...connection,
    max: 10,
    connectionTimeoutMillis: 5000,
    ssl: sslEnabled ? { rejectUnauthorized: true, ...(ca ? { ca } : {}) } : undefined,
  };
}
export function kafkaOptions(): KafkaConfig {
  const sslEnabled = enabled('KAFKA_SSL');
  const ca = process.env.KAFKA_SSL_CA;
  const mechanism = process.env.KAFKA_SASL_MECHANISM;
  if (ca && !sslEnabled) throw new Error('KAFKA_SSL_CA requires KAFKA_SSL=true');
  if (mechanism && mechanism !== 'scram-sha-512')
    throw new Error('KAFKA_SASL_MECHANISM must be scram-sha-512');
  if ((mechanism || process.env.KAFKA_USERNAME || process.env.KAFKA_PASSWORD) && !sslEnabled)
    throw new Error('Kafka credentials require verified TLS');
  if (!mechanism && (process.env.KAFKA_USERNAME || process.env.KAFKA_PASSWORD))
    throw new Error('KAFKA_SASL_MECHANISM is required for credentials');
  if ((mechanism || process.env.DEPLOYMENT_MODE === 'aws-ecs') && (!sslEnabled || !ca))
    throw new Error('Authenticated Kafka requires verified TLS with an explicit CA');
  if (process.env.DEPLOYMENT_MODE === 'aws-ecs' && !mechanism)
    throw new Error('AWS ECS Kafka connections require SCRAM authentication');
  const brokers = required('KAFKA_BROKERS')
    .split(',')
    .map((value) => value.trim());
  if (brokers.some((broker) => !broker || !/^[a-zA-Z0-9.-]+:[0-9]+$/.test(broker)))
    throw new Error('KAFKA_BROKERS must contain host:port entries');
  return {
    clientId: `marketplace-${serviceName()}`,
    brokers,
    connectionTimeout: 5000,
    requestTimeout: 10000,
    retry: { retries: 4 },
    ssl: sslEnabled ? { rejectUnauthorized: true, ...(ca ? { ca: [ca] } : {}) } : false,
    ...(mechanism
      ? {
          sasl: {
            mechanism: 'scram-sha-512' as const,
            username: required('KAFKA_USERNAME'),
            password: required('KAFKA_PASSWORD'),
          },
        }
      : {}),
  };
}
