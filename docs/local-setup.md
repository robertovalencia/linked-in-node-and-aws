# Local development and operations

Prerequisites: Node.js 22+, npm and Docker Desktop with Compose v2. Allocate about 4 GB to Docker for the application/dependencies; SonarQube needs additional memory. No AWS account, GitHub token or paid API key is required for local marketplace use.

```bash
cd /Users/robertovalencia/Documents/Business/linked-in-node-and-aws
npm run setup
npm run up
```

Open http://localhost:8180. Seed identities are `company@demo.local`, `individual@demo.local`, `ava@demo.local`, and `leo@demo.local`; all use `DemoPass123!`. The first two are clients and the last two are providers. Data is synthetic. `SEED_DEMO=true` enables those accounts locally; AWS demo seeding is an explicit development choice.

For hot reload, stop full application containers, keep only dependencies, then run the frontend and four backend processes on the host:

```bash
npm run down
bash scripts/local.sh deps
npm --prefix backend ci
npm --prefix frontend ci
npm run dev
```

Open http://localhost:5183. Vite proxies to services on 8181–8184. PostgreSQL is loopback 55432; Kafka's host listener is loopback 19092, while containers use `kafka:9092`. Do not run host services and the full application containers at the same time because they intentionally use the same service ports. `Ctrl+C` stops host processes; `npm run down` stops dependencies without deleting data.

```bash
bash scripts/local.sh status
bash scripts/local.sh logs inquiries
docker compose restart identity catalog inquiries notifications
npm run acceptance
```

For VS Code debugging, use the supplied launch/tasks configuration; investigate an individual service with its `SERVICE`, `PORT`, `DB_URL` and generated local secrets. Never paste secrets into shared logs. HTTP readiness is `/health/ready` per service; liveness is a separate process check. The frontend `/health` proves only nginx is serving, so verify API journeys as well.

`docker compose down` keeps data. To delete this laboratory's databases and broker data deliberately:

```bash
bash scripts/local.sh reset --confirm-local-data-loss
```

The script always uses this repository's Compose file/name. It never invokes AWS or the reference stack. Keep `.env` while volumes exist; startup creates passwords only once. To change database passwords without data loss, use a coordinated PostgreSQL role change and application secret update, not regeneration alone.

Common failures: port conflict means another host/full-stack process is listening; an authentication error after regenerating `.env` means stored database passwords differ; notifications missing means inspect inquiries outbox and notifications consumer plus broker health; a failed frontend request means inspect the Vite/nginx route and service readiness before changing the UI. Never resolve these by silently returning fake data.
