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
| R10 AWS dev | infra/aws-dev (local-login/GitHub modes), scripts/aws-* | Five dev and two bootstrap mock runs pass; account-specific bootstrap plan and local-backend dev preview prepared; final S3-backed plan/apply/cloud smoke pending approval | Selected us-east-2 dev; source/digest manifest and exact SSM command/48-check report required; [preparation boundaries](results.md) |
| R11 toolchain | .github, .vscode, sonar-project.properties, compose.ci-quality.yaml, scripts/sonar-ci.mjs | Prior local/Verify gates pass; fresh exact-SHA verification with isolated CI Sonar 80% gate required; hosted Cloud remains pending | Successful verification-only run ID checked by local release helper; optional protected GitHub deploy mode retained |
| R12 learning/AI | AGENTS.md, docs/specs, docs/prompts, guides | independent critic; docs link check; interview rehearsal | docs/releases/current.json |

For a new change use branch/commit naming such as `R05: preserve idempotency across retries`, then add the actual commit SHA and pull-request/workflow links to its review entry. A release records source SHA, migration versions, test-report identity and immutable image digests. The prepared AWS deploy script retains deployed digests for rollback; it is not proof of a deployment until executed.

[Jira CSV](jira-import.csv) has importable Summary, Description, Issue Type and Labels columns. In Jira map those fields in CSV import, choose your existing project, inspect the preview and import. Add returned issue keys to this table and link pull requests manually or through your configured integration. CSV creation did not access Jira.


## Cloud study extension evidence

R12 → `docs/nodejs-aws-study-path/generated/20–43` → `scripts/check-cloud-study.py` → `labs/terraform-local/run.py` and `evidence/` → independent curriculum review. These are teaching/local verification results, not AWS deployment evidence. The app imports managed guides with profile-scoped IDs and preserves personal notes/expansions/comments.


## Production dependency advisory repair

R11 → `backend/package.json` scoped override and `backend/package-lock.json` patched parser/upload dependencies → production audits, valid dependency tree, existing unit suites and unchanged real API contract → `docs/evidence/ci-security-repair/` → independent review. Hosted SonarCloud configuration/status is tracked separately in `docs/sonarqube-cloud.md`; its gate remains required when that workflow runs.
