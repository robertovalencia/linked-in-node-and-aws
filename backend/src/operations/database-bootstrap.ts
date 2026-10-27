import { Client } from 'pg';
import { pathToFileURL } from 'node:url';
import { databaseOptions } from '../common/connections.js';
import { required, SERVICES } from '../common/config.js';

const identifier = (value: string) => `"${value.replaceAll('"', '""')}"`;
const literal = (value: string) => `'${value.replaceAll("'", "''")}'`;
export async function bootstrapDatabases(client?: Client): Promise<void> {
  // Standalone one-shot task only. Normal capabilities never receive administrator credentials.
  const options = databaseOptions();
  if (!options.ssl) throw new Error('Database bootstrap requires verified TLS');
  const passwords = Object.fromEntries(
    SERVICES.map((service) => [service, required(`${service.toUpperCase()}_DB_PASSWORD`)]),
  );
  for (const password of Object.values(passwords)) {
    if (password.length < 32 || password.includes('\0'))
      throw new Error('Owned database passwords require at least 32 characters and no NUL');
  }
  const admin = client ?? new Client(options);
  await admin.connect();
  try {
    await admin.query('SELECT pg_advisory_lock(hashtext($1))', ['marketplace-database-bootstrap']);
    for (const service of SERVICES) {
      const exists = await admin.query('SELECT 1 FROM pg_roles WHERE rolname=$1', [service]);
      // SQL identifiers/literals are escaped; PostgreSQL does not accept bind parameters here.
      await admin.query(
        `${exists.rowCount ? 'ALTER' : 'CREATE'} ROLE ${identifier(service)} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION PASSWORD ${literal(passwords[service])}`,
      );
      const database = await admin.query(
        'SELECT pg_get_userbyid(datdba) AS owner FROM pg_database WHERE datname=$1',
        [service],
      );
      if (!database.rowCount)
        await admin.query(`CREATE DATABASE ${identifier(service)} OWNER ${identifier(service)}`);
      else if (database.rows[0].owner !== service)
        throw new Error(`Database ${service} has unexpected owner; manual review required`);
      await admin.query(`REVOKE ALL ON DATABASE ${identifier(service)} FROM PUBLIC`);
      await admin.query(
        `GRANT CONNECT, TEMPORARY ON DATABASE ${identifier(service)} TO ${identifier(service)}`,
      );
    }
  } finally {
    await admin.end();
  }
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  void bootstrapDatabases()
    .then(() => console.log('Service-owned databases bootstrapped'))
    .catch(() => {
      // SQL errors may include statements with password literals: never print the raw exception.
      console.error(
        'Database bootstrap failed; inspect DB connectivity/ownership using the recovery guide',
      );
      process.exitCode = 1;
    });
}
