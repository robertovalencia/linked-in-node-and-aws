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
| R10 AWS dev | infra/aws-dev, scripts/aws-* | Terraform validate/mock tests; actual plan/cloud smoke pending account/approval | AWS environment dev, digest release manifest |
| R11 toolchain | .github, .vscode, sonar-project.properties | local gates; actionlint; remote CI/Sonar pending setup | Protected dev environment and workflow run |
| R12 learning/AI | AGENTS.md, docs/specs, docs/prompts, guides | independent critic; docs link check; interview rehearsal | docs/releases/current.json |

For a new change use branch/commit naming such as `R05: preserve idempotency across retries`, then add the actual commit SHA and pull-request/workflow links to its review entry. A release records source SHA, migration versions, test-report identity and immutable image digests. The prepared AWS deploy script retains deployed digests for rollback; it is not proof of a deployment until executed.

[Jira CSV](jira-import.csv) has importable Summary, Description, Issue Type and Labels columns. In Jira map those fields in CSV import, choose your existing project, inspect the preview and import. Add returned issue keys to this table and link pull requests manually or through your configured integration. CSV creation did not access Jira.
