# Service marketplace · Node.js and AWS

An independent interview portfolio migrated from the Java project in “Build LinkedIn-style service market” and “Linked-in-project Phase 2”. Providers showcase services, skills, experience, portfolios, rates and availability. Companies/individuals discover and compare providers, send durable inquiries and receive provider decisions and notifications.

React/TypeScript, four NestJS services, PostgreSQL and Kafka run locally. Terraform and GitHub Actions prepare an isolated AWS dev environment. The original project and credentials are preserved. This application is not affiliated with LinkedIn.

## Run locally

Install Node.js 22+ and Docker Desktop/Compose v2, then:

```bash
cd /Users/robertovalencia/Documents/Business/linked-in-node-and-aws
npm run setup
npm run up
```

Open **http://localhost:8180**. Demo accounts: `company@demo.local` and `individual@demo.local` are clients; `ava@demo.local` and `leo@demo.local` are providers. All use `DemoPass123!`. These are synthetic laboratory identities.

For hot reload, use `npm run down`, `bash scripts/local.sh deps`, install dependencies with `npm --prefix backend ci` and `npm --prefix frontend ci`, then `npm run dev`. Open **http://localhost:5183**. See [complete local setup and troubleshooting](docs/local-setup.md).

## Verify and understand

```bash
npm --prefix backend ci
npm --prefix frontend ci
npm run check
npm test
npm run build
npm run acceptance
npx playwright install chromium
npm run test:browser
node scripts/failure-drill.mjs
```

[Results and limitations](docs/results.md) report actual fresh evidence. [Testing](docs/testing.md) explains the 48 reference API checks, unit/component tests and resilience drills. [Progress page](docs/progress.html) records the build and critic status.

## Project map

| Path | Purpose |
|---|---|
| `backend/src/{identity,catalog,inquiries,notifications}` | Four independently run NestJS capabilities with service-owned PostgreSQL data |
| `backend/src/common`, `backend/migrations` | Shared infrastructure/security and versioned SQL migrations |
| `frontend/src/components` | Separate component files grouped by UI responsibility |
| `frontend/src/{services,routes,types,contexts,hooks}` | Typed APIs, page composition, contracts, auth and reusable state/effects |
| `compose.yaml`, `scripts/local.sh`, `scripts/dev.mjs` | Isolated local containers and host hot reload |
| `infra/aws-dev`, `infra/bootstrap`, `scripts/aws-*` | Terraform dev infrastructure, remote-state setup and release operations |
| `.github`, `.vscode`, `sonar-project.properties` | Delivery/quality automation and editor tooling |

## Learn and rehearse

Start with [architecture and request/event diagrams](docs/architecture.md), then [Java-to-NestJS migration](docs/interview-topics/java-to-nestjs.md), [data consistency and security](docs/interview-topics/data-security.md), [React layers](docs/interview-topics/frontend.md) and the [API/event contract](CONTRACT.md).

Practice the [interview demonstration and questions](docs/interview-demo.md). Use [Codex development and review workflow](docs/ai-development.md), [requirements](docs/specs/requirements.md), [implementation plan](docs/specs/implementation-plan.md), [traceability/Jira import](docs/traceability.md), [critic review records](docs/reviews.md) and [toolchain setup](docs/toolchain.md) to explain how you direct and validate generated code. Approximately 95% Codex-generated application code is a target, not a measured claim.

## AWS development environment

[AWS dev setup, deployment, rollback and cleanup](docs/aws-dev.md) explains the Terraform-managed EC2/SSM/ECR environment. [Current cost assumptions](docs/costs.md) and [Azure equivalents](docs/azure-mapping.md) cover interview tradeoffs. Local data/secrets/ports never target AWS. Provisioning requires review and approval of the actual saved Terraform plan. See [results](docs/results.md) for what was executed versus prepared.
