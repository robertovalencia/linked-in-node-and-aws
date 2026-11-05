# Requirements through release

The stable identifiers below map the interview specification to source, tests and operational evidence. They are local requirement IDs; Jira issue keys become real only after import into the chosen Jira project. Do not invent issue URLs or claim an import ran.

| Requirement | Implementation | Verification | Deployment/release link |
|---|---|---|---|
| R01 discovery | backend/src/catalog, frontend/services and hooks | acceptance search/filter/sort/paging; frontend discovery tests | Same catalog image/source commit as release |
| R02 profile/compare | frontend/src/components and routes | comparison/profile component tests; browser smoke | Frontend image digest |
| R03 identity/security | backend/src/common/auth.ts, identity | JWT/role/owner Jest tests; acceptance negative cases | Identity runtime of backend digest |
| R04 owned edits | catalog service + profile editor | acceptance cross-owner/invalid-price/persistent read; frontend workspace tests | Catalog runtime; migration version |
| R05 inquiry/idempotency | backend/src/inquiries | original concurrent duplicate checks + transaction tests | Inquiries runtime; DB migration |
| R06 lifecycle | inquiries service, workspace | accepted/declined/ownership API checks | Inquiries runtime |
| R07 notifications | outbox publisher + notifications consumer | Kafka acceptance; failure-drill replay/outage | Kafka topic + notifications runtime |
| R08 React separation | frontend/src/{components,services,routes,types,contexts,hooks} | lint/types; Vitest stale-request and error tests | Frontend digest |
| R09 local setup | compose.yaml, scripts/local.sh, scripts/dev.mjs | full Compose acceptance; hot-reload readiness | Local project linked-in-node-local |
| R10 AWS dev | infra/aws-ecs-dev, infra/aws-ecs-certificate; owned TLS connections/bootstrap/replay; scripts/aws-ecs-* | [Fresh local preparation evidence](evidence/ecs-preparation/verification-manifest.json), 10+2 mock runs, PG30/Kafka9/DNS5, saved-plan negative controls and independent critic | [Selected ECS guide](aws-ecs-dev.md); local-backend 108-create preview only; final S3 plan, exact-source CI and all cloud gates tracked separately |
| R11 toolchain | .github, .vscode, sonar-project.properties, compose.ci-quality.yaml, scripts/sonar-ci.mjs | Prior local/Verify gates pass; fresh exact-SHA verification with isolated CI Sonar 80% gate required; hosted Cloud remains pending | Successful verification-only run ID checked by local release helper; optional protected GitHub deploy mode retained |
| R12 learning/AI | AGENTS.md, docs/specs, docs/prompts; [AWS questionnaire](nodejs-aws-study-path/aws-terraform-questionnaire.md); [Node/backend questionnaire](nodejs-aws-study-path/node-backend-questionnaire.md) | check-cloud-study.py; both questionnaire validators and corrupt-input regressions; runtime lab; clean-checkout/extracted managed ZIP verification; independent section and final critics | Git publication recorded separately from local validation; live Study Desk reader unchanged |

For a new change use branch/commit naming such as `R05: preserve idempotency across retries`, then add the actual commit SHA and pull-request/workflow links to its review entry. A release records source SHA, migration versions, test-report identity and immutable image digests. The prepared AWS deploy script retains deployed digests for rollback; it is not proof of a deployment until executed.

[Jira CSV](jira-import.csv) has importable Summary, Description, Issue Type and Labels columns. In Jira map those fields in CSV import, choose your existing project, inspect the preview and import. Add returned issue keys to this table and link pull requests manually or through your configured integration. CSV creation did not access Jira.


## Cloud study extension evidence

R12 → `docs/nodejs-aws-study-path/generated/20–43` → `scripts/check-cloud-study.py` → `labs/terraform-local/run.py` and `evidence/` → independent curriculum review. These are teaching/local verification results, not AWS deployment evidence. The app imports managed guides with profile-scoped IDs and preserves personal notes/expansions/comments.


## Production dependency advisory repair

R11 → `backend/package.json` scoped override and `backend/package-lock.json` patched parser/upload dependencies → production audits, valid dependency tree, existing unit suites and unchanged real API contract → `docs/evidence/ci-security-repair/` → independent review. Hosted SonarCloud configuration/status is tracked separately in `docs/sonarqube-cloud.md`; its gate remains required when that workflow runs.


## Cost-first deployment redesign

R10 → [phased ADR and cost review](aws-cost-review-2026-10-27/README.md) → `model.py` / `rates.json` / exact scenario ledger → independent `critic_audit.py` (42 platform + six streaming cases) / `critic.md` → sanitized October 27 account and baseline-preview summaries. Cost/topology selection, hardened infrastructure, final S3-backed plan approval, cloud recovery/security/48-check execution and teardown are pending. No Jira import or new release is implied by these local requirement links.

