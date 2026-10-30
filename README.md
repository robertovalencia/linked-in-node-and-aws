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

The [AWS visual study guide](docs/nodejs-aws-study-path/visuals/README.md) adds actual project views and official console examples with field explanations and explicit provenance, plus guidance for email/provider sign-in and the actual IAM user-permissions wizard.

New to the setup process? Read [How this project was set up and verified](docs/nodejs-aws-study-path/walkthroughs/README.md). Eleven small-concept chapters connect every stage—from local credentials and source review through Terraform/DNS/certificate preparation, pending deployment and GitHub/Study Desk publication—to real files and evidence.

Explore the [NodeJs/AWS study path](docs/nodejs-aws-study-path/README.md): 84 beginner-to-senior lessons covering JavaScript, TypeScript, Node.js/NestJS, PostgreSQL, Kafka, React, AWS/Terraform, testing, and AI-assisted delivery. Follow the [twelve-week roadmap and mastery gates](docs/nodejs-aws-study-path/generated/00-roadmap-and-mastery-gates.md), use the six-week or urgent interview route, or [download the complete study pack](docs/nodejs-aws-study-path/NodeJs-AWS-study-pack.zip). Lessons teach individual Node.js concepts and libraries with short explanations, exact source excerpts, fixed GitHub line links, recall questions, and practical labs. The coverage matrix maps tools and interview requirements to lessons.

For copyable commands with expected results, start the [local Terraform command workbook](docs/nodejs-aws-study-path/walkthroughs/09-terraform-local-commands.md), then the [AWS command and approval workflow](docs/nodejs-aws-study-path/walkthroughs/10-terraform-aws-commands.md).

For deeper cloud study, start the [24-lesson AWS/Terraform extension](docs/nodejs-aws-study-path/generated/20-cloud-roadmap-and-lab.md): AWS fundamentals, IAM/networking, EC2/ECR/S3/secrets, operations/costs, Terraform language/state/plans/testing, and deployment/rollback. Practice with the [credential-free local Terraform lab](docs/nodejs-aws-study-path/labs/terraform-local/README.md) before any account-backed work.

For service-specific tools, open the [Node.js technical handbooks](docs/nodejs-beginner/README.md): Identity (scrypt/JWT), Catalog (Zod/JSONB), Inquiries (fetch/hashes/locks), and Notifications (KafkaJS/offsets/deduplication). The original application walkthroughs and local debugging labs remain available there.

Start with [architecture and request/event diagrams](docs/architecture.md), then [Java-to-NestJS migration](docs/interview-topics/java-to-nestjs.md), [data consistency and security](docs/interview-topics/data-security.md), [React layers](docs/interview-topics/frontend.md) and the [API/event contract](CONTRACT.md).

Practice the [interview demonstration and questions](docs/interview-demo.md). Use the [paste-ready project gauntlet prompt](docs/prompts/project-gauntlet.md), [Codex development and review workflow](docs/ai-development.md), [requirements](docs/specs/requirements.md), [implementation plan](docs/specs/implementation-plan.md), [traceability/Jira import](docs/traceability.md), [critic review records](docs/reviews.md) and [toolchain setup](docs/toolchain.md), [hosted SonarQube setup](docs/sonarqube-cloud.md) to explain how you direct and validate generated code. Approximately 95% Codex-generated application code is a target, not a measured claim.

The [dependency security guide](docs/dependency-security.md) explains the body-parser/Multer advisory repair, the temporary scoped npm override, verification evidence, and when to remove it. Hosted SonarCloud setup remains a separate owner action; its missing credentials do not disable production audit or release verification.

## AWS development environment

The approved initial infrastructure apply **failed partially**: 99 completed creates, 100 managed state instances including a tainted ALB. Paid resources remain, but no RDS, HTTPS listener or application tasks are running. [Actual execution and independent critic](docs/evidence/aws-infrastructure-apply-2026-10-29/README.md) explain the three service failures.

The original operator-assisted shutdown deadline remains **30 October 2026, 5:51 PM EDT**, with operator return by **3:51 PM EDT**. There is no automatic cleanup. [Current repair/cost review](docs/aws-repair-review-2026-10-30.md) prepares a fresh plan; repair and application activation require separate exact approval. The account remains Free/ACTIVE with $98.59 reported credits at the 30 October read-only check.

The selected [private ECS/RDS + one NAT environment](docs/aws-ecs-dev.md) preserves local Compose and the Java project. Current repaired comparison estimates are **$6.84/24h** for infrastructure and **$8.32/24h** for future five-task activation, before credits, usage variation and recovery. Corresponding 720-hour comparisons are $191.32/$235.78; these do not extend the real deadline. [Cost alternatives](docs/aws-cost-review-2026-10-27/README.md), [Azure mapping](docs/azure-mapping.md), and [operator/teardown guide](docs/aws-operator-runbook-2026-10-29.md). Hosted SonarCloud remains configured/pending; isolated CI SonarQube keeps its 80% gate.

## Complete professional AWS/Terraform study

The [full syllabus and concept checklist](docs/nodejs-aws-study-path/generated/44-cloud-complete-syllabus-and-mastery-map.md) expands the path to 84 lessons, with 64 cloud/Terraform lessons. Important topics are taught even when the current portfolio does not implement them: new examples are explicitly illustrative, and advanced network/Terraform labs run locally without AWS credentials. Cost comparison and deployment redesign belong to “Create Node.js AWS LinkedIn project”; its [acknowledged handoff](docs/nodejs-aws-study-path/deployment-handoff.md) and [coordination status](docs/nodejs-aws-study-path/deployment-coordination.json) do not claim an approved or provisioned architecture.


Deployment status: the initial approved application plan failed partially; repair preparation is pending exact review and approval. The separate certificate and protected state bootstrap remain verified. Consult the current repair report for actual resources and the unchanged shutdown deadline.

For the real approved state bootstrap and the remaining application plan/24-hour teardown boundaries, read the [29 October AWS execution journal](docs/nodejs-aws-study-path/walkthroughs/11-aws-execution-journal.md).
