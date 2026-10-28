# Results and verification boundary

## Current plan preparation — 28 October 2026

The owner approved one HTTPS client /32 for planning, not provisioning. Read-only checks after temporary-login renewal confirm Free/ACTIVE/$100 credits, the existing certificate ISSUED and no app infrastructure in queried scopes. Prepared a source-bound five-create state-bootstrap plan plus a 111-create HTTPS local-backend infrastructure preview with no app tasks. [Actual review packet](aws-https-plan-review-2026-10-28.md). No AWS writes occurred today.

All 31 selected rates/units remain unchanged. Current probe stage expected $6.83/24h/$191.22 per 720h includes TLS/403/503 allowance; future five-task activation remains $8.32/$235.68 plus recovery. Shared S3 costs explicitly allocate state within existing totals. Both real valid plan fixtures pass the reviewer; 23 HTTPS and 11 legacy negative controls reject unsafe variants. The fresh critic checks actual binaries/source, privacy, security graph and all 12 cost ledgers. [Evidence index](evidence/aws-https-plan-2026-10-28/README.md).

No app/infra definitions were changed. The final S3-backed saved plan cannot exist until approved state bootstrap, then needs new cost/source/input review before provisioning. Neither the historical no-listener plan nor today's local preview is an apply approval. The planning expiry proposal must be refreshed at the actual agreed start; no demo timer has started.

## Historical ECS preparation — 27 October 2026

The owner selected private ECS/RDS + one NAT for plan review. **Only the separately approved ACM certificate has been created; no application infrastructure is deployed.** The historical local-backend preview proposes 108 creates, no changes/destroys, no listener, no client ingress and no app task definitions/services; it predates the registered hostname/issued certificate and is not an activation plan. Expected gross staging cost is $6.71/24h or $187.40/720h. Future five-task activation is $8.32/24h or $235.68/720h plus recovery exercises; it is not in this plan. [Itemized current plan/cost summary](evidence/ecs-preparation/staging-plan-cost-review.json).

Fresh local execution passes source checks/builds, 88 backend tests, 28 frontend tests, all unchanged 48 API checks, two browser journeys, nine dependency recovery checks, 30 real PostgreSQL TLS/ownership/migration/replay/log-redaction checks, nine real Kafka TLS/SCRAM/ACL checks, five nginx DNS/configuration checks, 10 ECS + two certificate Terraform mock runs, and all 49 release contracts. [Source hashes and verification manifest](evidence/ecs-preparation/verification-manifest.json), [PG](evidence/ecs-preparation/postgres-tls-ownership-replay.json), [Kafka](evidence/ecs-preparation/kafka-tls-scram-acl.json), [DNS](evidence/ecs-preparation/frontend-dns.json), [API](evidence/ecs-preparation/local-acceptance.json), [browser](evidence/ecs-preparation/browser-smoke.json), [recovery](evidence/ecs-preparation/failure-drill.json), [publisher contracts](evidence/ecs-preparation/release-contracts.txt), [plan negative controls](evidence/ecs-preparation/plan-negative-controls.json). Historical evidence below is retained at its original paths.

The offline reviewer compares saved *.tf/provider lock bytes against current source, requires JSON to match the actual saved binary, checks the external broker template against the planning scratch copy, rejects inline/legacy SG rules and enforces allowed protocol/port/CIDR shapes. Template bytes are not a separate embedded file in the plan ZIP; their current hash is recorded separately. A changed source/input needs a new plan/review. IAM Autopilot produced three local policy drafts with 12 wildcard warnings; none was attached or approved.

