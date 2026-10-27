# Independent ECS preparation critic — final review, 27 October 2026

**Verdict: ready for review as a preparation package and hostname-free local-backend staging preview. It is not approved for AWS apply, paid staging, image publication or deployment.** The user-selected private ECS/RDS + one zonal NAT design is implemented separately from the preserved EC2/SSM baseline. No owned hostname is available; the actual preview has no client ingress, ALB listener or application task definition/service. Paying for staging while waiting for DNS is unwarranted.

No AWS resource writes were performed by this critic. Critic runtime checks used disposable local fixtures, temporary source copies and mock external tools; they did not alter marketplace source/data. Local Docker/provider sockets required sandbox escalation. The original application acceptance oracle and excluded learning tools were not weakened.

## Concrete saved preview and cost verdict

Independently ran the final offline auditor against the regenerated private binary/JSON and current source. Result: **108 creates, zero changes or destroys**, account `772641336063`, region `us-east-2`, access mode `no_listener_no_client_ingress_staging`.

| Artifact | SHA256 |
|---|---|
| `work/aws-ecs-preparation/terraform/staging-preview.tfplan` | `afce0049b278669990eb2c09f511a5af6f5ccc41ecb04eaa370527fc69436591` |
| `work/aws-ecs-preparation/staging-plan.json` | `e99e17c2726003d2d35240336f308c9a4dfa4c11b551be38f1970fb45463da1e` |

Saved Terraform *.tf and provider-lock bytes match current source; the only extra saved configuration is the explicit local-backend override. Actual `terraform show -json` matches the supplied JSON. The external broker template matches the planning scratch copy and has a separate recorded hash: it is not separately embedded in the plan ZIP. This is a dirty-working-tree preparation receipt, not a committed exact-SHA release or a final S3-backed apply artifact. Changed source/inputs/account require a new plan and review.

Independently recomputed all 12 idle/expected/higher cost ledgers directly against the dated rate file, checking line products, sums and deltas from the previous candidate. Quantities agree with actual code: seven secrets including RDS master, three host custom metrics, seven alarm metrics, one NAT, one RDS instance, one private Kafka host and two ALB public-AZ addresses.

| Expected gross estimate, before credits | 24 hours | 720 hours |
|---|---:|---:|
| Actual zero-task staging preview, including KMS allowance | $6.71 | $187.40 |
| Future five-task activation, including KMS allowance; not planned here | $8.32 | $235.68 |

These are consumption assumptions, not spending caps. Staging still bills ALB/NAT/RDS/EC2 even without a visitor path. The later estimate removes the old ordinary cross-AZ backend allowance because task/broker/RDS primary traffic is in one AZ; usage outside that topology, restore rehearsals, domain registration and retained resources remain separate. The private hosted zone's nonprorated calendar-month cost remains included. Credits do not make resources free.

## Evidence independently reproduced

| Check | Actual critic result | Scope |
|---|---|---|
| ECS Terraform mocked runs | **10 passed / 0 failed** | Every AWS provider mocked; local mock applies are not AWS provisioning |
| Certificate-only Terraform mocked runs | **2 passed / 0 failed** | Nonexportable DNS certificate request only; no domain/zone/purchase |
| Backend Jest | **88 passed / 0 failed**, five suites | Includes original 64 tests plus connection, health, bootstrap and replay tests |
| PostgreSQL runtime integration | **30 passed / 0 failed** | Actual disposable PostgreSQL 17 with required TLS, temporary source build |
| Kafka runtime integration | **9 passed / 0 failed** | Actual broker CONFIG extracted from user-data, verified TLS/SCRAM/ACLs |
| Frontend DNS/configuration | **5 passed / 0 failed** | Actual nginx image; old address occupied before backend replacement |
| ECS publisher contracts | **21 passed / 0 failed** | AWS/GitHub/Docker/Trivy mocked; no publication |
| Offline plan negative controls | **10 passed / 0 failed** | Real source ZIP and binary/JSON mismatch test; rule controls stub only local show |
| Cost audit | **12 ledgers agree** | Independent arithmetic using saved rates and topology deltas |
| Broker syntax | Shell syntax and embedded Python compile passed | Does not establish AL2023/systemd/CloudWatch execution |

The PostgreSQL drill proves four verified-TLS owned logins, all twelve cross-service CONNECT denials, initial/idempotent DB bootstrap and checksummed migrations, plaintext/wrong-CA/wrong-hostname rejection, controlled outbox metadata replay preserving event IDs/payloads, one durable inbox effect on repeated events, and CLI/server-log password nondisclosure. Kafka checks prove producer/consumer success plus wrong password/CA/hostname/plaintext/anonymous operation denial and consumer publish ACL denial. Anonymous TCP connection alone was correctly rejected as an insufficient test; the final negative sends a real operation.

