# Service marketplace · Node.js and AWS

A [private GitHub interview portfolio](https://github.com/robertovalencia/linked-in-node-and-aws) migrated from the Java project in “Build LinkedIn-style service market” and “Linked-in-project Phase 2”. Providers showcase services, skills, experience, portfolios, rates and availability. Companies/individuals discover and compare providers, send durable inquiries and receive provider decisions and notifications.

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
| `infra/aws-ecs-dev`, `infra/aws-ecs-certificate` | Selected private ECS/RDS/NAT preparation and optional owned-hostname certificate |
| `infra/aws-dev`, `infra/bootstrap`, `scripts/aws-*` | Preserved EC2/SSM baseline, separate remote-state setup and release controls |
| `.github`, `.vscode`, `sonar-project.properties` | Delivery/quality automation and editor tooling |

## Learn and rehearse

Explore the [NodeJs/AWS study path](docs/nodejs-aws-study-path/README.md): 44 beginner-to-senior lessons covering JavaScript, TypeScript, Node.js/NestJS, PostgreSQL, Kafka, React, AWS/Terraform, testing, and AI-assisted delivery. Follow the [twelve-week roadmap and mastery gates](docs/nodejs-aws-study-path/generated/00-roadmap-and-mastery-gates.md), use the six-week or urgent interview route, or [download the complete study pack](docs/nodejs-aws-study-path/NodeJs-AWS-study-pack.zip). Lessons teach individual Node.js concepts and libraries with short explanations, exact source excerpts, fixed GitHub line links, recall questions, and practical labs. The coverage matrix maps tools and interview requirements to lessons.

For deeper cloud study, start the [24-lesson AWS/Terraform extension](docs/nodejs-aws-study-path/generated/20-cloud-roadmap-and-lab.md): AWS fundamentals, IAM/networking, EC2/ECR/S3/secrets, operations/costs, Terraform language/state/plans/testing, and deployment/rollback. Practice with the [credential-free local Terraform lab](docs/nodejs-aws-study-path/labs/terraform-local/README.md) before any account-backed work.

For service-specific tools, open the [Node.js technical handbooks](docs/nodejs-beginner/README.md): Identity (scrypt/JWT), Catalog (Zod/JSONB), Inquiries (fetch/hashes/locks), and Notifications (KafkaJS/offsets/deduplication). The original application walkthroughs and local debugging labs remain available there.

Start with [architecture and request/event diagrams](docs/architecture.md), then [Java-to-NestJS migration](docs/interview-topics/java-to-nestjs.md), [data consistency and security](docs/interview-topics/data-security.md), [React layers](docs/interview-topics/frontend.md) and the [API/event contract](CONTRACT.md).

Practice the [interview demonstration and questions](docs/interview-demo.md). Use the [paste-ready project gauntlet prompt](docs/prompts/project-gauntlet.md), [Codex development and review workflow](docs/ai-development.md), [requirements](docs/specs/requirements.md), [implementation plan](docs/specs/implementation-plan.md), [traceability/Jira import](docs/traceability.md), [critic review records](docs/reviews.md) and [toolchain setup](docs/toolchain.md), [hosted SonarQube setup](docs/sonarqube-cloud.md) to explain how you direct and validate generated code. Approximately 95% Codex-generated application code is a target, not a measured claim.

The [dependency security guide](docs/dependency-security.md) explains the body-parser/Multer advisory repair, the temporary scoped npm override, verification evidence, and when to remove it. Hosted SonarCloud setup remains a separate owner action; its missing credentials do not disable production audit or release verification.

## AWS development environment

The selected [private ECS/RDS + one NAT environment](docs/aws-ecs-dev.md) is prepared for plan review, with narrow security-group trust, verified database/broker TLS, service-owned databases, logs, alarms and recovery controls. The free zone `linked-in-node-rv.dynv6.net` is registered; a certificate-only plan for its `app` child is ready for review. The historical **108-create staging preview** has no ALB listener, client ingress or application tasks. The [free testing-hostname guide](docs/aws-free-test-hostname.md) provides a dynv6 path without buying a domain. Do not pay for infrastructure while waiting for DNS. Expected gross costs are **$6.71/24h staging** or **$8.32/24h after future five-task activation**, plus recovery exercises; the corresponding 720-hour estimates are $187.40/$235.68 before credits. These are estimates, not caps.

The [27 October cost-first comparison](docs/aws-cost-review-2026-10-27/README.md) contains dated Ohio prices and alternatives including the preserved [EC2/SSM baseline](docs/aws-dev.md), NAT/endpoints and optional MSK. Read [fresh local preparation evidence and pending cloud gates](docs/results.md), [Azure equivalents](docs/azure-mapping.md), and the new guide's hostname → certificate → final plan → verification → activation → teardown steps. The account recheck found an active Free plan/$100 credits and no project resources in the queried scopes; this does not make every service free. No AWS apply, image publication, live recovery or deployment has occurred. Hosted Sonar Cloud remains configured/pending; GitHub verification retains the isolated SonarQube 80% gate. A final S3-backed saved plan, current costs and explicit approval are required before provisioning. No teardown deadline has started.
