# Inspected Node/backend source excerpts

Inspected 5 November 2026. These literal excerpts describe source, not a new deployment. Paths are repository-relative. Hashes bind the full inspected file; validators require current source to match. Absent-feature cards show a related boundary for contrast and label their external example separately.

<a id="source-nr01"></a>

## NR01 · backend/src/main.ts

Symbol: `const service = serviceName();`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  const service = serviceName();
  const controllers: Record<string, Type> = {
    identity: IdentityController,
    catalog: CatalogController,
```

<a id="source-nr02"></a>

## NR02 · backend/src/catalog/catalog.service.ts

Symbol: `const values: unknown[] = [];`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
    const values: unknown[] = [];
    const where: string[] = [];
    const add = (value: unknown) => {
      values.push(value);
```

<a id="source-nr03"></a>

## NR03 · backend/src/catalog/catalog.service.ts

Symbol: `const add = (value: unknown) => {`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
    const add = (value: unknown) => {
      values.push(value);
      return `$${values.length}`;
    };
```

<a id="source-nr04"></a>

## NR04 · backend/src/catalog/catalog.service.ts

Symbol: `const { ownerEmail, ...document } = entry;`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
        const { ownerEmail, ...document } = entry;
        providerSchema.parse(document);
        await client.query(
          'INSERT INTO providers(id,owner_email,document) VALUES($1,$2,$3) ON CONFLICT(id) DO NOTHING',
```

<a id="source-nr05"></a>

## NR05 · backend/src/identity/identity.service.ts

Symbol: `const valid = await verifyPassword`. Full-file SHA-256: `523e20fee146d919f357a86e0dacb858f1e077249662225affcbb28a86846756`.

```text
    const valid = await verifyPassword(password, account?.password_hash ?? this.dummyHash);
    if (!account || !valid) throw new UnauthorizedException('Invalid email or password');
    const actor: Actor = {
      id: account.email,
```

<a id="source-nr06"></a>

## NR06 · frontend/src/hooks/useMarketplace.ts

Symbol: `...new Set(`. Full-file SHA-256: `3b000e07303811f6cc73b1bdbef0635d65a159124102d956337e7f45a1757f72`.

```text
            ...new Set(
              saved.filter((id): id is string => typeof id === "string"),
            ),
          ].slice(0, 3)
```

<a id="source-nr07"></a>

## NR07 · backend/src/common/errors.ts

Symbol: `catch(error: unknown, host: ArgumentsHost): void {`. Full-file SHA-256: `2cfbad026cdde095f570ea7a2518f268a485e6e73a732a4bcf956d5f2bc99adb`.

```text
  catch(error: unknown, host: ArgumentsHost): void {
    const response = host.switchToHttp().getResponse<Response>();
    const parserStatus =
      typeof error === 'object' &&
```

<a id="source-nr08"></a>

## NR08 · backend/src/catalog/catalog.service.ts

Symbol: `async update(email: string, input: unknown): Promise<Provider> {`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
  async update(email: string, input: unknown): Promise<Provider> {
    const updated = providerSchema.parse(input);
    return this.db.transaction(async (client) => {
      const result = await client.query(
```

<a id="source-nr09"></a>

## NR09 · backend/src/common/config.ts

Symbol: `export const SERVICES =`. Full-file SHA-256: `c7b2d09a4fa511e0a218023b52e8790a77b290344ae1591ee58b73583bc9c590`.

```text
export const SERVICES = ['identity', 'catalog', 'inquiries', 'notifications'] as const;
export type ServiceName = (typeof SERVICES)[number];
export function serviceName(): ServiceName {
  const value = process.env.SERVICE;
```

<a id="source-nr10"></a>

## NR10 · frontend/src/services/http.ts

Symbol: `export async function api<T>(`. Full-file SHA-256: `519eadc524d706311cbf8fa2da42cf0b06f32bad8217cdb4978cd59cf45c276e`.

```text
export async function api<T>(
  path: string,
  auth: Auth | null = null,
  options: RequestInit = {},
```

<a id="source-nr11"></a>

## NR11 · backend/src/catalog/catalog.service.ts

Symbol: `constructor(private readonly db: Database) {}`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
  constructor(private readonly db: Database) {}
  async onApplicationBootstrap(): Promise<void> {
    if (process.env.SEED_DEMO !== 'true') return;
    const providers: (Provider & { ownerEmail: string })[] = JSON.parse(
```

<a id="source-nr12"></a>

## NR12 · backend/src/common/database.ts

Symbol: `import { serviceName } from './config.js';`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
import { serviceName } from './config.js';
import { databaseOptions } from './connections.js';

@Injectable()
```

<a id="source-nr13"></a>

## NR13 · backend/tsconfig.json

Symbol: `"emitDecoratorMetadata": true,`. Full-file SHA-256: `708bf96be02999b8ad14ab0879428e8ea132f30c171870faa38e2315a59be34f`.

```text
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
```

<a id="source-nr14"></a>

## NR14 · backend/src/identity/identity.service.ts

Symbol: `const result = await this.db.query(`. Full-file SHA-256: `523e20fee146d919f357a86e0dacb858f1e077249662225affcbb28a86846756`.

```text
    const result = await this.db.query(
      'SELECT email,name,role,password_hash FROM accounts WHERE email=$1',
      [email.toLowerCase()],
    );
```

<a id="source-nr15"></a>

## NR15 · backend/src/identity/password.ts

Symbol: `const scrypt = promisify(scryptCallback);`. Full-file SHA-256: `bb95c10f417f7ce36c3ca256fcfa5eec1cac26d20ce22ef055cf23279acc53ca`.

```text
const scrypt = promisify(scryptCallback);
export async function hashPassword(password: string): Promise<string> {
  const salt = randomBytes(16).toString('hex');
  const hash = (await scrypt(password, salt, 64)) as Buffer;
```

<a id="source-nr16"></a>

## NR16 · backend/src/identity/password.ts

Symbol: `const hash = (await scrypt(password, salt, 64)) as Buffer;`. Full-file SHA-256: `bb95c10f417f7ce36c3ca256fcfa5eec1cac26d20ce22ef055cf23279acc53ca`.

```text
  const hash = (await scrypt(password, salt, 64)) as Buffer;
  return `scrypt:${salt}:${hash.toString('hex')}`;
}
export async function verifyPassword(password: string, encoded: string): Promise<boolean> {
```

<a id="source-nr17"></a>

## NR17 · frontend/src/hooks/useMarketplace.ts

Symbol: `Promise.all(compare.map((id) => providerService.get(id, controller.signal)))`. Full-file SHA-256: `3b000e07303811f6cc73b1bdbef0635d65a159124102d956337e7f45a1757f72`.

```text
    Promise.all(compare.map((id) => providerService.get(id, controller.signal)))
      .then((items) => {
        if (!controller.signal.aborted) setCompareProviders(items);
      })
```

<a id="source-nr18"></a>

## NR18 · backend/src/common/messaging.ts

Symbol: `setTimeout(resolve, ms).unref();`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
    setTimeout(resolve, ms).unref();
  });

@Injectable()
```

<a id="source-nr19"></a>

## NR19 · backend/src/common/messaging.ts

Symbol: `const pause = (ms: number) =>`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
const pause = (ms: number) =>
  new Promise<void>((resolve) => {
    setTimeout(resolve, ms).unref();
  });
```

<a id="source-nr20"></a>

## NR20 · backend/src/common/messaging.ts

Symbol: `void this.run();`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
    void this.run();
  }
  async publishBatch(): Promise<void> {
    await this.db.transaction(async (client) => {
```

<a id="source-nr21"></a>

## NR21 · backend/src/common/connections.ts

Symbol: `max: 10,`. Full-file SHA-256: `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

```text
    max: 10,
    connectionTimeoutMillis: 5000,
    ssl: sslEnabled ? { rejectUnauthorized: true, ...(ca ? { ca } : {}) } : undefined,
  };
```

<a id="source-nr22"></a>

## NR22 · backend/src/common/database.ts

Symbol: `this.pool.on('error', (error: Error) =>`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
    this.pool.on('error', (error: Error) =>
      console.error(
        JSON.stringify({ level: 'error', event: 'database_pool_error', message: error.message }),
      ),
```

<a id="source-nr23"></a>

## NR23 · backend/src/main.ts

Symbol: `app.use(json({ limit: '128kb' }));`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  app.use(json({ limit: '128kb' }));
  app.useGlobalFilters(new ErrorFilter());
  app.enableShutdownHooks();
  const port = Number(process.env.PORT ?? 8181 + SERVICES.indexOf(service));
```

<a id="source-nr24"></a>

## NR24 · backend/src/common/config.ts

Symbol: `if (Buffer.byteLength(secret) < 32)`. Full-file SHA-256: `c7b2d09a4fa511e0a218023b52e8790a77b290344ae1591ee58b73583bc9c590`.

```text
  if (Buffer.byteLength(secret) < 32) throw new Error('JWT_SECRET requires at least 32 bytes');
  databaseOptions();
  if (['catalog', 'inquiries'].includes(service) && required('INTERNAL_API_KEY').length < 32)
    throw new Error('INTERNAL_API_KEY requires at least 32 characters');
```

<a id="source-nr25"></a>

## NR25 · backend/src/common/database.ts

Symbol: `const files = (await readdir(directory))`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
    const files = (await readdir(directory))
      .filter((file) => file.startsWith(`${name}.`) && /^.+\.\d{3}\.sql$/.test(file))
      .sort((a, b) => a.localeCompare(b, 'en'));
    if (!files.length) throw new Error(`No migrations found for ${name}`);
```

<a id="source-nr26"></a>

## NR26 · backend/src/common/database.ts

Symbol: `const directory = join(process.cwd(), 'migrations');`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
    const directory = join(process.cwd(), 'migrations');
    const files = (await readdir(directory))
      .filter((file) => file.startsWith(`${name}.`) && /^.+\.\d{3}\.sql$/.test(file))
      .sort((a, b) => a.localeCompare(b, 'en'));
```

<a id="source-nr27"></a>

## NR27 · backend/src/common/database.ts

Symbol: `const sql = await readFile(join(directory, file), 'utf8');`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
        const sql = await readFile(join(directory, file), 'utf8');
        const version = file.replace(/\.sql$/, '');
        const checksum = createHash('sha256').update(sql).digest('hex');
        const applied = await client.query(
```

<a id="source-nr28"></a>

## NR28 · backend/src/common/connections.ts

Symbol: `max: 10,`. Full-file SHA-256: `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

```text
    max: 10,
    connectionTimeoutMillis: 5000,
    ssl: sslEnabled ? { rejectUnauthorized: true, ...(ca ? { ca } : {}) } : undefined,
  };
```

<a id="source-nr29"></a>

## NR29 · backend/scripts/dev.mjs

Symbol: `const build = spawn(process.execPath,`. Full-file SHA-256: `06519c677969d389492988d4b884ecd4fd58bdf98064cc9aa89dd0c7b73e928f`.

```text
const build = spawn(process.execPath, [compiler, '--outDir', outDir], { stdio: 'inherit' });
const built = await new Promise((resolve) => build.on('exit', resolve));
if (built !== 0) process.exit(Number(built ?? 1));
const children = [
```

<a id="source-nr30"></a>

## NR30 · backend/scripts/dev.mjs

Symbol: `const build = spawn(process.execPath,`. Full-file SHA-256: `06519c677969d389492988d4b884ecd4fd58bdf98064cc9aa89dd0c7b73e928f`.

```text
const build = spawn(process.execPath, [compiler, '--outDir', outDir], { stdio: 'inherit' });
const built = await new Promise((resolve) => build.on('exit', resolve));
if (built !== 0) process.exit(Number(built ?? 1));
const children = [
```

<a id="source-nr31"></a>

## NR31 · backend/src/main.ts

Symbol: `app.enableShutdownHooks();`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  app.enableShutdownHooks();
  const port = Number(process.env.PORT ?? 8181 + SERVICES.indexOf(service));
  if (!Number.isInteger(port) || port < 1 || port > 65535)
    throw new Error('PORT must be a valid TCP port');
```

<a id="source-nr32"></a>

## NR32 · backend/src/main.ts

Symbol: `await app.listen(port,`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  await app.listen(port, '0.0.0.0');
}
void bootstrap().catch((error) => {
  console.error(error instanceof Error ? error.stack : error);
```

<a id="source-nr33"></a>

## NR33 · backend/src/common/errors.ts

Symbol: `private readonly logger = new Logger('HttpErrors');`. Full-file SHA-256: `2cfbad026cdde095f570ea7a2518f268a485e6e73a732a4bcf956d5f2bc99adb`.

```text
  private readonly logger = new Logger('HttpErrors');
  catch(error: unknown, host: ArgumentsHost): void {
    const response = host.switchToHttp().getResponse<Response>();
    const parserStatus =
```

<a id="source-nr34"></a>

## NR34 · backend/src/inquiries/inquiries.service.ts

Symbol: `signal: AbortSignal.timeout(5000),`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
          signal: AbortSignal.timeout(5000),
        },
      );
    } catch {
```

<a id="source-nr35"></a>

## NR35 · backend/src/common/errors.ts

Symbol: `private readonly logger = new Logger('HttpErrors');`. Full-file SHA-256: `2cfbad026cdde095f570ea7a2518f268a485e6e73a732a4bcf956d5f2bc99adb`.

```text
  private readonly logger = new Logger('HttpErrors');
  catch(error: unknown, host: ArgumentsHost): void {
    const response = host.switchToHttp().getResponse<Response>();
    const parserStatus =
```

<a id="source-nr36"></a>

## NR36 · backend/src/catalog/catalog.service.ts

Symbol: `const providers: (Provider & { ownerEmail: string })[] = JSON.parse(`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
    const providers: (Provider & { ownerEmail: string })[] = JSON.parse(
      await readFile(join(process.cwd(), 'seeds/providers.json'), 'utf8'),
    );
    await this.db.transaction(async (client) => {
```

<a id="source-nr37"></a>

## NR37 · backend/src/common/database.ts

Symbol: `.filter((file) => file.startsWith(`${name}.`) && /^.+\.\d{3}\.sql$/.test(file))`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
      .filter((file) => file.startsWith(`${name}.`) && /^.+\.\d{3}\.sql$/.test(file))
      .sort((a, b) => a.localeCompare(b, 'en'));
    if (!files.length) throw new Error(`No migrations found for ${name}`);
    await this.transaction(async (client) => {
```

<a id="source-nr38"></a>

## NR38 · backend/src/inquiries/inquiries.service.ts

Symbol: `createdAt: new Date(row.created_at).toISOString(),`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
    createdAt: new Date(row.created_at).toISOString(),
  };
}
@Injectable()
```

<a id="source-nr39"></a>

## NR39 · backend/src/common/config.ts

Symbol: `const catalog = new URL(required('CATALOG_URL'));`. Full-file SHA-256: `c7b2d09a4fa511e0a218023b52e8790a77b290344ae1591ee58b73583bc9c590`.

```text
    const catalog = new URL(required('CATALOG_URL'));
    if (!['http:', 'https:'].includes(catalog.protocol))
      throw new Error('CATALOG_URL must use HTTP or HTTPS');
  }
```

<a id="source-nr40"></a>

## NR40 · backend/src/main.ts

Symbol: `const controllers: Record<string, Type> = {`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  const controllers: Record<string, Type> = {
    identity: IdentityController,
    catalog: CatalogController,
    inquiries: InquiriesController,
```

<a id="source-nr41"></a>

## NR41 · frontend/src/services/http.ts

Symbol: `import type { Auth }`. Full-file SHA-256: `519eadc524d706311cbf8fa2da42cf0b06f32bad8217cdb4978cd59cf45c276e`.

```text
import type { Auth } from "../types/marketplace";
export class ApiError extends Error {
  constructor(
    message: string,
```

<a id="source-nr42"></a>

## NR42 · scripts/dev.mjs

Symbol: `const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');`. Full-file SHA-256: `d9dc9b4664d5db3caff38adc32e429f81c5abe6b9638b4aeb5739518bb439d1d`.

```text
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const secrets=Object.fromEntries(readFileSync(resolve(root,'.env'),'utf8').split('\n').filter(l=>l&&!l.startsWith('#')).map(l=>{const i=l.indexOf('=');return [l.slice(0,i),l.slice(i+1)];}));
const children=[];
for (const [index,service] of ['identity','catalog','inquiries','notifications'].entries()) {
```

<a id="source-nr43"></a>

## NR43 · backend/src/catalog/catalog.service.ts

Symbol: `const add =`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
    const where: string[] = [];
    const add = (value: unknown) => {
      values.push(value);
      return `$${values.length}`;
    };
```

<a id="source-nri01"></a>

## NRI01 · backend/src/common/database.ts

Symbol: `import { serviceName } from './config.js';`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
import { serviceName } from './config.js';
import { databaseOptions } from './connections.js';

@Injectable()
```

<a id="source-nri02"></a>

## NRI02 · backend/src/common/database.ts

Symbol: `const directory = join(process.cwd(), 'migrations');`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
    const directory = join(process.cwd(), 'migrations');
    const files = (await readdir(directory))
      .filter((file) => file.startsWith(`${name}.`) && /^.+\.\d{3}\.sql$/.test(file))
      .sort((a, b) => a.localeCompare(b, 'en'));
```

<a id="source-nri03"></a>

## NRI03 · backend/src/identity/password.ts

Symbol: `const hash = (await scrypt(password, salt, 64)) as Buffer;`. Full-file SHA-256: `bb95c10f417f7ce36c3ca256fcfa5eec1cac26d20ce22ef055cf23279acc53ca`.

```text
  const hash = (await scrypt(password, salt, 64)) as Buffer;
  return `scrypt:${salt}:${hash.toString('hex')}`;
}
export async function verifyPassword(password: string, encoded: string): Promise<boolean> {
```

<a id="source-nri04"></a>

## NRI04 · backend/src/common/messaging.ts

Symbol: `void this.run();`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
    void this.run();
  }
  async publishBatch(): Promise<void> {
    await this.db.transaction(async (client) => {
```

<a id="source-nri05"></a>

## NRI05 · backend/scripts/dev.mjs

Symbol: `const build = spawn(process.execPath,`. Full-file SHA-256: `06519c677969d389492988d4b884ecd4fd58bdf98064cc9aa89dd0c7b73e928f`.

```text
const build = spawn(process.execPath, [compiler, '--outDir', outDir], { stdio: 'inherit' });
const built = await new Promise((resolve) => build.on('exit', resolve));
if (built !== 0) process.exit(Number(built ?? 1));
const children = [
```

<a id="source-nri06"></a>

## NRI06 · backend/src/main.ts

Symbol: `app.enableShutdownHooks();`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  app.enableShutdownHooks();
  const port = Number(process.env.PORT ?? 8181 + SERVICES.indexOf(service));
  if (!Number.isInteger(port) || port < 1 || port > 65535)
    throw new Error('PORT must be a valid TCP port');
```

<a id="source-ns01"></a>

## NS01 · backend/src/main.ts

Symbol: `@Module({`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  };
  @Module({
    controllers: [HealthController, controllers[service]],
    providers: [Database, AuthGuard, WorkerHealth, ...providers[service]],
  })
```

<a id="source-ns02"></a>

## NS02 · backend/src/catalog/catalog.service.ts

Symbol: `constructor(private readonly db: Database)`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
export class CatalogService implements OnApplicationBootstrap {
  constructor(private readonly db: Database) {}
  async onApplicationBootstrap(): Promise<void> {
    if (process.env.SEED_DEMO !== 'true') return;
    const providers: (Provider & { ownerEmail: string })[] = JSON.parse(
```

<a id="source-ns03"></a>

## NS03 · backend/src/catalog/catalog.controller.ts

Symbol: `@Get('api/providers/me')`. Full-file SHA-256: `8b36a72ed7b2b6cfe7484e8bcebe73582108f154f40cefe5e99d1dec9312e84c`.

```text
  }
  @Get('api/providers/me') @UseGuards(AuthGuard) mine(@Req() request: AuthRequest) {
    requireRole(request.actor, 'PROVIDER');
    return this.catalog.mine(request.actor.email);
  }
```

<a id="source-ns04"></a>

## NS04 · backend/src/identity/identity.service.ts

Symbol: `async onApplicationBootstrap()`. Full-file SHA-256: `523e20fee146d919f357a86e0dacb858f1e077249662225affcbb28a86846756`.

```text
  constructor(private readonly db: Database) {}
  async onApplicationBootstrap(): Promise<void> {
    this.dummyHash = await hashPassword('dummy-password-never-used');
    if (process.env.SEED_DEMO !== 'true') return;
    const providers: { ownerEmail: string; name: string }[] = JSON.parse(
```

<a id="source-ns05"></a>

## NS05 · backend/src/main.ts

Symbol: `app.use(json({ limit: '128kb' }));`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  app.use(helmet());
  app.use(json({ limit: '128kb' }));
  app.useGlobalFilters(new ErrorFilter());
  app.enableShutdownHooks();
  const port = Number(process.env.PORT ?? 8181 + SERVICES.indexOf(service));
```

<a id="source-ns06"></a>

## NS06 · backend/src/common/errors.ts

Symbol: `error instanceof ZodError`. Full-file SHA-256: `2cfbad026cdde095f570ea7a2518f268a485e6e73a732a4bcf956d5f2bc99adb`.

```text
    const status =
      error instanceof ZodError
        ? 400
        : error instanceof HttpException
          ? error.getStatus()
```

<a id="source-ns07"></a>

## NS07 · backend/package.json

Symbol: `"rxjs"`. Full-file SHA-256: `b22b09f975bd55e53ffb60eca9ff9b031d310426e8a20dd072b7b298e55559da`.

```text
    "reflect-metadata": "^0.2.2",
    "rxjs": "^7.8.2",
    "zod": "^4.1.0"
  },
  "devDependencies": {
```

<a id="source-ns08"></a>

## NS08 · backend/src/inquiries/inquiries.service.ts

Symbol: `const input = inquirySchema.parse(body);`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
      );
    const input = inquirySchema.parse(body);
    const hash = fingerprint(input);
    return this.db.transaction(async (client) => {
      // The transaction-scoped lock serializes the same client/key across every replica.
```

<a id="source-ns09"></a>

## NS09 · backend/src/catalog/provider.schema.ts

Symbol: `.enum(['true', 'false'])`. Full-file SHA-256: `c3cead76e4b957e722c8e9245bf4d0dd1c822990ed731dc82baf46060c222cdf`.

```text
    available: z
      .enum(['true', 'false'])
      .transform((v) => v === 'true')
      .optional(),
    sort: z.enum(['recommended', 'rate-asc', 'rating']).default('recommended'),
```

<a id="source-ns10"></a>

## NS10 · backend/src/catalog/provider.schema.ts

Symbol: `export type Provider = z.infer<typeof providerSchema>;`. Full-file SHA-256: `c3cead76e4b957e722c8e9245bf4d0dd1c822990ed731dc82baf46060c222cdf`.

```text
  .strict();
export type Provider = z.infer<typeof providerSchema>;
export const searchSchema = z
  .object({
    q: z.string().max(200).optional(),
```

<a id="source-ns11"></a>

## NS11 · backend/src/catalog/catalog.service.ts

Symbol: `const add = (value: unknown) => {`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
    const where: string[] = [];
    const add = (value: unknown) => {
      values.push(value);
      return `$${values.length}`;
    };
```

<a id="source-ns12"></a>

## NS12 · backend/src/catalog/catalog.service.ts

Symbol: `(document->>'hourlyRate')::numeric`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
    if (query.maxRate !== undefined)
      where.push(`(document->>'hourlyRate')::numeric<=${add(query.maxRate)}`);
    if (query.available !== undefined)
      where.push(`(document->>'available')::boolean=${add(query.available)}`);
    const condition = where.length ? `WHERE ${where.join(' AND ')}` : '';
```

<a id="source-ns13"></a>

## NS13 · backend/src/catalog/catalog.service.ts

Symbol: `WITH filtered AS`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
    const result = await this.db.query(
      `WITH filtered AS (SELECT id,document FROM providers ${condition}) SELECT (SELECT count(*)::int FROM filtered) AS total, COALESCE((SELECT jsonb_agg(page.document ORDER BY page.ordinal) FROM (SELECT document,row_number() OVER (ORDER BY ${order}) ordinal FROM filtered ORDER BY ${order} LIMIT ${add(query.size)} OFFSET ${add(query.page * query.size)}) page),'[]'::jsonb) AS items`,
      values,
    );
    return result.rows[0];
```

<a id="source-ns14"></a>

## NS14 · backend/src/catalog/catalog.service.ts

Symbol: `rating: row.document.rating,`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
        ...updated,
        rating: row.document.rating,
        reviewCount: row.document.reviewCount,
        completedProjects: row.document.completedProjects,
      };
```

<a id="source-ns15"></a>

## NS15 · backend/src/common/connections.ts

Symbol: `max: 10,`. Full-file SHA-256: `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

```text
    ...connection,
    max: 10,
    connectionTimeoutMillis: 5000,
    ssl: sslEnabled ? { rejectUnauthorized: true, ...(ca ? { ca } : {}) } : undefined,
  };
```

<a id="source-ns16"></a>

## NS16 · backend/src/common/database.ts

Symbol: `const client = await this.pool.connect();`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
  async transaction<T>(operation: (client: PoolClient) => Promise<T>): Promise<T> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      const result = await operation(client);
```

<a id="source-ns17"></a>

## NS17 · backend/src/inquiries/inquiries.service.ts

Symbol: `budget: Number(row.budget),`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
    message: row.message,
    budget: Number(row.budget),
    clientType: row.client_type,
    status: row.status,
    createdAt: new Date(row.created_at).toISOString(),
```

<a id="source-ns18"></a>

## NS18 · backend/src/inquiries/inquiries.service.ts

Symbol: `SELECT pg_advisory_xact_lock(hashtextextended($1,0))`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
      // The transaction-scoped lock serializes the same client/key across every replica.
      await client.query('SELECT pg_advisory_xact_lock(hashtextextended($1,0))', [
        JSON.stringify([actor.email, key]),
      ]);
      const previous = await client.query(
```

<a id="source-ns19"></a>

## NS19 · backend/src/common/database.ts

Symbol: `await client.query('BEGIN');`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
    try {
      await client.query('BEGIN');
      const result = await operation(client);
      await client.query('COMMIT');
      return result;
```

<a id="source-ns20"></a>

## NS20 · backend/src/common/database.ts

Symbol: `Migration ${version} changed after application`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
            throw new Error(
              `Migration ${version} changed after application; create a new migration`,
            );
        } else {
          await client.query(sql);
```

<a id="source-ns21"></a>

## NS21 · backend/src/common/connections.ts

Symbol: `rejectUnauthorized: true`. Full-file SHA-256: `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

```text
    connectionTimeoutMillis: 5000,
    ssl: sslEnabled ? { rejectUnauthorized: true, ...(ca ? { ca } : {}) } : undefined,
  };
}
export function kafkaOptions(): KafkaConfig {
```

<a id="source-ns22"></a>

## NS22 · backend/src/identity/password.ts

Symbol: `const scrypt = promisify(scryptCallback);`. Full-file SHA-256: `bb95c10f417f7ce36c3ca256fcfa5eec1cac26d20ce22ef055cf23279acc53ca`.

```text
import { promisify } from 'node:util';
const scrypt = promisify(scryptCallback);
export async function hashPassword(password: string): Promise<string> {
  const salt = randomBytes(16).toString('hex');
  const hash = (await scrypt(password, salt, 64)) as Buffer;
```

<a id="source-ns23"></a>

## NS23 · backend/src/identity/password.ts

Symbol: `const salt = randomBytes(16).toString('hex');`. Full-file SHA-256: `bb95c10f417f7ce36c3ca256fcfa5eec1cac26d20ce22ef055cf23279acc53ca`.

```text
export async function hashPassword(password: string): Promise<string> {
  const salt = randomBytes(16).toString('hex');
  const hash = (await scrypt(password, salt, 64)) as Buffer;
  return `scrypt:${salt}:${hash.toString('hex')}`;
}
```

<a id="source-ns24"></a>

## NS24 · backend/src/identity/password.ts

Symbol: `return timingSafeEqual(candidate, Buffer.from(hash, 'hex'));`. Full-file SHA-256: `bb95c10f417f7ce36c3ca256fcfa5eec1cac26d20ce22ef055cf23279acc53ca`.

```text
  const candidate = (await scrypt(password, salt, 64)) as Buffer;
  return timingSafeEqual(candidate, Buffer.from(hash, 'hex'));
}
```

<a id="source-ns25"></a>

## NS25 · backend/src/common/auth.ts

Symbol: `algorithm: 'HS256'`. Full-file SHA-256: `88f5ed7fab96d3c14878b048c4042a8222e825997ab451ddd8965b258d715d71`.

```text
  return jwt.sign(actor, required('JWT_SECRET'), {
    algorithm: 'HS256',
    issuer: 'marketplace',
    audience: 'marketplace',
    subject: actor.email,
```

<a id="source-ns26"></a>

## NS26 · backend/src/common/auth.ts

Symbol: `algorithms: ['HS256']`. Full-file SHA-256: `88f5ed7fab96d3c14878b048c4042a8222e825997ab451ddd8965b258d715d71`.

```text
    const value = jwt.verify(token, required('JWT_SECRET'), {
      algorithms: ['HS256'],
      issuer: 'marketplace',
      audience: 'marketplace',
    });
```

<a id="source-ns27"></a>

## NS27 · backend/src/notifications/notifications.service.ts

Symbol: `if (row.recipient_email !== actor.email)`. Full-file SHA-256: `d4eabfe0f00dc4f96da55b4864c937c6b630f332b1eb928725b4888236a07eae`.

```text
      if (!row) throw new NotFoundException('Notification not found');
      if (row.recipient_email !== actor.email)
        throw new ForbiddenException('Notification belongs to another account');
      const updated = await client.query(
        'UPDATE notifications SET read=true WHERE id=$1 RETURNING *',
```

<a id="source-ns28"></a>

## NS28 · backend/src/identity/identity.controller.ts

Symbol: `private readonly attempts = new Map`. Full-file SHA-256: `0f2520bb6f64bd56e107efadfeda0bcd44182f5d695e53b9a3ce93fad0514ce2`.

```text
  // Per-process throttle protects password hashing; the private AWS dev environment has no additional ingress rate rule.
  private readonly attempts = new Map<string, { count: number; until: number }>();
  constructor(private readonly identity: IdentityService) {}
  @Post('login') @HttpCode(200) async login(@Body() body: unknown, @Req() request: Request) {
    const now = Date.now();
```

<a id="source-ns29"></a>

## NS29 · backend/src/inquiries/inquiries.service.ts

Symbol: `if (!response.ok)`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
    if (response.status === 404) throw new NotFoundException('Provider not found');
    if (!response.ok) throw new ServiceUnavailableException('Catalog lookup failed');
    try {
      return z
        .object({ id: z.string(), ownerEmail: z.email(), name: z.string() })
```

<a id="source-ns30"></a>

## NS30 · backend/src/inquiries/inquiries.service.ts

Symbol: `signal: AbortSignal.timeout(5000),`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
          headers: { 'X-Internal-Key': required('INTERNAL_API_KEY') },
          signal: AbortSignal.timeout(5000),
        },
      );
    } catch {
```

<a id="source-ns31"></a>

## NS31 · backend/src/inquiries/inquiries.service.ts

Symbol: `export function fingerprint(input: CreateInquiry): string {`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
import { inquirySchema, statusSchema, CreateInquiry } from './inquiry.schema.js';
export function fingerprint(input: CreateInquiry): string {
  return createHash('sha256')
    .update(
      JSON.stringify([
```

<a id="source-ns32"></a>

## NS32 · backend/src/inquiries/inquiries.service.ts

Symbol: `const eventId = randomUUID();`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
      const id = randomUUID();
      const eventId = randomUUID();
      const createdAt = new Date().toISOString();
      const inserted = await client.query(
        'INSERT INTO inquiries(id,provider_id,provider_email,provider_name,client_email,client_name,subject,message,budget,client_type,created_at,idempotency_key,request_hash) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13) RETURNING *',
```

<a id="source-ns33"></a>

## NS33 · backend/src/inquiries/inquiries.service.ts

Symbol: `INSERT INTO outbox(event_id,inquiry_id,payload)`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
      };
      await client.query('INSERT INTO outbox(event_id,inquiry_id,payload) VALUES($1,$2,$3)', [
        eventId,
        id,
        event,
```

<a id="source-ns34"></a>

## NS34 · backend/src/inquiries/inquiries.service.ts

Symbol: `if (row.status !== 'PENDING' && row.status !== input.status)`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
        throw new ForbiddenException('Inquiry belongs to another provider');
      if (row.status !== 'PENDING' && row.status !== input.status)
        throw new ConflictException('Inquiry already resolved');
      const updated = await client.query('UPDATE inquiries SET status=$1 WHERE id=$2 RETURNING *', [
        input.status,
```

<a id="source-ns35"></a>

## NS35 · backend/src/common/messaging.ts

Symbol: `groupId: 'marketplace-notifications-v1'`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
        this.consumer = kafka().consumer({
          groupId: 'marketplace-notifications-v1',
          allowAutoTopicCreation: process.env.DEPLOYMENT_MODE !== 'aws-ecs',
          retry: { retries: 5 },
        });
```

<a id="source-ns36"></a>

## NS36 · backend/src/common/messaging.ts

Symbol: `acks: -1,`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
          topic: process.env.KAFKA_TOPIC ?? INQUIRY_TOPIC,
          acks: -1,
          messages: [{ key: event.inquiry_id, value: JSON.stringify(event.payload) }],
        });
        await client.query('UPDATE outbox SET published_at=now() WHERE event_id=$1', [
```

<a id="source-ns37"></a>

## NS37 · backend/src/common/messaging.ts

Symbol: `LIMIT 25 FOR UPDATE SKIP LOCKED`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
      const pending = await client.query(
        'SELECT event_id,inquiry_id,payload FROM outbox WHERE published_at IS NULL ORDER BY created_at LIMIT 25 FOR UPDATE SKIP LOCKED',
      );
      for (const event of pending.rows) {
        await this.producer!.send({
```

<a id="source-ns38"></a>

## NS38 · backend/src/common/messaging.ts

Symbol: `fromBeginning: true,`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
          topic: process.env.KAFKA_TOPIC ?? INQUIRY_TOPIC,
          fromBeginning: true,
        });
        await this.consumer.run({
          eachMessage: async ({ message }) => {
```

<a id="source-ns39"></a>

## NS39 · backend/src/common/messaging.ts

Symbol: `await this.notifications.consume(JSON.parse(message.value.toString('utf8')));`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
            // Await durable insert before KafkaJS acknowledges the offset. Replays are deduplicated in SQL.
            await this.notifications.consume(JSON.parse(message.value.toString('utf8')));
          },
        });
        // KafkaJS runs processing in the background; retain the connection until shutdown.
```

<a id="source-ns40"></a>

## NS40 · backend/src/notifications/notifications.service.ts

Symbol: `ON CONFLICT(event_id) DO NOTHING`. Full-file SHA-256: `d4eabfe0f00dc4f96da55b4864c937c6b630f332b1eb928725b4888236a07eae`.

```text
    await this.db.query(
      'INSERT INTO notifications(id,event_id,inquiry_id,recipient_email,message,created_at) VALUES($1,$2,$3,$4,$5,$6) ON CONFLICT(event_id) DO NOTHING',
      [
        randomUUID(),
        event.eventId,
```

<a id="source-ns41"></a>

## NS41 · backend/src/common/messaging.ts

Symbol: `void this.run();`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
  onApplicationBootstrap(): void {
    void this.run();
  }
  async publishBatch(): Promise<void> {
    await this.db.transaction(async (client) => {
```

<a id="source-ns42"></a>

## NS42 · backend/src/common/messaging.ts

Symbol: `this.consumer.events.GROUP_JOIN`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
        });
        this.consumer.on(this.consumer.events.GROUP_JOIN, () => {
          this.health.ready = true;
        });
        this.consumer.on(this.consumer.events.DISCONNECT, () => {
```

<a id="source-ns43"></a>

## NS43 · backend/src/common/health.ts

Symbol: `@Get('health/serve')`. Full-file SHA-256: `2941f0c699974fd0f6e27c82200cd617693eae335afdd4710066eb3fadf4c5b8`.

```text
  // Routing readiness preserves durable inquiry writes while Kafka retries asynchronously.
  @Get('health/serve') async serving() {
    try {
      await this.db.query('SELECT 1');
    } catch {
```

<a id="source-ns44"></a>

## NS44 · backend/src/main.ts

Symbol: `const providers: Record<string, Type[]> = {`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  };
  const providers: Record<string, Type[]> = {
    identity: [IdentityService],
    catalog: [CatalogService],
    inquiries: [InquiriesService, OutboxPublisher],
```

<a id="source-ns45"></a>

## NS45 · backend/src/catalog/catalog.service.ts

Symbol: `WHERE owner_email=$1 FOR UPDATE`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
      const result = await client.query(
        'SELECT id,document FROM providers WHERE owner_email=$1 FOR UPDATE',
        [email],
      );
      const row = result.rows[0];
```

<a id="source-ns46"></a>

## NS46 · backend/src/main.ts

Symbol: `app.use(helmet());`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  });
  app.use(helmet());
  app.use(json({ limit: '128kb' }));
  app.useGlobalFilters(new ErrorFilter());
  app.enableShutdownHooks();
```

<a id="source-ns47"></a>

## NS47 · backend/src/common/auth.ts

Symbol: `expiresIn: '1h'`. Full-file SHA-256: `88f5ed7fab96d3c14878b048c4042a8222e825997ab451ddd8965b258d715d71`.

```text
    subject: actor.email,
    expiresIn: '1h',
  });
}
export function verifyActor(token: string): Actor {
```

<a id="source-ns48"></a>

## NS48 · backend/src/main.ts

Symbol: `app.enableShutdownHooks();`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  app.useGlobalFilters(new ErrorFilter());
  app.enableShutdownHooks();
  const port = Number(process.env.PORT ?? 8181 + SERVICES.indexOf(service));
  if (!Number.isInteger(port) || port < 1 || port > 65535)
    throw new Error('PORT must be a valid TCP port');
```

<a id="source-ns49"></a>

## NS49 · backend/src/common/errors.ts

Symbol: `this.logger.error(error instanceof Error ? error.stack : String(error))`. Full-file SHA-256: `2cfbad026cdde095f570ea7a2518f268a485e6e73a732a4bcf956d5f2bc99adb`.

```text
          : (error as Error).message;
    if (status === 500) this.logger.error(error instanceof Error ? error.stack : String(error));
    if (detail.length > 1500) detail = detail.slice(0, 1500);
    response.status(status).json({ status, detail });
  }
```

<a id="source-ns50"></a>

## NS50 · backend/src/main.ts

Symbol: `app.useGlobalFilters(new ErrorFilter());`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  app.use(json({ limit: '128kb' }));
  app.useGlobalFilters(new ErrorFilter());
  app.enableShutdownHooks();
  const port = Number(process.env.PORT ?? 8181 + SERVICES.indexOf(service));
  if (!Number.isInteger(port) || port < 1 || port > 65535)
```

<a id="source-ns51"></a>

## NS51 · backend/src/common/config.ts

Symbol: `export function validateConfig(): void {`. Full-file SHA-256: `c7b2d09a4fa511e0a218023b52e8790a77b290344ae1591ee58b73583bc9c590`.

```text
}
export function validateConfig(): void {
  const service = serviceName();
  const secret = required('JWT_SECRET');
  if (Buffer.byteLength(secret) < 32) throw new Error('JWT_SECRET requires at least 32 bytes');
```

<a id="source-ns52"></a>

## NS52 · backend/package.json

Symbol: `"pg"`. Full-file SHA-256: `b22b09f975bd55e53ffb60eca9ff9b031d310426e8a20dd072b7b298e55559da`.

```text
    "kafkajs": "^2.2.4",
    "pg": "^8.16.0",
    "reflect-metadata": "^0.2.2",
    "rxjs": "^7.8.2",
    "zod": "^4.1.0"
```

<a id="source-ns53"></a>

## NS53 · backend/src/common/auth.ts

Symbol: `export class AuthGuard implements CanActivate {`. Full-file SHA-256: `88f5ed7fab96d3c14878b048c4042a8222e825997ab451ddd8965b258d715d71`.

```text
@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest<AuthRequest>();
    const authorization = request.headers.authorization;
```

<a id="source-ns54"></a>

## NS54 · backend/package.json

Symbol: `"zod"`. Full-file SHA-256: `b22b09f975bd55e53ffb60eca9ff9b031d310426e8a20dd072b7b298e55559da`.

```text
    "rxjs": "^7.8.2",
    "zod": "^4.1.0"
  },
  "devDependencies": {
    "@eslint/js": "^10.0.1",
```

<a id="source-nsi01"></a>

## NSI01 · backend/src/common/auth.ts

Symbol: `throw new UnauthorizedException('Invalid or expired bearer token');`. Full-file SHA-256: `88f5ed7fab96d3c14878b048c4042a8222e825997ab451ddd8965b258d715d71`.

```text
  } catch {
    throw new UnauthorizedException('Invalid or expired bearer token');
  }
}
@Injectable()
```

<a id="source-nsi02"></a>

## NSI02 · backend/src/catalog/provider.schema.ts

Symbol: `.enum(['true', 'false'])`. Full-file SHA-256: `c3cead76e4b957e722c8e9245bf4d0dd1c822990ed731dc82baf46060c222cdf`.

```text
    available: z
      .enum(['true', 'false'])
      .transform((v) => v === 'true')
      .optional(),
    sort: z.enum(['recommended', 'rate-asc', 'rating']).default('recommended'),
```

<a id="source-nsi03"></a>

## NSI03 · backend/src/common/database.ts

Symbol: `client.release();`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
    } finally {
      client.release();
    }
  }
  async onModuleDestroy(): Promise<void> {
```

<a id="source-nsi04"></a>

## NSI04 · backend/src/common/database.ts

Symbol: `changed after application; create a new migration`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
            throw new Error(
              `Migration ${version} changed after application; create a new migration`,
            );
        } else {
          await client.query(sql);
```

<a id="source-nsi05"></a>

## NSI05 · backend/src/inquiries/inquiries.service.ts

Symbol: `Idempotency key already used for a different inquiry`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
        if (previous.rows[0].request_hash !== hash)
          throw new ConflictException('Idempotency key already used for a different inquiry');
        return inquiryView(previous.rows[0]);
      }
      const target = await this.provider(input.providerId);
```

<a id="source-nsi06"></a>

## NSI06 · backend/src/common/messaging.ts

Symbol: `UPDATE outbox SET published_at=now()`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
        });
        await client.query('UPDATE outbox SET published_at=now() WHERE event_id=$1', [
          event.event_id,
        ]);
      }
```

<a id="source-nsi07"></a>

## NSI07 · backend/src/common/messaging.ts

Symbol: `throw new Error('Event payload missing; offset is not acknowledged');`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
            if (!message.value)
              throw new Error('Event payload missing; offset is not acknowledged');
            // Await durable insert before KafkaJS acknowledges the offset. Replays are deduplicated in SQL.
            await this.notifications.consume(JSON.parse(message.value.toString('utf8')));
          },
```

<a id="source-nsi08"></a>

## NSI08 · backend/src/common/connections.ts

Symbol: `DB_URL ssl parameters`. Full-file SHA-256: `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

```text
    if ([...url.searchParams.keys()].some((key) => key.toLowerCase().startsWith('ssl')))
      throw new Error('Use DB_SSL and its CA settings instead of DB_URL ssl parameters');
    connection = { connectionString: process.env.DB_URL };
  } else {
    const port = Number(process.env.DB_PORT ?? '5432');
```

<a id="source-nsi09"></a>

## NSI09 · backend/src/identity/identity.controller.ts

Symbol: `const key = request.ip ?? 'unknown';`. Full-file SHA-256: `0f2520bb6f64bd56e107efadfeda0bcd44182f5d695e53b9a3ce93fad0514ce2`.

```text
    for (const [key, value] of this.attempts) if (value.until <= now) this.attempts.delete(key);
    const key = request.ip ?? 'unknown';
    const attempts = this.attempts.get(key) ?? { count: 0, until: now + 60_000 };
    if (++attempts.count > 30)
      throw new HttpException('Too many login attempts; retry in one minute', 429);
```

<a id="source-no01"></a>

## NO01 · backend/package.json

Symbol: `"node":`. Full-file SHA-256: `b22b09f975bd55e53ffb60eca9ff9b031d310426e8a20dd072b7b298e55559da`.

```text
  "engines": {
    "node": ">=22 <25"
  },
  "scripts": {
    "build": "tsc -p tsconfig.json",
```

<a id="source-no02"></a>

## NO02 · package.json

Symbol: `"check":`. Full-file SHA-256: `d680dbdf10b38324c8099c83ddc3f2b3a0cb45f49b049aaf5aac77edcacf1d34`.

```text
    "dev": "node scripts/dev.mjs",
    "check": "npm --prefix backend run check && npm --prefix frontend run check",
    "test": "npm --prefix backend test && npm --prefix frontend test",
    "build": "npm --prefix backend run build && npm --prefix frontend run build",
    "acceptance": "node scripts/acceptance.mjs http://localhost:8180 docs/evidence/local-acceptance.json",
```

<a id="source-no03"></a>

## NO03 · scripts/local.sh

Symbol: `up) docker compose`. Full-file SHA-256: `87bdc30924dc44be17f2e6a3d389c9170a5118dd99c6294fd69ed956d9b3fe9e`.

```text
case "${1:-up}" in
  up) docker compose up -d --build --wait --wait-timeout 240; echo 'Marketplace: http://localhost:8180' ;;
  deps) docker compose up -d --wait postgres kafka ;;
  down) docker compose down ;;
  logs) docker compose logs --tail=150 -f "${@:2}" ;;
```

<a id="source-no04"></a>

## NO04 · backend/scripts/dev.mjs

Symbol: `const outDir =`. Full-file SHA-256: `06519c677969d389492988d4b884ecd4fd58bdf98064cc9aa89dd0c7b73e928f`.

```text
}
const outDir = `dist-dev/${service}`;
const compiler = 'node_modules/typescript/bin/tsc';
const build = spawn(process.execPath, [compiler, '--outDir', outDir], { stdio: 'inherit' });
const built = await new Promise((resolve) => build.on('exit', resolve));
```

<a id="source-no05"></a>

## NO05 · compose.yaml

Symbol: `name: linked-in-node-local`. Full-file SHA-256: `4041fec31b19574a77777564085c3041cea86059684edd71b5d4f7d0f491ed7c`.

```text
name: linked-in-node-local
x-node: &node
  image: linked-in-node/backend:local
  build: ./backend
```

<a id="source-no06"></a>

## NO06 · backend/src/common/config.ts

Symbol: `export function validateConfig`. Full-file SHA-256: `c7b2d09a4fa511e0a218023b52e8790a77b290344ae1591ee58b73583bc9c590`.

```text
}
export function validateConfig(): void {
  const service = serviceName();
  const secret = required('JWT_SECRET');
  if (Buffer.byteLength(secret) < 32) throw new Error('JWT_SECRET requires at least 32 bytes');
```

<a id="source-no07"></a>

## NO07 · backend/Dockerfile

Symbol: `COPY --chown=node:node migrations`. Full-file SHA-256: `f6e27129a553a36ab16b821dc34f1667fd42a6a40d21e526261b5b3e0c4051a7`.

```text
COPY --chown=node:node certs ./certs
COPY --chown=node:node migrations ./migrations
COPY --chown=node:node seeds ./seeds
COPY --chown=node:node package.json ./
USER node
```

<a id="source-no08"></a>

## NO08 · backend/src/main.ts

Symbol: `const providers:`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
  };
  const providers: Record<string, Type[]> = {
    identity: [IdentityService],
    catalog: [CatalogService],
    inquiries: [InquiriesService, OutboxPublisher],
```

<a id="source-no09"></a>

## NO09 · backend/test/workflows.spec.ts

Symbol: `function database(`. Full-file SHA-256: `a35785dec5a1015a3a37b334b387667cccc4ad5975a2b5283433bcd102815d6b`.

```text
};
function database(rows: unknown[] = []) {
  const query = jest.fn<(...args: any[]) => Promise<any>>().mockResolvedValue({ rows });
  const db = {
    query,
```

<a id="source-no10"></a>

## NO10 · frontend/src/hooks/useMarketplace.test.tsx

Symbol: `let resolveFirst`. Full-file SHA-256: `f1c35db19a488c701be1fc2411cd2d51d148e572f6f27c70ece49d7b5ddba5c5`.

```text
  it("ignores late search results after filters change even if transport ignores abort", async () => {
    let resolveFirst!: (value: Response) => void;
    vi.stubGlobal(
      "fetch",
      vi
```

<a id="source-no11"></a>

## NO11 · package.json

Symbol: `"acceptance":`. Full-file SHA-256: `d680dbdf10b38324c8099c83ddc3f2b3a0cb45f49b049aaf5aac77edcacf1d34`.

```text
    "build": "npm --prefix backend run build && npm --prefix frontend run build",
    "acceptance": "node scripts/acceptance.mjs http://localhost:8180 docs/evidence/local-acceptance.json",
    "test:browser": "node scripts/browser-smoke.mjs http://localhost:8180"
  },
  "devDependencies": {
```

<a id="source-no12"></a>

## NO12 · scripts/browser-smoke.mjs

Symbol: `chromium`. Full-file SHA-256: `0b3fde952a0e7d2381b676c7120a2548c79f14981197368e64d01196357c686a`.

```text
import { mkdir, writeFile } from 'node:fs/promises';
import { chromium } from 'playwright';
const base=process.argv[2]||'http://127.0.0.1:8180';
const browser=await chromium.launch({headless:true,...(process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
const results=[];
```

<a id="source-no13"></a>

## NO13 · frontend/src/services/http.ts

Symbol: `if (!res.ok)`. Full-file SHA-256: `519eadc524d706311cbf8fa2da42cf0b06f32bad8217cdb4978cd59cf45c276e`.

```text
  });
  if (!res.ok) {
    let detail = "The request could not be completed.";
    try {
      const e = await res.json();
```

<a id="source-no14"></a>

## NO14 · frontend/src/hooks/useMarketplace.ts

Symbol: `if (controller.signal.aborted) return;`. Full-file SHA-256: `3b000e07303811f6cc73b1bdbef0635d65a159124102d956337e7f45a1757f72`.

```text
      .then((r) => {
        if (controller.signal.aborted) return;
        setProviders(r.items);
        setTotal(r.total);
      })
```

<a id="source-no15"></a>

## NO15 · frontend/src/hooks/useInquiryAttempt.ts

Symbol: `const inFlight = useRef(false);`. Full-file SHA-256: `d082914d2e8cc7437aec1b5a295f5161f8ab7547e60f759a8cb7bc093b5196dc`.

```text
  const mounted = useRef(true);
  const inFlight = useRef(false);
  useEffect(() => {
    mounted.current = true;
    return () => {
```

<a id="source-no16"></a>

## NO16 · frontend/src/hooks/useInquiryAttempt.ts

Symbol: `sessionStorage.setItem(key, JSON.stringify(canonical));`. Full-file SHA-256: `d082914d2e8cc7437aec1b5a295f5161f8ab7547e60f759a8cb7bc093b5196dc`.

```text
    // Persist before sending: dismiss/reopen and page reload must resume this attempt.
    sessionStorage.setItem(key, JSON.stringify(canonical));
    setAttempt(canonical);
    inFlight.current = true;
    setBusy(true);
```

<a id="source-no17"></a>

## NO17 · .github/workflows/verify.yml

Symbol: `jobs:`. Full-file SHA-256: `fc09098fb72d963e65f4621e88f57c54e91c5927a16be389fef793adb913554f`.

```text
  cancel-in-progress: true
jobs:
  source:
    runs-on: ubuntu-latest
    timeout-minutes: 15
```

<a id="source-no18"></a>

## NO18 · scripts/sonar-ci.mjs

Symbol: `qualitygate`. Full-file SHA-256: `e13c9b35c37de9c919db3b595c88c7899dd0a427b4522168604e7ebb72b7713b`.

```text
  const gateName = 'Marketplace release (Sonar way plus overall checks)';
  const gate = await api('/api/qualitygates/copy', { sourceName: 'Sonar way', name: gateName });
  for (const condition of [
    { metric: 'coverage', op: 'LT', error: '80' },
    { metric: 'violations', op: 'GT', error: '0' },
```

<a id="source-no19"></a>

## NO19 · backend/package.json

Symbol: `"overrides":`. Full-file SHA-256: `b22b09f975bd55e53ffb60eca9ff9b031d310426e8a20dd072b7b298e55559da`.

```text
  },
  "overrides": {
    "js-yaml": "^4.1.1",
    "@nestjs/platform-express": {
      "multer": "2.5.0"
```

<a id="source-no20"></a>

## NO20 · .github/workflows/deploy-dev.yml

Symbol: `id-token:`. Full-file SHA-256: `022a3fde2671ef6c53af6417754eabd544c3acb07e99bd2aca01ae6580f1ebc1`.

```text
      contents: read
      id-token: write
    runs-on: ubuntu-latest
    timeout-minutes: 25
    env:
```

<a id="source-no21"></a>

## NO21 · scripts/aws-remote-deploy.sh

Symbol: `flock -n 9`. Full-file SHA-256: `c26debfcadb3297dcd2997d42e41a25d6fd73c7a605a43f2e0c6644d67a4bea1`.

```text
exec 9>/opt/marketplace/deploy.lock
flock -n 9 || { echo 'Another deployment is running'; exit 1; }
secret_arn=$(jq -er .secret_arn manifest.json)
region=$(jq -er .region manifest.json)
registry=$(jq -er .backend manifest.json | cut -d/ -f1)
```

<a id="source-no22"></a>

## NO22 · CONTRACT.md

Symbol: `executable reference`. Full-file SHA-256: `86989a051b164fb8ccba93f8daf22e2020043730f32125a7678152bf1764707c`.

```text

This document defines the local application boundaries and the API behavior that the frontend and services rely on. The schemas below define the public migration contract; the executable reference is `scripts/acceptance.mjs`.

**Stack:** Node.js 22, NestJS, strict TypeScript, React/Vite, PostgreSQL and Kafka. Local and AWS dev have independent configuration, secrets and data.
```

<a id="source-no23"></a>

## NO23 · backend/src/catalog/catalog.service.ts

Symbol: `async search`. Full-file SHA-256: `f993491d6ec844e830c04a34822e6c70b625966b32ae9fda873679cbfb7cd531`.

```text
  }
  async search(input: unknown) {
    const query = searchSchema.parse(input);
    // Parameterized JSONB predicates keep filtering/pagination in PostgreSQL as the catalog grows.
    const values: unknown[] = [];
```

<a id="source-no24"></a>

## NO24 · backend/src/notifications/notifications.service.ts

Symbol: `async list`. Full-file SHA-256: `d4eabfe0f00dc4f96da55b4864c937c6b630f332b1eb928725b4888236a07eae`.

```text
  }
  async list(actor: Actor) {
    const result = await this.db.query<NotificationRow>(
      'SELECT * FROM notifications WHERE recipient_email=$1 ORDER BY created_at DESC,id',
      [actor.email],
```

<a id="source-no25"></a>

## NO25 · backend/src/notifications/notifications.service.ts

Symbol: `ON CONFLICT`. Full-file SHA-256: `d4eabfe0f00dc4f96da55b4864c937c6b630f332b1eb928725b4888236a07eae`.

```text
    await this.db.query(
      'INSERT INTO notifications(id,event_id,inquiry_id,recipient_email,message,created_at) VALUES($1,$2,$3,$4,$5,$6) ON CONFLICT(event_id) DO NOTHING',
      [
        randomUUID(),
        event.eventId,
```

<a id="source-no26"></a>

## NO26 · backend/src/common/messaging.ts

Symbol: `class InquiryConsumer`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
@Injectable()
export class InquiryConsumer implements OnApplicationBootstrap, OnModuleDestroy {
  private readonly logger = new Logger('InquiryConsumer');
  private consumer?: Consumer;
  private stopping = false;
```

<a id="source-no27"></a>

## NO27 · backend/src/common/messaging.ts

Symbol: `class InquiryConsumer`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
@Injectable()
export class InquiryConsumer implements OnApplicationBootstrap, OnModuleDestroy {
  private readonly logger = new Logger('InquiryConsumer');
  private consumer?: Consumer;
  private stopping = false;
```

<a id="source-no28"></a>

## NO28 · backend/src/main.ts

Symbol: `await app.listen`. Full-file SHA-256: `b7ec3c2e7aa877c7e48f7a74e3350d373044ae6834760996db7d3b34b38bc988`.

```text
    throw new Error('PORT must be a valid TCP port');
  await app.listen(port, '0.0.0.0');
}
void bootstrap().catch((error) => {
  console.error(error instanceof Error ? error.stack : error);
```

<a id="source-no29"></a>

## NO29 · backend/src/common/connections.ts

Symbol: `connectionTimeoutMillis`. Full-file SHA-256: `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

```text
    max: 10,
    connectionTimeoutMillis: 5000,
    ssl: sslEnabled ? { rejectUnauthorized: true, ...(ca ? { ca } : {}) } : undefined,
  };
}
```

<a id="source-no30"></a>

## NO30 · backend/src/common/messaging.ts

Symbol: `class OutboxPublisher`. Full-file SHA-256: `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

```text
@Injectable()
export class OutboxPublisher implements OnApplicationBootstrap, OnModuleDestroy {
  private readonly logger = new Logger('OutboxPublisher');
  private producer?: Producer;
  private stopping = false;
```

<a id="source-no31"></a>

## NO31 · backend/src/common/health.ts

Symbol: `class HealthController`. Full-file SHA-256: `2941f0c699974fd0f6e27c82200cd617693eae335afdd4710066eb3fadf4c5b8`.

```text
@Controller()
export class HealthController {
  constructor(
    private readonly db: Database,
    private readonly worker: WorkerHealth,
```

<a id="source-no32"></a>

## NO32 · backend/src/inquiries/inquiries.service.ts

Symbol: `class InquiriesService`. Full-file SHA-256: `4e1752037f93eac22b8f2017299f218afd6b04f32cda4a002a45c2655ffe3c85`.

```text
@Injectable()
export class InquiriesService {
  constructor(private readonly db: Database) {}
  private async provider(id: string) {
    let response: Response;
```

<a id="source-no33"></a>

## NO33 · backend/src/common/database.ts

Symbol: `readonly pool =`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
export class Database implements OnModuleInit, OnModuleDestroy {
  readonly pool = new Pool(databaseOptions());
  constructor() {
    this.pool.on('error', (error: Error) =>
      console.error(
```

<a id="source-no34"></a>

## NO34 · compose.yaml

Symbol: `mem_limit:`. Full-file SHA-256: `4041fec31b19574a77777564085c3041cea86059684edd71b5d4f7d0f491ed7c`.

```text
  restart: unless-stopped
  mem_limit: 256m
  cpus: 1
  security_opt: [no-new-privileges:true]
  depends_on:
```

<a id="source-no35"></a>

## NO35 · compose.yaml

Symbol: `volumes:`. Full-file SHA-256: `4041fec31b19574a77777564085c3041cea86059684edd71b5d4f7d0f491ed7c`.

```text
      NOTIFICATIONS_DB_PASSWORD: ${NOTIFICATIONS_DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./infra/postgres/init-databases.sh:/docker-entrypoint-initdb.d/10-databases.sh:ro
    healthcheck:
```

<a id="source-no36"></a>

## NO36 · backend/src/common/connections.ts

Symbol: `export function databaseOptions`. Full-file SHA-256: `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

```text
}
export function databaseOptions(): PoolConfig {
  const sslEnabled = enabled('DB_SSL');
  let connection: PoolConfig;
  if (process.env.DB_URL) {
```

<a id="source-no37"></a>

## NO37 · backend/src/common/database.ts

Symbol: `database_pool_error`. Full-file SHA-256: `f24201468bda45ef27d5b7e6362bf5acf0f4ef67797067b92444b2410d134f3a`.

```text
      console.error(
        JSON.stringify({ level: 'error', event: 'database_pool_error', message: error.message }),
      ),
    );
  }
```

<a id="source-no38"></a>

## NO38 · backend/src/common/health.ts

Symbol: `class WorkerHealth`. Full-file SHA-256: `2941f0c699974fd0f6e27c82200cd617693eae335afdd4710066eb3fadf4c5b8`.

```text
@Injectable()
export class WorkerHealth {
  ready = !['inquiries', 'notifications'].includes(serviceName());
}
@Controller()
```

<a id="source-no39"></a>

## NO39 · backend/package.json

Symbol: `"moduleNameMapper":`. Full-file SHA-256: `b22b09f975bd55e53ffb60eca9ff9b031d310426e8a20dd072b7b298e55559da`.

```text
    ],
    "moduleNameMapper": {
      "^(\\.{1,2}/.*)\\.js$": "$1"
    },
    "transform": {
```

<a id="source-no40"></a>

## NO40 · backend/src/identity/identity.service.ts

Symbol: `if (process.env.SEED_DEMO !== 'true') return;`. Full-file SHA-256: `523e20fee146d919f357a86e0dacb858f1e077249662225affcbb28a86846756`.

```text
    this.dummyHash = await hashPassword('dummy-password-never-used');
    if (process.env.SEED_DEMO !== 'true') return;
    const providers: { ownerEmail: string; name: string }[] = JSON.parse(
      await readFile(join(process.cwd(), 'seeds/providers.json'), 'utf8'),
    );
```

<a id="source-noi01"></a>

## NOI01 · backend/package.json

Symbol: `"engines":`. Full-file SHA-256: `b22b09f975bd55e53ffb60eca9ff9b031d310426e8a20dd072b7b298e55559da`.

```text
  "private": true,
  "engines": {
    "node": ">=22 <25"
  },
  "scripts": {
```

<a id="source-noi02"></a>

## NOI02 · scripts/dev.mjs

Symbol: `PORT:String(8181+index)`. Full-file SHA-256: `d9dc9b4664d5db3caff38adc32e429f81c5abe6b9638b4aeb5739518bb439d1d`.

```text
for (const [index,service] of ['identity','catalog','inquiries','notifications'].entries()) {
  const env={...process.env,...secrets,SEED_DEMO:'true',INSPECT_PORT:String(9229+index),SERVICE:service,PORT:String(8181+index),DB_URL:`postgresql://${service}:${secrets[`${service.toUpperCase()}_DB_PASSWORD`]}@127.0.0.1:55432/${service}`,CATALOG_URL:'http://127.0.0.1:8182',KAFKA_BROKERS:'127.0.0.1:19092'};
  children.push(spawn('npm',['run',`dev:${service}`],{cwd:resolve(root,'backend'),env,stdio:'inherit',detached:process.platform!=='win32'}));
}
children.push(spawn('npm',['run','dev'],{cwd:resolve(root,'frontend'),env:process.env,stdio:'inherit',detached:process.platform!=='win32',detached:process.platform!=='win32'}));
```

<a id="source-noi03"></a>

## NOI03 · scripts/setup-local.sh

Symbol: `Keeping existing .env`. Full-file SHA-256: `9951bff8a5f7fdbe98e96b565c62f9080690edd92cd7a9a84a51167cbbb99a6c`.

```text
if [ -e .env ]; then
  echo 'Keeping existing .env and database credentials.'
  exit 0
fi
umask 077
```

<a id="source-noi04"></a>

## NOI04 · backend/Dockerfile

Symbol: `COPY --chown=node:node migrations`. Full-file SHA-256: `f6e27129a553a36ab16b821dc34f1667fd42a6a40d21e526261b5b3e0c4051a7`.

```text
COPY --chown=node:node certs ./certs
COPY --chown=node:node migrations ./migrations
COPY --chown=node:node seeds ./seeds
COPY --chown=node:node package.json ./
USER node
```

<a id="source-noi05"></a>

## NOI05 · frontend/src/hooks/useMarketplace.ts

Symbol: `if (controller.signal.aborted) return;`. Full-file SHA-256: `3b000e07303811f6cc73b1bdbef0635d65a159124102d956337e7f45a1757f72`.

```text
      .then((r) => {
        if (controller.signal.aborted) return;
        setProviders(r.items);
        setTotal(r.total);
      })
```

<a id="source-noi06"></a>

## NOI06 · scripts/acceptance.mjs

Symbol: `const base=`. Full-file SHA-256: `c1944f25a05ae7ed076c632bc3d8177495e1bde456c3eed74095170e67f4fb9d`.

```text
import { dirname } from 'node:path';
const base=(process.argv[2]||'http://localhost:8080').replace(/\/$/,'');
const output=process.argv[3];
const runId=`acceptance-${Date.now()}`;
const results=[];
```

<a id="source-noi07"></a>

## NOI07 · backend/src/notifications/notifications.service.ts

Symbol: `ON CONFLICT`. Full-file SHA-256: `d4eabfe0f00dc4f96da55b4864c937c6b630f332b1eb928725b4888236a07eae`.

```text
    await this.db.query(
      'INSERT INTO notifications(id,event_id,inquiry_id,recipient_email,message,created_at) VALUES($1,$2,$3,$4,$5,$6) ON CONFLICT(event_id) DO NOTHING',
      [
        randomUUID(),
        event.eventId,
```

<a id="source-noi08"></a>

## NOI08 · scripts/aws-remote-deploy.sh

Symbol: `flock -n 9`. Full-file SHA-256: `c26debfcadb3297dcd2997d42e41a25d6fd73c7a605a43f2e0c6644d67a4bea1`.

```text
exec 9>/opt/marketplace/deploy.lock
flock -n 9 || { echo 'Another deployment is running'; exit 1; }
secret_arn=$(jq -er .secret_arn manifest.json)
region=$(jq -er .region manifest.json)
registry=$(jq -er .backend manifest.json | cut -d/ -f1)
```

<a id="source-noi09"></a>

## NOI09 · backend/src/common/connections.ts

Symbol: `max:`. Full-file SHA-256: `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

```text
    ...connection,
    max: 10,
    connectionTimeoutMillis: 5000,
    ssl: sslEnabled ? { rejectUnauthorized: true, ...(ca ? { ca } : {}) } : undefined,
  };
```
