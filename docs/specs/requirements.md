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


### R12 process and setup companion

The GitHub learning entry point must link a supplementary beginner walkthrough of the recorded process and reproducible setup. Cover tools/local credentials/startup, contract-preserving migration, account identity and dated cost ownership, Terraform roots/backends/private state and saved-plan review, DNS/TLS issuance, pending delivery/security/recovery gates, independent build/review evidence, Git/PR/quality tooling and Study Desk import. Each chapter uses small concepts, code links, expected observations, troubleshooting and a comprehension check. Preserve 84 numbered lesson IDs. Include the walkthrough in the managed download and validate its links. Never claim pending AWS or external-account configuration has completed.


### R12 visual AWS learning companion

The GitHub study path must include real screenshots or attributed official AWS screenshots with small concept captions, related source/lesson links and recall questions. Distinguish an actual account capture, an unauthenticated sign-in screen and an official example. Never imply example resources are this project, expose credentials/private client addresses, or create resources for a screenshot. Include managed local images in the ZIP, state the online-only boundary for externally hosted examples, and validate the new local Markdown/image targets. Preserve existing numbered lesson IDs and saved notes.


### R12 Terraform command workbooks

Provide an executable local command sequence using only the inspected built-in-resource lab, plus a separately labeled AWS operator reference. Explain command purpose, working directory, inputs, expected observations, state scope and failure handling. The local sequence must actually pass; cloud templates must be syntax-checked and independently reviewed without being executed. Existing artifact guards must stop execution before overwrites, and saved-plan apply must explain its lack of an extra prompt and require the approved hash/account. Distinguish GitHub verification from the legacy EC2 deployment and pending ECS activation. Include the workbooks in the ZIP and link them from the existing roadmap/lessons without renumbering them.


### R12 execution-journal extension

Document the real approved bootstrap and its observed controls, actual S3 backend, visible safe inspection commands, offline plan-review output and failure/retry boundaries. Distinguish historical accepted artifacts from current source drift and never bypass the review. Record the selected 24-hour/delete-demo-data/preserve-state policy and pending shutdown mechanism. Preserve all numbered lesson IDs and include the new chapter in the downloadable pack and reader index.


## R10 partial-apply repair acceptance — 30 October 2026

The approved initial artifact failed; preserve its diagnostics, actual 100-instance state and original paid-resource deadline. Repair preparation must use a new real saved S3-backed plan, explicit mixed-action allowlist and fresh independent critic. Require one-day candidate RDS retention with seven-day source default and no account upgrade; Cloud Map broker registration; official ALB log-delivery scope; tainted-ALB replacement; explicit custom health for five proven-empty app definitions; pinned current broker AMI and preserved instance/EBS identities/protections. Require canonical configured volume expiry, disclosed cached provider tag mirror and actual post-apply read-back. Keep no application tasks/secret versions/public DNS changes. Preserve initial create-only gates; negative tests must reject changed broker storage/AMI, added exposure, extra replacements, source/backend/baseline mismatch and incorrect prices/quantities. Current cost and exact changed artifact need separate human approval; the original deadline is not extended.


## R10 fixed four-hour extension proposal and Kafka regression — October 30

Any four-hour deadline extension must preserve the original start, actual partial states, deployed broker/AMI/EBS and existing private client rule. Require a new concrete binary, exact managed-change comparison showing only the proposed deadline differs, current incremental Decimal estimate and one combined human approval before extension or repair apply. Keep original artifact/reviewer guards unchanged; proposal validation is not approval. No new reviewers per human instruction. Locally generated Kafka cluster IDs must retain the 16-byte URL-safe encoding and avoid a leading hyphen that kafka-storage parses as an option. Require a deterministic leading-hyphen regression and the existing real TLS/SCRAM/ACL drill. Hosted SonarCloud missing configuration remains blocked, without weakening any gate. See [proposal](../aws-extension-repair-proposal-2026-10-30.md).


## R10 actual Free-plan size restriction — October 30

After approved repair rejected db.t4g.small, preserve104-resource serial7 state, original clock plus approved four-hour extension, existing broker/AMI/EBS/private /32 and all diagnostics. Preparation may use documented db.t4g.micro (1GiB/2vCPU), preserving one-day backups, private encrypted storage, managed credentials, deletion protection and snapshot/backup protections. Require fresh eight-create/no-update/no-destroy plan, current micro rate, exact source/RDS delta and alarm dimension checks, targeted mock/security negative controls and separate approval of the changed artifact. Never claim orderability or mocks prove create/runtime acceptance; stop on rejection without account upgrade or weaker protections.


### R12 AWS/Terraform questionnaire acceptance · November 2, 2026

Add a supplementary 30-question/12-incident questionnaire inside the existing 84-lesson path, linked by both READMEs and packaged without personal data. Every stable Q01–Q30/I01–I12 item needs a short plain-language answer or diagnostic checks/repair/recovery sequence, existing lesson links, study priority, real source path and literal symbol/excerpt, evidence scope and a primary reference. Absent features need an official worked example. Distinguish current source, local/mock definitions and dated execution; reconcile October 30 completion/cleanup/rejected destroy with October 31 temporary stop, retained costs and RDS restart, without fresh cloud claims. Preserve all numbered lessons and saved progress. Validate IDs, actual source/excerpts, links/fragments, lesson mappings and absent examples through the existing checker plus negative regression tests; verify managed ZIP bytes/exclusions. Require a separate critic to review security, contracts, failure/recovery explanations and actual output. No cloud call, secret read, application activation, reader publication or GitHub write is needed for this learning change.

### R12 Node.js/backend interview companion · November 5, 2026

Inventory both84-lesson profiles plus service handbooks and setup walkthroughs before drafting. Add a supplementary beginner questionnaire whose stable cards carry priority, plain-language answers/acronym explanations, exact lesson links, inspected file/symbol/excerpt and relevant current official documentation. Label prerequisite versus researched extension and absent implementations; supply useful external worked examples. Include service setup and every retained Node/backend mechanism, plus researched gaps. Incidents must state symptom, checks, repair and observable recovery criteria, including stopped-consumer/manual-restart paths.

Acceptance: deterministic item/source/hash/render/lesson/link and complete concept-disposition checks; meaningful corrupt-input regressions; runnable credential-free examples with failure-path assertions; managed ZIP byte/inclusion/exclusion verification from a clean source candidate and extracted ZIP; independent fresh-context section/integrated reviews and anonymous equivalent-answer comparisons. Record actual results and largest gap/repair in reviews/evidence/live progress. Preserve numbered lessons, personal data, original Java and unrelated work. No hosted publication or cloud verification is inferred.