The critic also reviewed fresh running-marketplace evidence: **exactly 48 API passes/zero failures**, two browser journeys and nine dependency failure/recovery checks. The root ran these marketplace-changing checks; the critic did not repeat them against user data. Published frontend unit evidence reports 28 passes and release-contract evidence reports 49 total including legacy controls. The unchanged acceptance script blob remains `8a8204006737aa67187ed8e9189b4f08a4072a2f` (SHA256 `c1944f25a05ae7ed076c632bc3d8177495e1bde456c3eed74095170e67f4fb9d`). Historical reports were not substituted for the current results.

## Material findings repaired through review

1. **An empty broker secret stranded first boot.** Initial user-data exited permanently before secret population. The repaired boot-ordered systemd one-shot retries every 30 seconds and reuses encrypted Kafka storage. Real AL2023 boot/reboot remains a cloud gate.
2. **Gateway S3 policy could block bootstrap despite NAT.** The policy now includes official AL2023 repository and ECR starport buckets. Gateway routes take precedence over NAT. Operations uploads remain an external approved operator path; runtime roles receive no general S3 access.
3. **TLS options and password logs needed hardening.** `pg` SSL URI overrides are rejected; ECS requires explicit verified TLS/CA and field-based DB credentials. Failed role SQL carries password literals, so RDS uses `log_statement=none` and `log_min_error_statement=panic`; real local server logs were checked for generated passwords.
4. **Messaging readiness could evict durable inquiry serving.** Task routing health now uses DB-dependent `/health/serve`; strict `/health/ready` retains messaging diagnostics. The contract and tests preserve this distinction.
5. **Host-network Kafka could obtain instance-profile credentials.** Hop limit alone does not isolate host-network containers. A UID1000 IMDS denial guard now precedes Docker at boot, capabilities are dropped and IPv6 IMDS is disabled. The actual EC2 negative/reboot test remains mandatory.
6. **The first cost model no longer matched source.** Seven actual secrets, three custom host metrics and seven alarms replace five/eight/ten. The revised ledger also distinguishes zero-task staging from later activation and states retry/request assumptions.
7. **The first saved plan was stale.** Its data.tf snapshot predated password-log protection. The regenerated binary now matches current *.tf/lock; the external template is separately bound to scratch/source.
8. **The first offline reviewer accepted an unsafe inline public SSH rule.** The critic reproduced exit zero on a temporary mutated plan. The repaired reviewer rejects inline/legacy SG rules, checks ports independently of unknown SG IDs, compares source/lock snapshots and actual binary-derived JSON, and refuses optimized Python. Ten executable negative controls retain the regression.

## Source, security and release assessment

Actual code has two public ALB subnets in distinct AZs, two private DB subnets, one active app/broker AZ and one zonal NAT. Current staging has zero CIDR ingress/listeners/tasks. Later HTTPS configuration requires hostname, same-account Ohio certificate, narrow approved CIDRs and immutable image digests; there is no HTTP fallback. SG trust follows ALB→frontend→four APIs, inquiries→catalog, APIs/bootstrap→RDS and inquiries/notifications→TLS Kafka. Private HTTP hops are documented accurately; this is not end-to-end TLS. Outbound HTTPS uses destination `0.0.0.0/0`, not an internet service allowlist; broker installation alone adds TCP80.

Five separate Fargate capabilities, owned DB credentials, separate execution/application roles and separate producer/consumer identities preserve boundaries. Ordinary tasks cannot fetch RDS master or broker-private-key secrets and have no application AWS policy. The privileged bootstrap task alone receives master plus owned DB passwords. Empty/default staging does not invent image references or start demo accounts.

The image publisher retains clean main/exact repository/SHA, verification-only successful CI, unchanged 48-pass evidence, explicit Sonar coverage/violation/duplication conditions, isolated ECS S3 state, matching account/region, immutable ECR tags, amd64/Linux/source-label checks and scans of actual digests. It never invokes ECS, SSM or Terraform apply. Mock publication success is not real publication/scanning evidence. CI additions keep deployment separate; hosted execution for this new source remains pending.

Read the complete runbook, requirements/contract/results/review/traceability changes and evidence boundaries. The hostname→certificate→final-plan→publication→bootstrap→activation sequence requires distinct reviewable approvals. Recovery documents write freezing, a coordinated four-DB point, replay identities/deduplication and data-loss boundaries. Teardown accounts for protected RDS/snapshots, versioned S3, secret recovery windows, images/logs/state and delayed billing. No excluded study-path/import tool or original baseline infrastructure was changed. IAM Autopilot's three local drafts have 12 unresolved wildcard warnings and were not attached or accepted as an operator policy.

## Largest remaining gap and approval boundary

**The largest remaining gap is live execution of this topology after an owned hostname/issued certificate, approved CIDRs, exact-source hosted verification/images and a newly reviewed final S3-backed plan.** This is an execution gate outside preparation authorization, not a reason to provision speculative staging.

Before any deployment claim, prove actual account permissions, private reachability/TLS and role denial, AL2023 bootstrap/metadata guard and reboot behavior, supported RDS version/capacity, task memory/load and connection headroom, Cloud Map replacement in AWS, metrics and alarm transition/delivery, visible outbox backlog, live broker outage/replay, isolated restore with measured RPO/RTO, bad-release rollback, full 48-check AWS smoke and destroy/residual inventory. Seven configured alarms and optional existing-topic actions do not prove delivery; no destination/message was created. The DB pool permits ten connections/process, so rolling overlap can mean 80 API pool connections plus bootstrap/operator headroom.