## Selected ECS scope

R10 selection supersedes the earlier proposed SSM recommendation for preparation only. [Requirements](specs/requirements.md) → [runtime/Terraform source](../infra/aws-ecs-dev/README.md) → [local execution manifest](evidence/ecs-preparation/verification-manifest.json) → [sanitized actual plan/costs](evidence/ecs-preparation/staging-plan-cost-review.json) → [critic record](reviews.md). The new publisher validates exact-SHA GitHub/Sonar/48-API evidence and isolated ECS state before ECR writes; no AWS publication or deployment occurred. Jira import and actual deployment/release identities remain pending.

## Historical R10 free-hostname preparation checkpoint, 27 October 2026

[Free hostname guide](aws-free-test-hostname.md) → dynv6 primary CNAME/CAA/underscore documentation and public/authoritative DNS checks → owner account/zone reservation → reviewed certificate-only plan and actual ACM ISSUED → new final S3-backed infrastructure plan. The candidate is not claimed reserved. No AWS or provider records were created, no application/Terraform source changed and no free-DNS feature removes the cloud approval or security gates.

Historical checkpoint before certificate approval: R10 registered-zone checkpoint → owner-account/public DNS evidence → `infra/aws-ecs-certificate` (unchanged source) → two passing mock tests → [one-create saved certificate plan receipt](evidence/certificate-request/plan-review.json) → user approval pending → actual CNAME/ISSUED → fresh reviewed infrastructure plan. The old hostname-free preview is not an activation approval.

R10 approved certificate execution → exact reviewed plan/source/account guards → Terraform one-resource apply → actual provider CNAME → three-resolver DNS proof → live ACM ISSUED/DNS SUCCESS → no-change post-issuance plan → [execution evidence](evidence/certificate-request/issuance.json) / [independent critic](evidence/certificate-request/issuance-critic.md). Client CIDRs/final infrastructure plan and all application deployment gates remain pending.

## R10 next review — 28 October 2026

Approved client /32 and issued certificate → renewed read-only preflight → protected-state bootstrap (5 creates) / HTTPS infrastructure preview (111 creates) → exact-SKU price refresh (31 rates) / Decimal cost ledgers (12 cases) → positive plan checks + 23 HTTPS / 11 legacy adversarial controls → [review packet](aws-https-plan-review-2026-10-28.md). Actual S3 backend/final saved plan and all provisioning/application gates remain pending. The client address and raw plans/state remain private.

## Full professional cloud learning extension

R12 → lessons 44–83 and `cloud-coverage.json` → source/link/manifest validation, foundation and advanced Terraform labs, network reasoning lab, 85-guide reader/import isolation checks → independent full-curriculum review. Current project source, new illustrations, local evidence and pending deployment-owner decisions are distinct. No new cloud price or provisioned resource is claimed.


R12 setup/process teaching → `docs/nodejs-aws-study-path/walkthroughs/README.md` and chapters01–08 → managed source/link validation, archive completeness and committed-reader-link refresh → separate walkthrough critic. The companion explains recorded steps and pending gates without modifying infrastructure or personal study data.


R12 visual learning → `docs/nodejs-aws-study-path/visuals/README.md`, identity guide and nine official screenshot cards → image/provenance review, extended local-link validation, archive-byte checks and published-reader-link verification. The visual guide makes no provisioning or IAM-access change.


R12 IAM screenshot clarification → visual guide 03 and user-provided permissions-screen PNG → independent image/policy review, managed-link/ZIP validation, no IAM writes. The guide distinguishes an attached permission grant from a boundary and checks Step 1 console availability without inferring the account model from its role alone.


R12 actual console learning → visual guide 04 and signed-in project captures → independent privacy/caption review, scope-aware observation record, source/ZIP/link checks and managed reader refresh. User-completed TOTP registration is reported separately from untested sign-in challenge behavior; no authentication secrets or device/IP details are published.


R12 Terraform commands → walkthroughs 09–10 → exact local Markdown-block execution, saved-plan/action/output/cleanup assertions, cloud-template syntax and independent stubbed failure-path checks, managed-link/archive validation → separate command critic. No cloud execution, login or GitHub dispatch is performed by this documentation change.


## R10 approved state bootstrap —29 October 2026

Human exact-plan approval → immediate hash/source/provider-lock/account/absence guards → actual Terraform 5 create/0 change/0 destroy → authenticated bucket-control read-back → separate post-apply critic → [actual evidence](evidence/aws-state-bootstrap-2026-10-29/README.md) → NEW actual S3-backed application plan → separate application approval, publication/bootstrap/activation and runtime gates. Certificate local state remains separate.


