# Requirements and acceptance specification

This is an independent interview laboratory migrated from reference commit `582c847d700c27d3bc60b44aeb8974ee6365face`. Its requirements are product behavior, not a promise to reproduce every historical infrastructure tool. AWS replaces the reference's prepared GCP environment. Java is replaced completely in runtime/build paths.

| ID | Business or engineering requirement | Judgeable acceptance |
|---|---|---|
| R01 | Anonymous provider discovery | Six durable profiles; search, category, skill, rate, availability, deterministic sorting/paging, empty state |
| R02 | Rich profiles and comparison | Skills, tools, experience, portfolio, prices and availability rendered; compare real API results |
| R03 | Authentication and authorization | Four demo identities; invalid/tampered/missing token rejected; role and owner enforced server-side |
| R04 | Provider profile update | Provider can edit own profile, invalid price rejected, changes survive read/restart, cannot alter another owner |
| R05 | Durable inquiries | Company/individual can submit; same idempotency key and payload converge under concurrency; changed payload conflicts |
| R06 | Inquiry lifecycle | Only participants list; only target provider accepts/declines; invalid transitions/status rejected |
| R07 | Eventual notifications | Inquiry/outbox commit atomically; broker failure does not lose intent; consumer deduplicates; read ownership persists |
| R08 | Readable React architecture | Separate components/services/routes/types/contexts/hooks; loading/error/empty states and stale-response handling |
| R09 | Reproducible local setup | No AWS credentials; Compose data dependencies; hot reload; explicit start/test/debug/reset/stop commands |
| R10 | Isolated AWS dev | Terraform validated/mocked for optional GitHub OIDC and selected temporary-local-login mode; reviewed final S3-backed plan; separate state/secrets/data; immutable release, exact-command 48-check smoke evidence and rollback; 24-hour teardown |
| R11 | Enforced delivery toolchain | ESLint, Prettier, strict types, Vitest/Jest, Dependabot, isolated CI SonarQube 80% gate and exact-SHA successful verification before release; hosted Cloud configured pending; Jira import and VS Code setup |
| R12 | AI-assisted learning and traceability | Codex instructions/specs/prompts; README-linked guides; requirements → tests → source → deployment → release record |

The existing product exposes inquiry creation and reading plus profile/status/inbox updates. It has no profile deletion workflow: “CRUD layer design” means clear responsibility separation, not inventing destructive endpoints. New deletion requirements need their own product specification.

The original suite has conditional checks. A successful process alone is insufficient: require exactly 48 passes and zero failures, including the branches after login/inquiry creation. Supplement those with frontend, security, persistence, broker-outage and deduplication evidence. A passing local suite does not establish AWS readiness or a completed cloud deployment.


## R12 learning acceptance: AWS/Terraform extension

The NodeJS/AWS path contains 84 lessons, including 64 ordered AWS/Terraform lessons (20–83). New lessons must distinguish current resources from proposed services, link real pinned GitHub examples, teach prerequisites/mechanisms, include observable practice and answered recall questions. The credential-free local Terraform lab must demonstrate create, idempotence, update, replacement, moved identity, tests and cleanup. The real Terraform mock checks must report actual execution. Study Desk navigation must expose the lessons and preserve all personal/saved content. Validate local links and pinned source ranges with `python3 scripts/check-cloud-study.py`; do not provision cloud infrastructure for documentation verification.


## R11 dependency repair acceptance

Production npm audit remains enforced at high severity for root/backend/frontend. Preserve NestJS 12.2.0 and API contracts while upgrading body-parser to 2.4.0 and scoping a temporary Multer 2.5.0 override to `@nestjs/platform-express`. Require a valid dependency tree, reproducible `npm ci`, passing existing 64 backend and 28 frontend tests/builds/checks, the unchanged 48-check running API suite, and actual hosted Verify results. Hosted SonarCloud remains separately owner-configured; missing credentials must not be marked as a successful analysis.


## R10 cost-first phased deployment acceptance

Before implementing a changed topology or provisioning, compare the actual zero-ingress EC2/SSM baseline with proportionate hardening, ALB/TLS, private ECS/Fargate + RDS and separately optional MSK. Require dated Ohio prices, deterministic 24-hour/720-hour idle/expected/higher-use calculations, all compute/network/data/observability/security/storage meters, account eligibility/credits and scoped deployment inventory, traffic/identity/recovery tests, and explicit residual/rollback/teardown boundaries. Preserve Kafka and service-owned DB contracts; do not deploy named services merely for curriculum coverage. No AWS mutations, account upgrades, changed exposure or paid-service enablement are authorized by the cost review. A chosen implementation needs a new source-bound final plan, updated costs and separate provisioning approval. The [27 October reviewed packet](../aws-cost-review-2026-10-27/README.md) satisfies the decision-support scope; implementation/runtime gates remain pending.

## R10 selected ECS preparation acceptance, 27 October 2026

The owner selected private ECS/RDS with one zonal NAT for plan preparation, not provisioning. Preserve the EC2/SSM roots and local environment. Require per-service SG trust, private RDS/EC2, owned DB roles, verified DB/broker TLS, secret-free Terraform, distinct ECS state key, immutable exact-SHA verified/scanned images, safe bootstrap/replay, bounded logs/alarms and explicit recovery/teardown boundaries. No owned hostname means no listener, no client CIDR ingress and no running application tasks; a separate nonexportable DNS certificate module must not purchase a domain or zone.

Acceptance for preparation: real disposable PostgreSQL TLS/ownership/idempotent migrations/replay/password-log checks; actual Kafka TLS/SCRAM/ACL tests; nginx DNS replacement proof; unchanged 48 API checks and desktop/mobile journeys; 10 ECS plus two certificate mock runs; publisher contracts retaining all release gates; offline saved-plan source/JSON/rule checks with executable negative controls; independently reviewed current plan/costs. Live cloud identity denial, health, metrics/alarm/delivery, recovery RPO/RTO, rollback and 48-check smoke remain separate required gates after explicit approval. A local preview must never be described as a final S3-backed apply plan.

### R12 professional core breadth

The concept checklist covers identity/governance, networking/ingress/private access, managed compute/data/events, encryption/security/audit, telemetry/recovery/cost methods and advanced Terraform modules/state/collaboration. Absent project features still require primary-source teaching, clearly labeled new examples and observable local or design exercises. Three local labs must preserve existing behavior and pass their meaningful assertions; Study Desk exposes 85 guides including the index and preserves saved notes. The learning chat makes no actual cost estimate or infrastructure change; the acknowledged deployment owner supplies those after current evidence and cost review.
