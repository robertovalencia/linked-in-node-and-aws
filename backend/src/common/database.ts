import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { Pool, PoolClient, QueryResultRow } from 'pg';
import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { serviceName, required } from './config.js';

@Injectable()
export class Database implements OnModuleInit, OnModuleDestroy {
  readonly pool = new Pool({
    connectionString: required('DB_URL'),
    max: 10,
    connectionTimeoutMillis: 5000,
    ssl:
      process.env.DB_SSL === 'true'
        ? {
            rejectUnauthorized: true,
            ...(process.env.DB_SSL_CA ? { ca: process.env.DB_SSL_CA } : {}),
          }
        : undefined,
  });
  constructor() {
    this.pool.on('error', (error: Error) =>
      console.error(
        JSON.stringify({ level: 'error', event: 'database_pool_error', message: error.message }),
      ),
    );
  }
  async onModuleInit(): Promise<void> {
    const name = serviceName();
    const directory = join(process.cwd(), 'migrations');
    const files = (await readdir(directory))
      .filter((file) => file.startsWith(`${name}.`) && /^.+\.\d{3}\.sql$/.test(file))
      .sort((a, b) => a.localeCompare(b, 'en'));
    if (!files.length) throw new Error(`No migrations found for ${name}`);
    await this.transaction(async (client) => {
      await client.query('SELECT pg_advisory_xact_lock(hashtext($1))', [
        `marketplace-migrations-${name}`,
      ]);
      await client.query(
        'CREATE TABLE IF NOT EXISTS schema_migrations (version text PRIMARY KEY, checksum text NOT NULL, applied_at timestamptz NOT NULL DEFAULT now())',
      );
      for (const file of files) {
        const sql = await readFile(join(directory, file), 'utf8');
        const version = file.replace(/\.sql$/, '');
        const checksum = createHash('sha256').update(sql).digest('hex');
        const applied = await client.query(
          'SELECT checksum FROM schema_migrations WHERE version=$1',
          [version],
        );
        if (applied.rowCount) {
          if (applied.rows[0].checksum !== checksum)
            throw new Error(
              `Migration ${version} changed after application; create a new migration`,
            );
        } else {
          await client.query(sql);
          await client.query('INSERT INTO schema_migrations(version,checksum) VALUES($1,$2)', [
            version,
            checksum,
          ]);
        }
      }
    });
  }
  query<T extends QueryResultRow = QueryResultRow>(sql: string, values?: unknown[]) {
    return this.pool.query<T>(sql, values);
  }
  async transaction<T>(operation: (client: PoolClient) => Promise<T>): Promise<T> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      const result = await operation(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
  async onModuleDestroy(): Promise<void> {
    await this.pool.end();
  }
}