## R10 actual S3-backed application plan — 29 October 2026

Approved five-resource state bootstrap → authenticated controls/post-apply critic → empty isolated real S3 backend init with account/encryption/locking safeguards → NEW exact saved application plan (111 creates) → current official tariffs/actual-quantity ledgers → strict saved-backend/source/security checks and 54/23/11 negative controls → separate fresh-context critic → [reviewable packet](aws-s3-plan-review-2026-10-29.md). Application apply, publication/bootstrap/activation, runtime acceptance and scheduled teardown remain pending separate decisions.


R12 execution journal → walkthrough11 → original owner execution/read-back evidence, actual local reviewer success before retention changes, independently observed old-artifact source-drift rejection, Bash syntax/pinned links/private fail-fast checks and fresh critic → [independent review](evidence/aws-execution-journal-review-2026-10-29.md). No new cloud mutation or iTerm automation.


## R10 visible commands and demo-data cleanup — 29 October 2026

Human request for visible iTerm commands → iTerm automation denial/no workaround → manual command helper/private transcript → 28 fake-CLI tests → actual read-only preflight stopped at client mismatch → no new plan. Human 24-hour/delete-demo-data/preserve-state choice → explicit safe-default cleanup flag → 12 mocked transition tests → [runbook and shutdown cost comparison](aws-operator-runbook-2026-10-29.md) → intended-client/shutdown decisions pending → fresh exact plan/cost/critic/apply approval. Native cleanup remains proposal-only; no timer or app resource created.


## R10 final matching saved application plan — 29 October 2026

Human explicit IP lookup/private-/32 approval → legitimate private lookup/context update → CLI/IAB match → actual preflight pass → refreshed metadata/new saved 2fd776 artifact → source/backend/security/cost review → 54 existing controls +8 independent mutants → final fresh-context critic PASS → [exact application apply package](aws-application-plan-approval-2026-10-29.md). No app apply, activation, DNS routing, actual 24h clock or teardown success yet. Retention is discard-demo-data/preserve-state; operator-assisted return and exact future cleanup/destroy approval are explicit.


## R10 actual partial failure and repair preparation — 30 October 2026

Explicit human approval of initial 2fd776 artifact → actual exit 1 and 99 completed creates/100 persisted managed instances → independent AWS/state critic FAIL → preserved errors and original T0/deadline → human-authorized repair preparation → source fixes, rejected AMI/volume-tag previews, 18 isolated Terraform mock runs → fresh exact mixed-action plan and current 31-rate/12-ledger cost packet → strict reviewer/negative controls and fresh critic → [current repair review](aws-repair-review-2026-10-30.md). Changed-plan apply, runtime controls, activation and cleanup remain separate approval/verification boundaries; no Git/Jira deployment/release success is inferred.


## R10 four-hour proposal and CI repair — October 30

Human handoff (one owner/no new reviewers) → unchanged original state/artifact/reviewer → fresh fixed-deadline proposal binary → every managed change and refresh drift identical after deadline normalization → existing strict source/backend/security/cost checks plus eight extension controls → [combined approval packet](aws-extension-repair-proposal-2026-10-30.md). No extension/apply approval inferred. Kafka failed-job evidence → local `generate_cluster_id` encoding guard → two deterministic regressions wired to Verify → [nine real TLS/SCRAM/ACL checks](evidence/aws-extension-repair-2026-10-30/kafka-local-regression.json). Hosted Verify not rerun; SonarCloud missing external configuration remains blocked. [Actual execution journal](aws-final-stretch-journal-2026-10-30.md).


## R10 approved repair output and micro residual — October 30

Direct human approval → strict immediate source/backend/account/cost/live-drift guards → exact saved apply exit1 → preserved104-resource serial7 state → actual RDS size rejection and verified ALB/TLS/log delivery/CloudMap/DNS/volume-expiry controls → documented Free micro candidate and Ohio orderability/price API receipts → one focused mock and eight residual negative controls → [eight-create saved-plan approval packet](aws-rds-micro-completion-2026-10-30.md). Deadline9:51PM EDT remains approved; no new extension, account upgrade, app activation or cleanup inferred. [Execution evidence](evidence/aws-approved-repair-apply-2026-10-30/status.json).


## R10 micro completion actual execution — October 30

Exact direct human approval → bound preapply guards/live drift match → eight-create apply exit0 →112 actual resources/no taints and unchanged104 identities → available private encrypted protected micro RDS/one-day backups/forceSSL plus seven approved alarms → full no-change plan → [sanitized execution evidence](evidence/aws-micro-completion-2026-10-30/status.json). No application/bootstrap/recovery/notification success is inferred. Approved deadline9:51PM EDT persists; current cleanup plans still require exact approval.
