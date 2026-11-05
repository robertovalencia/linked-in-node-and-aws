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

Start with the [Node.js/backend interview questionnaire and troubleshooting guide](docs/nodejs-aws-study-path/node-backend-questionnaire.md): short answers, service setup, source-linked mechanisms, recovery scenarios and a credential-free runnable lab. The [coverage ledger](docs/nodejs-aws-study-path/node-backend-coverage.md) maps both lesson sets; [live progress](docs/nodejs-aws-study-path/node-backend-progress.md) records checks and independent reviews.

Practice with the [AWS/Terraform questionnaire and developer troubleshooting companion](docs/nodejs-aws-study-path/aws-terraform-questionnaire.md): 30 concise answers and 12 diagnostic scenarios, each mapped to existing lessons, priority and dated project evidence.

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

**October31 current operating state:** EC2 broker and RDS are verified **stopped**, with data/storage retained. Full teardown did not execute; ALB/NAT/storage and other resources remain allocated. RDS automatically restarts after seven stopped days. [Actual stop execution](docs/aws-reversible-compute-stop-2026-10-31.md).

**Final destroy blocked:** automatic approval review rejected execution before process creation.112 Terraform-managed resources remain; EC2 and RDS were subsequently stopped reversibly, with no deletion. [Blocked result and reversible-stop proposal](docs/aws-destroy-execution-blocked-2026-10-30.md).

**Current cleanup status:** the approved eight-update cleanup transition succeeded; RDS deletion protection is off and112 resources remain. [Final112-delete plan](docs/aws-final-destroy-approval-2026-10-30.md) awaits exact approval. The9:51PM EDT deadline was missed; no timer/extension exists. [Actual transition execution](docs/aws-cleanup-transition-execution-2026-10-30.md).

[Automatic-shutdown readiness audit](docs/aws-automatic-shutdown-readiness-2026-10-30.md): no automatic controller exists; exact eight-update cleanup transition is prepared but unapproved. Deadline remains9:51PM EDT.

[Live AWS inspection checklist](docs/aws-live-inspection-2026-10-30.md): current console links, CloudWatch findings, host inspection and private PostgreSQL connection boundaries.

[Micro completion executed and verified](docs/aws-micro-completion-execution-2026-10-30.md): 112 actual resources, available private/encrypted RDS with one-day backups, seven alarms and a no-change plan. App tasks remain zero. Deadline: 9:51 PM EDT; cleanup review by 7:51 PM EDT.

The earlier partial failures are repaired. The approved micro completion succeeded: 112 managed instances, no taints, available private/encrypted RDS with one-day backups and seven alarms. The ALB, HTTPS listener, access logs, broker DNS and expiry controls are verified; the fresh infrastructure plan has no changes. No application tasks are running. [Actual execution and independent critic](docs/evidence/aws-infrastructure-apply-2026-10-29/README.md) explain the three service failures.

The human approved a four-hour extension: the operator-assisted shutdown deadline is **30 October 2026, 9:51 PM EDT**, with cleanup preparation by **7:51 PM EDT**. There is no automatic cleanup. [Current repair/cost review](docs/aws-repair-review-2026-10-30.md) prepares a fresh plan; repair and application activation require separate exact approval. The account remains Free/ACTIVE with $98.59 reported credits at the 30 October read-only check.

The selected [private ECS/RDS + one NAT environment](docs/aws-ecs-dev.md) preserves local Compose and the Java project. Current micro comparison estimates are **$6.45/24h** for infrastructure and **$7.94/24h** for future five-task activation, before credits, usage variation and recovery. These are comparison windows and do not extend the real deadline; see the current micro cost packet for itemized figures. [Cost alternatives](docs/aws-cost-review-2026-10-27/README.md), [Azure mapping](docs/azure-mapping.md), and [operator/teardown guide](docs/aws-operator-runbook-2026-10-29.md). Hosted SonarCloud remains configured/pending; isolated CI SonarQube keeps its 80% gate.

## Complete professional AWS/Terraform study

The [full syllabus and concept checklist](docs/nodejs-aws-study-path/generated/44-cloud-complete-syllabus-and-mastery-map.md) expands the path to 84 lessons, with 64 cloud/Terraform lessons. Important topics are taught even when the current portfolio does not implement them: new examples are explicitly illustrative, and advanced network/Terraform labs run locally without AWS credentials. Cost comparison and deployment redesign belong to “Create Node.js AWS LinkedIn project”; its [acknowledged handoff](docs/nodejs-aws-study-path/deployment-handoff.md) and [coordination status](docs/nodejs-aws-study-path/deployment-coordination.json) do not claim an approved or provisioned architecture.


Deployment status: approved infrastructure repair completed and verified; application activation remains pending its release/runtime gates and exact approval. Separate certificate and state bootstrap are preserved. Shutdown deadline is 9:51 PM EDT, with cleanup review by 7:51 PM EDT.

For the real approved state bootstrap and the remaining application plan/24-hour teardown boundaries, read the [29 October AWS execution journal](docs/nodejs-aws-study-path/walkthroughs/11-aws-execution-journal.md).