ECS circuit-breaker rollback requires a prior completed deployment. Image rollback cannot undo destructive schema changes, secret rotation, lost topics or writes absent from the recovery point. Kafka's terminated root disk and retention limits require deliberate replay/recovery; local replay proof does not measure cloud RPO/RTO. Expiry tags and budget notifications are not hard stops.

**Recommendation:** present the source, sanitized current cost/plan summary and this evidence for review. Keep the private binary/JSON ignored. Obtain a hostname before any paid infrastructure step; do not apply this local preview. No remaining preparation source defect was found after the repairs above. Refresh the published verification-manifest hashes/counts to the frozen source before delivery; the actual final plan/hash checks in this report already pass.

## Primary references rechecked

[ECS circuit breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html), [ECS discovery](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-discovery.html), [Fargate networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html), [RDS PostgreSQL TLS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html), [RDS master secrets](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html), [ALB target SGs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html), [AL2023 repositories](https://docs.aws.amazon.com/linux/al2023/ug/managing-repos-os-updates.html), [CloudWatch procstat](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-procstat-process-metrics.html), [PostgreSQL 17 logging](https://www.postgresql.org/docs/17/runtime-config-logging.html), [ACM pricing](https://aws.amazon.com/certificate-manager/pricing/).

## Appendix — Linux CI PostgreSQL fixture repair

The first hosted Verify run `40586119114` failed while waiting for the disposable PostgreSQL fixture. That run is not a successful overall verification. The repair is confined to `scripts/aws-ecs-runtime-integration.py`: before the entrypoint drops privileges, root now copies the HBA file alongside the TLS files into `/tmp`, sets ownership to the image's PostgreSQL user and makes the HBA/key mode 0600. PostgreSQL references `/tmp/pg_hba.conf`. The shell now uses `set -eu` so copy/ownership failures cannot silently continue. None of the 30 test assertions or application/Terraform configuration changed for this repair.

Independently reproduced the failure mechanism inside the pinned PostgreSQL image on its native Linux filesystem: fixture directory owner UID/GID1001, mode0700; HBA file owner1001, mode0644; image PostgreSQL UID/GID70. `gosu postgres cat` on the original path failed with `Permission denied`. Copying the HBA into `/tmp`, assigning owner70:70 and mode0600 made the same read succeed. This establishes the directory-traversal mismatch that a host-private Linux bind mount preserves; macOS Docker sharing had concealed it. An initial diagnostic assumed `su-exec`; the pinned image actually provides `gosu`, and the corrected diagnostic passed.

Independently reran the repaired complete drill in a temporary source copy: **30 passed, zero failed**, including verified TLS, all twelve cross-DB denials, bootstrap/migration idempotence, negative TLS, replay/deduplication and CLI/server-log password checks. The temporary container/files were cleaned. No marketplace data or AWS calls were involved. Preparation-readiness verdict is unchanged; a new successful hosted Verify run is still required before claiming CI success or publishing images.


## Appendix — KMS API accounting correction

The earlier totals omitted API requests on AWS-managed KMS keys while correctly excluding customer-managed key-month charges. Current [AWS KMS pricing](https://aws.amazon.com/kms/pricing/) explicitly distinguishes free managed-key creation/storage from chargeable managed-key API use. The saved Ohio `kms_api` tariff is $0.000003/request ($0.03/10,000). This correction changes accounting only: Terraform source, the 108-create plan, binary hash and JSON hash above are unchanged.

Independently checked `work/aws-ecs-preparation/kms-inclusive-review.json` and recalculated all twelve cases without importing the builder model. Every case contains exactly one KMS allowance line; quantity × saved rate, every other line product, final sum and delta from the previous non-KMS ledger agree. The allowance is:

- Staging: 150 modeled Secrets reads/hour plus 100 storage/lifecycle calls per 24 hours. That is 3,700 calls/$0.01110 for 24h or 111,000 calls/$0.33300 for 720h.
- Later activation: 70 modeled Secrets reads/hour plus the same storage/lifecycle allowance. That is 1,780 calls/$0.00534 for 24h or 53,400 calls/$0.16020 for 720h.

The ledger clearly labels this **conservative, unmeasured usage**, rather than actual KMS telemetry or a one-to-one billing guarantee. Empty-secret failures may never decrypt; service caching and lifecycle behavior vary. The arbitrary 100-call/day buffer is an assumption, not capacity proof or an upper bound. No customer-managed key-month charge is added. The shared 20,000-request monthly allowance is deliberately not deducted because its availability to this project is unverified.

Corrected expected gross totals are **$6.71/24h and $187.40/720h for staging**, and **$8.32/24h and $235.68/720h for future activation**. These supersede the earlier KMS-exclusive figures; the main comparison above has been updated. Publish matching ledgers/docs/manifests together. Preparation-review verdict and all approval boundaries are unchanged; no AWS API or mutation was required for this audit.