The separate critic checks preparation readiness, not cloud readiness. At source publication, hosted CI was pending; consult [current Verify runs](https://github.com/robertovalencia/linked-in-node-and-aws/actions/workflows/verify.yml) and [verification-only release runs](https://github.com/robertovalencia/linked-in-node-and-aws/actions/workflows/deploy-dev.yml) for actual outcomes. A final S3-backed plan, actual image publication/scans, approved client CIDRs, bootstrap, live cloud health/security/metrics/alarm delivery, recovery RPO/RTO, rollback and full AWS API smoke remain unverified. The preserved EC2/SSM deploy=true workflow is not an ECS deployment path. Use deploy=false for verification. See [the exact next steps](aws-ecs-dev.md). No timer or teardown job has started.

## Approved certificate execution — 27 October 2026

The exact saved certificate plan was applied after the user's explicit yes: **one added, zero changed/destroyed**. The only resource is a nonexportable public ACM certificate for `app.linked-in-node-rv.dynv6.net`, in account `772641336063` in Ohio. The actual validation CNAME was saved through the provider UI and independently resolved at the authoritative server, `1.1.1.1` and `8.8.8.8`. Live ACM reports ISSUED/DNS SUCCESS; a post-issuance Terraform plan has no changes. [Sanitized evidence](evidence/certificate-request/issuance.json) and [independent critic](evidence/certificate-request/issuance-critic.md). No credentials/private keys, state, raw plans, personal email or apex address were copied into this evidence.

The certificate has no additional ACM fee, is not attached to an AWS service and is currently ineligible for renewal while unused. It does not prove ALB HTTPS/application operation. Preserve its ignored local state until deliberate migration or reviewed destruction; live ACM status is authoritative over request-phase state metadata. No 24-hour deadline for billable resources has started. Client CIDRs, state bootstrap/final S3 plan, exact-source images/bootstrap, paid-resource approval and all cloud security/health/recovery/smoke/rollback gates remain pending.

## Historical migration and earlier baseline preparation

The application results below were produced for this Node/React migration on 21 October 2026. AWS preparation status was updated on 23 October 2026 and is reported separately. The reference repository supplied contracts and the 48-check acceptance suite, but its old test reports were not reused as evidence. Read the linked raw reports to distinguish an executed check from a prepared integration.

| Gate | Executed result | Evidence |
|---|---|---|
| Source checks and builds | TypeScript, ESLint, Prettier and both production builds pass | [source check](evidence/source-check.txt), [build](evidence/build.txt) |
| Backend unit tests | 64/64 Jest tests pass; 95.44% backend line coverage | [backend test log](evidence/backend-tests.txt) |
| Frontend component and hook tests | 28/28 Vitest tests pass; 81.13% frontend line coverage | [frontend test log](evidence/frontend-tests.txt) |
| Reference API behavior | 48/48 adapted executable checks pass against the running local stack | [acceptance report](evidence/local-acceptance.json) |
| Adversarial backend behavior | 8/8 independent probes pass, including concurrent idempotency, changed-payload conflict and ownership denial | [adversarial report](evidence/backend-adversarial.json) and [database invariants](evidence/backend-db-invariants.json) |
| Dependency and application recovery | 9/9 local restart and replay checks pass | [failure drill](evidence/failure-drill.json) |
| Desktop and mobile user journeys | 2/2 real-browser smoke journeys pass on the nginx-served stack, covering discovery, compare, profile, login and durable inquiry | [browser report](evidence/browser-smoke.json) and [screenshots](evidence/browser/desktop-discovery.png) |
| Local SonarQube | Fresh evaluated gate **OK**: new-code coverage 82.3% against the unchanged 80% threshold, new duplication 0%, new violations 0; analysis ID `bff6bec1-c67f-4b1b-900e-fc63d704c5ea` | [gate](evidence/sonar-gate.json), [issues](evidence/sonar-issues.json), [scan log](evidence/sonar-scan.txt) |
| AWS definitions, original local evidence | Both Terraform roots validate; original mocked security plan passes. Fresh preparation now passes five aws-dev mock runs and two bootstrap mock runs; no live resources are created by mocks | [Original Terraform log](evidence/terraform.txt); current preparation described below |
| Remote release control flow | 2/2 fake-CLI success/rollback fixtures pass | [orchestration report](evidence/infra-remote-orchestration.json) |

The local SonarQube 82.3% is its **new-code** metric for this Git-aware analysis. A fresh scan initially failed at 62.6%; new behavior and failure-path tests raised the unchanged gate to passing. The [failed baseline](evidence/sonar-gate-failed-git-baseline.json) and final analysis ID make the correction traceable. Backend unit line coverage is 95.44%, while the 48 real HTTP checks and restart drill additionally exercise the running stack. The two browser journeys do not establish full visual or assistive-technology parity.

The first restart drill failed because nginx held stale container IPs after service recreation. The repair and passing rerun are both retained in [failure evidence](evidence/failure-drill-before-edge-repair.json) and [final evidence](evidence/failure-drill.json). The first remote release fixture exposed a relative secret-cleanup trap; its failing and repaired reports are [here](evidence/infra-remote-orchestration-before-repair.json) and [here](evidence/infra-remote-orchestration.json). These are corrections, not inherited success claims.

## Predeployment runtime image repair

The old backend runtime image failed the local High/Critical scan with 59 findings. A newly built amd64 image using the current digest-pinned official Node 22.23.4/Alpine 3.24 base and excluding unused runtime package managers passes the unchanged Trivy gate with zero High/Critical findings. A non-root runtime/dependency/scrypt probe also passes. [Exact evidence and hashes](evidence/backend-runtime-image-security.json) distinguish this local image result from fresh CI, complete HTTP acceptance, and AWS deployment, which require separate execution.

## External environments

The AWS Free plan account preflight reported **$100 available credits**. Live `us-east-2` discovery confirmed `m7i-flex.large` as Free Tier eligible (2 vCPU, 8 GiB), and resolved Amazon Linux 2023 x86_64 AMI `ami-053ef5d7ebe355f4a`. The account denies IAM OIDC-provider operations through an AWS-managed service control policy. The user selected GitHub verification plus release from a temporary local AWS login; Terraform's `enable_github_deployment=false` omits the deploy IAM role/policy while preserving host IAM/SSM controls. The optional OIDC mode remains available for an eligible account.

Two actual account-specific plans were prepared in ignored `work/aws-preparation/` without applying them:

| Prepared plan | Result | SHA256 | Approval boundary |
|---|---|---|---|
| Bootstrap bucket-only `bootstrap.tfplan` | 5 creates, 0 changes, 0 destroys; no OIDC provider | `cb8f09b28cd62261787f5e4bdea66c91ac3192acbc6e8e068fe6a96424af625f` | Requires approval before apply |
| Dev local-backend preview | 21 creates, 0 changes, 0 destroys in `us-east-2` | `70713543d3147f418a4782b7e458af10a0dddd08125971da9669b103008f002c` | Preview only; regenerate the final S3-backed saved plan after approved bootstrap |

No provisioning, ECR publication, SSM deployment, live AWS smoke test, or live rollback has occurred. The user selected **24 hours**; the historical core-only official-price model was approximately **$2.54 of credits** for core infrastructure including modeled 1 GB ECR storage, plus variable usage. The exact deadline starts at provisioning. No teardown is scheduled. See [costs](costs.md), [deployment](aws-dev.md), and [cleanup](short-run.md). Changes to source/inputs/account require a fresh plan, hash, and review; these recorded hashes are historical preparation evidence, not permission to apply a changed plan.

The most recently recorded GitHub Verify result before this preparation passed at [run 39699975809](https://github.com/robertovalencia/linked-in-node-and-aws/actions/runs/39699975809). This does not establish a pass for the new deployment changes. The [hosted SonarQube job](https://github.com/robertovalencia/linked-in-node-and-aws/actions/runs/39647580308) remains configured but pending because the Sonar Cloud organization/project identifiers and token have not been supplied. `SONAR_HOST_URL` is set to the Free EU service. The isolated CI SonarQube path has executed locally: fresh analysis `7be54378-5633-46f4-8700-aec2002b955a` passed with overall coverage 82.3%, duplication 0%, and zero violations. The negative run `2829da92-911c-4fac-8dbd-c7d37e646606` failed with 0% overall coverage against the unchanged 80% threshold. Its new-code Sonar Way conditions are copied unchanged; equivalent overall conditions are added because a fresh server has no new-code baseline. These local isolated runs are not GitHub execution evidence. The fresh verification-only GitHub run and temporary-login release remain pending. GitHub protected environments, Jira import and AWS deployment remain unverified. The [hosted Sonar guide](sonarqube-cloud.md) gives the exact setup. The evaluated local SonarQube gate is separate from the hosted job. The [independent review record](reviews.md) names each critic's verdict and remaining limits.


## Dependency security maintenance, 2026-10-26

New upstream advisories caused the existing production audit to fail with four high findings through two vulnerable transitive packages. Express now resolves body-parser 2.4.0; a narrowly scoped override selects Multer 2.5.0 for the still-current NestJS Express adapter 12.2.0. Application and test source are unchanged. See [repair rationale and removal criteria](dependency-security.md).

| Executed local check | Actual result | Evidence |
|---|---|---|
| Production backend audit | Four high findings before; zero findings after | [before](evidence/ci-security-repair/audit-before.json), [after](evidence/ci-security-repair/audit-after.json) |
| Root/frontend production audits | Zero findings | [root](evidence/ci-security-repair/root-audit.json), [frontend](evidence/ci-security-repair/frontend-audit.json) |
| Frozen npm install and installed graph | Pass; only the two package entries changed; no invalid dependency/peer result | [install](evidence/ci-security-repair/final-backend-ci.txt), [tree](evidence/ci-security-repair/resolved-tree.txt) |
| Backend types/lint/format, unchanged tests and build | Pass; all 64 tests pass | [checks](evidence/ci-security-repair/backend-check.txt), [tests](evidence/ci-security-repair/backend-tests.txt), [build](evidence/ci-security-repair/backend-build.txt) |
| React checks/tests/build | Pass; all 28 tests pass | [checks](evidence/ci-security-repair/frontend-check.txt), [tests](evidence/ci-security-repair/frontend-tests.txt), [build](evidence/ci-security-repair/frontend-build.txt) |
| Rebuilt local Node runtime | All 48 unchanged API checks pass | [build](evidence/ci-security-repair/image-build.txt), [start](evidence/ci-security-repair/container-start.txt), [API](evidence/ci-security-repair/acceptance.json) |
| Compressed request compatibility and rejection | Four bounded gzip/login/error/liveness checks pass; identity container retained its ID and restart count zero | [parser report](evidence/ci-security-repair/parser-smoke.json) |

These records establish the listed local checks, not universal immunity to denial of service. The parser smoke is not a reproduction of every upstream advisory condition. Audits depend on current advisory data. Fresh hosted Verify must be assessed against the published repair revision separately. The hosted SonarCloud job still lacks actual organization/project/token settings, and its fail-closed configuration gate remains unchanged. The owner must complete SonarCloud sign-in/terms and any repository-access setup; no credentials, account settings, or cloud resources were fabricated or bypassed.
