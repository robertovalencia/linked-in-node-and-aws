# AWS cost-first architecture review — 27 October 2026

**Recommendation: use phase A, the hardened EC2/SSM host, for the first 24-hour demonstration.** Expected gross AWS use is **$3.21**, plus approximately **$0.11** for a separate one-hour host restore rehearsal. Plan roughly **$4** with a 20% allowance under these assumptions. This allowance is not a spending cap. Keep ALB/TLS, private ECS/RDS, and managed streaming as separate later exercises with fresh cost and plan reviews.

No topology decision has been approved. No infrastructure implementation, AWS mutation, upgrade, paid-service enablement or public exposure was performed for this review. The 24-hour clock has not started. The 30-day figures below are a comparison, not a proposed run duration.

## Read the evidence

- [Cost comparison: idle, expected and higher use](tables.md).
- [Itemized meters for every option](line-items.md); [all exact quantities/results](comparison.json).
- [Phased architecture decision, diagrams, traffic matrix, security/recovery acceptance and rollback/cleanup](architecture.md).
- [Regional rates, dates, SKUs and sources](rates.json); [RDS/MSK/observability research and minimums](research-msk-rds.md).
- [Executable Decimal cost model](model.py); [independent critic](critic.md).
- [Current read-only account evidence](account-summary.json); [fresh baseline plan summary](baseline-plan-summary.json).

## Current account and deployment findings

Authenticated checks on **27 October 2026, after 20:11 UTC**, confirmed account `772641336063`, selected deployment region `us-east-2`, **Free plan / ACTIVE / $100 remaining credits**, expiring **21 April 2027 at 17:52 UTC**. Free Tier usage returned no active entries; that is not an authoritative zero-cost invoice. The `m7i-flex.large` discovery result is Free Tier eligible, with 2 vCPU/8 GiB. The standard EC2 On-Demand and Fargate On-Demand quotas are now 64 vCPU each; the previous report's quota is historical.

No project resources were found in the queried scopes: project-tagged VPC/EC2/volumes/NAT/endpoints, project-named ECR/S3, and regional ECS/RDS/ALB inventories. An additional unfiltered Ohio EC2 query found zero nonterminated instances. This is scoped evidence, not an all-service/all-region bill audit: Project-tagged EBS snapshots and project-named secret metadata (including pending deletion) were also empty; the host role was absent and unfiltered Ohio allocated public addresses were zero. Untagged snapshots/secrets and other services/regions were not exhaustively inventoried. MSK inventory and IAM OIDC-provider reads both returned explicit managed-SCP denials; denied reads do not establish empty inventories. No restrictions were bypassed.

Ohio and Virginia CloudWatch Logs listings succeeded. Therefore the Ohio no-NAT candidate is not rejected on read access alone, but `DescribeLogGroups` does not prove `CreateLogGroup` or `PutLogEvents` permission. Validate the intended log writes in the approved deployment; if policy requires Virginia logging, reprice the egress/collection path rather than assuming an Ohio endpoint reaches Virginia.

The [current account-experience service list](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html) includes ECS, RDS, ELB and VPC in Free, and MSK in Paid. Thus MSK remains a **cost comparison only** for this Free account. Credit balance, regional availability and read access do not prove every create action is permitted. A Paid upgrade alone would not resolve this account's OIDC restriction. Advanced activation is outside scope and removes project spend limits. [AWS account controls](https://docs.aws.amazon.com/accounts/latest/reference/activate-advanced-features.html)

The earlier verification-only GitHub deployment workflow [completed successfully](https://github.com/robertovalencia/linked-in-node-and-aws/actions/runs/39973901965) for source `9bb8851`. That is historical source verification, not an AWS deployment and not verification of today's source `8b2c3e0`.

## What each complete option contains

| Option | Compute, data and ingress | Learning value and limit |
|---|---|---|
| 0 Current baseline | One `m7i-flex.large`, 40 GiB gp3, public IPv4 for outbound, zero SG ingress, SSM tunnel, four Nest services/frontend/PostgreSQL/Kafka on host | Existing source, without proposed centralized operations improvements; single host/AZ and root-disk failure boundary |
| 1 / phase A | Baseline plus bounded centralized logs, three custom metrics/five alarms, logical backups/restore and identity review | Recommended first lab; no new ingress, no HA claim; improvements still proposed |
| 2 / phase B | Phase A plus internet-facing ALB in two AZs, two minimum ALB IPv4s, approved-client HTTPS, ALB SG → frontend only; original host retains outbound IPv4 | Real certificate/routing/SG teaching. DB/Kafka still share host; this does not demonstrate network DB isolation or availability |
| 3 / phase C | Five private Fargate tasks: four backend and one frontend, each 0.25 vCPU/0.5 GiB; RDS `db.t4g.small`, 20 GiB gp3, four owned DBs/logins; **dedicated private Kafka EC2 host remains**; ALB; one NAT | Separates compute/data and permits real app-SG → DB-SG trust; one active app AZ/Single-AZ DB/Kafka remain recovery compromises |
| 3e | Same compute/data as 3; six interface endpoints in one active AZ plus free S3 gateway instead of NAT | Complete named AWS API paths, no general internet; requires baked/maintained host AMI and images, and proven same-region logs access |
| 3r / 3re | Two replicas of each Fargate service across two AZs; RDS Multi-AZ standby; two NATs or twelve interface endpoint-AZs | Better app/DB availability, **Kafka EC2 remains a single point of failure**. Do not call this end-to-end HA; managed/multibroker Kafka is a further decision |

Fargate sizing and RDS connection capacity are unbenchmarked cost inputs. Kafka retains the original 8-GiB instance and 40-GiB disk conservatively; downsizing needs performance and account-eligibility evidence. It is not silently removed after moving databases. No public IPv4s are assigned to tasks, RDS or private Kafka. ALB minimum two IPv4s may grow with scaling; the estimate assumes that minimum.

The private-service candidate explicitly prices ECS-managed Cloud Map DNS discovery: one private namespace/hosted zone and five or ten registered task resources. Clients and nginx must refresh DNS on TTL/task replacement. No Service Connect proxy, service mesh, EFS, RDS Proxy or extra telemetry sidecars are assumed. Those alternatives require resources and repricing. The frontend still proxies to four capability endpoints; task IPs are not stable.

## Calculation and workload assumptions

All money arithmetic uses Python `Decimal`. Run `python3 model.py` from this folder; no AWS credentials or dependencies are needed. Runtime durations are **24 and 720 hours**. Monthly storage, secret, metric and alarm rates use a stated **730-hour normalization**, so 720-hour costs are not a claim about a calendar-month invoice. Some AWS examples instead use a 30-day month; actual billing proration can differ. Units follow the official rate dimensions; binary GiB capacity is used where AWS documents it. No Savings Plans, Reserved Instances, Spot, credits or shared free allowances are deducted.

| Consumption input | Idle | Expected | Higher sensitivity |
|---|---:|---:|---:|
| Standard logs ingested per hour | 0.001 GB | 0.04 GB | 0.5 GB |
| Private AWS API/image/log/secret traffic per hour | 0.01 GB | 0.25 GB | 5 GB |
| Internet response bytes per hour | 0.001 GB | 0.05 GB | 1 GB |
| Charged internal cross-AZ bytes per hour | 0 GB | 0.05 GB | 1 GB |
| ALB processed bytes/hour | 0.001 GB | 0.1 GB | 2 GB |
| New TLS connections/second | 0.01 | 1 | 50 |
| Active connections/minute | 5 | 100 | 1,000 |
| Requests/hour (WAF add-on only) | 10 | 3,600 | 180,000 |
| Billable RDS backups above allowance | 0 GiB | 5 GiB | 20 GiB |
| RDS surplus CPU credits per primary vCPU-hour/hour | 0 | 0 | 0.5 |

These are financial scenarios, not a traffic forecast or load-test result. The higher platform case holds task counts/disks fixed while varying log, egress and burst costs; it does not prove those sizes can sustain the workload. Platform Kafka and PostgreSQL retain a small synthetic dataset within the host disk; private AWS API traffic is **not Kafka ingest**. Before a real run, enforce bounded Kafka/log retention, disk headroom and database growth alarms. The existing Compose broker does not establish a safe retention limit. A larger-data scenario requires larger storage and a new estimate. The optional MSK higher case below is a distinct streaming workload.

ALB LCUs use the maximum of new connections/25, active connections/3,000, GB processed/hour, and rule evaluations/1,000. Ten or fewer listener rules, ordinary RSA≤2K/ECDSA≤256 certificates, no mTLS trust store and no LCU reservations are assumed. Health checks and deployment retries can increase metered traffic. [ALB price rules](https://aws.amazon.com/elasticloadbalancing/pricing/)

Logs retain seven days; storage is conservatively charged as if the full retained window occupied space throughout, without assuming compression savings. Five times ingestion volume is queried. Host adds three custom metrics/five standard alarm metrics; ECS adds eight/ten. High-cardinality dimensions, dashboards, Container Insights, detailed EC2 monitoring and traces are excluded. The CloudWatch agent itself has no extra license fee; ingested data and emitted custom metrics cost money. Alerts are proposed; notification delivery has not been configured or priced into these totals and needs a chosen destination/count before implementation.

## Major regional price inputs

Official regional catalogs were retrieved on 27 October 2026; publication/effective dates and SKUs are in `rates.json`. The EC2 website's Ohio Linux dataset was published 23 October. Storage/NAT/transfer were separately refreshed through the authenticated public Price List Query API. Public catalogs are list prices, not account discounts or permission checks.

| Meter | Ohio USD rate | Scope / minimum |
|---|---:|---|
| EC2 `m7i-flex.large` Linux shared | 0.09576/hour | 60-second minimum, per-second; not T-family surplus credits |
| EBS gp3 / standard snapshot storage | 0.08 / 0.05 per GB-month | 3,000 IOPS/125 MiB/s included on gp3; no snapshots in base totals; logical S3 backups instead |
| Fargate x86 CPU / RAM | 0.04048/vCPU-hour / 0.004445/GB-hour | Linux minimum one minute, per-second from image download; valid CPU/RAM pairs; 20 GiB ephemeral/task included |
| Extra Fargate ephemeral disk | 0.000111/GB-hour | Above 20 GiB/task only; not used for durable DB/Kafka |
| ALB / LCU | 0.0225/hour / 0.008/LCU-hour | Partial ALB hours round up; two AZ subnets required |
| Public IPv4 | 0.005/address-hour | ALB minimum two; host/NAT addresses additional |
| NAT / processed data | 0.045/AZ-hour / 0.045/GB | Model zonal NAT; one IPv4 each; hour/partial hour; regional NAT also charges per active AZ, not one region-wide flat fee |
| Interface endpoint / data | 0.01/endpoint-AZ-hour / 0.01/GB | First 1 PB processing tier; partial hours; S3 gateway endpoint has no hourly/processing charge |
| RDS PostgreSQL small Single / Multi-AZ | 0.032 / 0.065 per hour | One primary vs primary+one nonreadable standby; supported engine/class orderability still a pre-plan check |
| RDS gp3 Single / Multi-AZ | 0.115 / 0.23 per GB-month | 20 GiB model/minimum; Multi rate already includes both copies; included baseline I/O, no per-request gp3 I/O charge |
| RDS excess backup / T4g surplus | 0.095/GB-month / 0.075/vCPU-hour | Backups above eligible regional allocation; surplus CPU is additional; avoid unsupported/extended-support engine versions |
| Logs ingest / retention / Insights | 0.50/GB / 0.03/GB-month / 0.005/GB scanned | Standard class; free account-wide allowances not assumed remaining |
| Custom metric / standard alarm metric | 0.30 / 0.10 per month | Alarm price is per metric evaluated, not arbitrary unlimited expressions |
| ECR / S3 Standard | 0.10 / 0.023 per GB-month | Two GB images; two GB releases/state or ten GB with backups; versions count |
| S3 PUT-LIST / GET | 0.005/1,000 / 0.0004/1,000 | Ten writes and 100 reads/hour modeled |
| Secrets / API | 0.40/secret-month / 0.05/10,000 calls | One bundled secret on host; five isolated resources on managed option; ten calls/secret/hour modeled |
| Customer KMS key / symmetric API | 1/key-month / 0.03/10,000 calls | Optional, zero customer-managed keys in base totals; AWS-managed/default service encryption used where supported |
| Internet out / ordinary charged cross-AZ | 0.09/GB / 0.01 per charged side-GB | First paid internet tier; common free allowance not deducted; same-VPC ALB target transfer and RDS standby replication not charged as generic cross-AZ |

Reference sources: [EC2](https://aws.amazon.com/ec2/pricing/on-demand/), [EBS](https://aws.amazon.com/ebs/pricing/), [Fargate](https://aws.amazon.com/fargate/pricing/), [VPC/NAT/IP](https://aws.amazon.com/vpc/pricing/), [PrivateLink](https://aws.amazon.com/privatelink/pricing/), [RDS](https://aws.amazon.com/rds/postgresql/pricing/), [CloudWatch](https://aws.amazon.com/cloudwatch/pricing/), [ECR](https://aws.amazon.com/ecr/pricing/), [S3](https://aws.amazon.com/s3/pricing/), [Secrets](https://aws.amazon.com/secrets-manager/pricing/), [KMS](https://aws.amazon.com/kms/pricing/).

### NAT versus endpoints

One zonal NAT plus its IPv4 costs $0.05/hour before data. Six interface endpoints in one AZ cost $0.06/hour. With identical eligible traffic at $0.045/GB versus $0.01/GB, the fixed-price difference breaks even around **6.86 GB/day**, or **13.71 GB/day** for two NATs versus twelve endpoint-AZs. This calculation excludes S3 bytes routed through the free gateway in both designs and charges processed bytes only once, not once per endpoint count. Actual per-service endpoint traffic must be measured.

The expected case uses 6 GB/day, hence the similar platform totals: $8.37 NAT versus $8.40 endpoints. Endpoint-only does not provide general outbound internet, public package installation or external APIs. It needs `ecr.api`, `ecr.dkr`, Logs and Secrets for the tasks, plus SSM/ssmmessages for retained Kafka EC2; S3 image layers use the gateway. Add STS, monitoring or KMS endpoints only if chosen SDK/agent paths need them. The current host internet-install user-data cannot be reused unchanged for no-NAT deployment. A second AZ multiplies interface endpoint hours. One shared NAT across AZs would add an availability dependency and possible charged cross-AZ paths; that hybrid is not priced as two-NAT resilience.

### Optional managed streaming, priced separately

MSK is blocked by the current Free project policy, so no MSK implementation or enablement is proposed. The separate [streaming table](tables.md#optional-streaming-service-only) compares two or three `kafka.t3.small` brokers with Serverless six partitions. Small brokers cost $0.0456/hour each; gp2 storage $0.10/GB-month. Minimum Standard storage is 1 GiB/broker, but the model allocates at least 20 GiB each; retention+30% headroom grows higher-use storage to 160 GiB each, including full replica copies when replication factor equals broker count. Throughput/CPU remain to be benchmarked. Additional provisioned throughput is not silently purchased; larger supported brokers and storage/throughput choices require repricing.

Two brokers across two AZs at low/expected storage cost **$2.32/day or $69.61/30 days**, before logging and client network. Three brokers/three AZs cost **$3.48/day or $104.41/30 days**. Replication factor two cannot simultaneously promise majority durability and continued writes through one-broker loss; a three-broker RF3/minISR2 exercise teaches a different resilience guarantee. Free-plan restrictions, compatibility work and the desired recovery objective matter more than this small broker price alone.

Serverless has a **$0.75 cluster-hour floor**, plus $0.0015/open-partition-hour, $0.10/GB in, $0.05/GB out and $0.10/GB-month retained. Six completely idle partitions therefore cost **$18.216/day or $546.48/30 days before bytes**. Expected independent streaming input 0.25 GB/hour and two consumer copies raises this to **$19.44/day or $583.07/30 days**. It is not a low-idle-cost choice for this demonstration. No dedicated/brokerless option eliminates the cluster floor.

Streaming totals are the broker service only, not additions to already-running broker costs. If substituting MSK for the retained phase-C Kafka host, subtract that host's compute/disk (about $2.40/day) and reconsider host-only endpoints before adding MSK, logs, IAM/SASL compatibility and network cost. The higher streaming case is not equivalent to the fixed-disk platform higher case; do not use that delta as a validated capacity comparison. [MSK pricing](https://aws.amazon.com/msk/pricing/)

### Optional security, DNS, recovery and release costs

WAF, customer-managed KMS, GuardDuty, Inspector enhanced scanning, Security Hub, Config and paid CloudTrail data events are **not enabled or included**. They are not required merely to name every interview tool. Current account support differs by service; GuardDuty, for example, is absent from the supported new-experience services. WAF in this experience has regional constraints to resolve before any regional ALB association. Free/basic ECR scanning and runner Trivy do not mean Inspector is enabled.

If a WAF lesson is selected, one Web ACL ($5/month), five ordinary rules ($1/rule-month) and $0.60/million requests would add **$0.38/24h or $11.42/720h** at expected traffic, before WAF logs, paid managed rules, Bot/Fraud/CAPTCHA, oversize-body/WCU surcharges and account eligibility. A customer KMS key adds $1/month per billable key version plus $0.03/10,000 symmetric calls, with shared API allowance not deducted. Rotation/additional replicas can add key charges; retain decryptability for retained backups. [WAF](https://aws.amazon.com/waf/pricing/), [KMS](https://aws.amazon.com/kms/pricing/)

Prefer an existing domain/DNS account for the TLS lesson. ACM nonexportable public certificates used with ALB have no additional certificate fee; exportable/private certificates and purchased domains differ. A newly needed Route53 public or private zone costs **$0.50 for the month**, not 1/30 of that for one day; crossing a billing month can charge twice. Alias queries to ALB are free; ordinary standard queries cost $0.40/million. The managed options include one Cloud Map private DNS zone at $0.50 for the day and conservatively two $0.50 calendar-month charges over 30 days starting near month end, plus $0.10/registered-resource-month for five or ten tasks. DNS discovery makes no API lookup calls ($1/million if later selected). Current Route53 pricing states private queries have no extra query charge; the older generic Cloud Map example shows a query allowance instead, so check the actual private-zone tariff at implementation. [Cloud Map](https://aws.amazon.com/cloud-map/pricing/) [ACM](https://aws.amazon.com/certificate-manager/pricing/), [Route53](https://aws.amazon.com/route53/pricing/)

Add **$0.106** as a one-hour parallel host restore compute/disk/IPv4 allowance, plus backup reads and any extra secrets/logs. An RDS clone + one small migration/validation task for one hour adds about **$0.048**, plus actual clone lifetime, backups/logs/network; include additional restore RDS storage while both instances exist. These are rehearsal cost inputs, not measured restore times. Five additional Fargate tasks during a ten-minute overlapping rollout add roughly $0.0103 in compute; migration tasks, retries and image downloads add usage. GitHub Actions minutes/storage, domain registration, taxes and non-AWS SaaS costs are outside these AWS totals and must be checked separately against account allowances.

## Teardown and retention cost boundaries

Destroy at the actual start timestamp +24 hours, after evidence capture and the chosen restore rehearsal. Assign an operator and confirm the deadline before apply. No timer, automation or kill switch has been scheduled by this review. Budgets/alerts do not impose a hard spending cap; the account's Free-plan controls are a separate mechanism.

Stopping an EC2 host leaves disks, secrets, images, buckets and logs; retained EIPs also charge. Stopped RDS still charges storage/backups and automatically restarts after seven days. ALB, NAT gateways, interface endpoints and MSK must be deleted to end their running-resource meters. Set ECS desired count zero and verify tasks stopped before removing the rest, then destroy according to the reviewed dependency plan. Do not delete unrelated resources.

| Deliberately retained example | Gross residual per 30 days at 720/730 normalization |
|---|---:|
| 40 GiB unattached gp3 | $3.16 |
| 20 GiB RDS final snapshot after DB deletion | $1.87 |
| 10 GiB EBS standard snapshot | $0.49 |
| 2 GB ECR images | $0.20 |
| 10 GB S3 backups/state/release versions | $0.23 plus requests |
| 1 GB CloudWatch stored logs | $0.030; set seven-day retention or delete |
| One secret not scheduled for deletion | $0.395 plus API calls |
| One customer KMS key | $0.986 plus API calls; do not delete before dependent backups |
| New Route53 zone | $0.50/month even without traffic; domain renewals independent |

These are per-item examples, not cumulative required retention. Secrets Manager stops storage charges when a secret is scheduled for deletion, despite the recovery window. KMS pending-deletion keys are not charged, but cannot decrypt while pending; keep the key usable until retention ends. S3 versions/delete markers, incomplete multipart uploads, retained RDS automated backups/manual snapshots, tagged images and bootstrap state are easy residuals to miss. Avoid archive storage with minimum retention fees for this short lab. The bootstrap bucket has `prevent_destroy`; export necessary encrypted state, then separately review removing protection and version-aware cleanup. A dev destroy alone is incomplete final closure. [Secrets deletion](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_delete-secret.html), [RDS stopping](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html)

## Decision and next review boundary

The proposed first choice is phase A for 24 hours, with roughly $4 expected gross allowance including the one-hour restore exercise and margin. Higher-use sensitivity is $11.07/day before the extra rehearsal; the expected amount is not a hard cap. Keeping it 30 days would consume roughly $96.56 before extra activities and tax, too close to the currently available $100 credits for an unattended learning environment.

Pending owner decisions: phase A versus a separately funded B/C exercise; maximum planned gross allowance; whether an owned DNS name is available; approved client CIDRs if selecting public ingress; one or two active AZs; NAT versus fully specified endpoints; backup retention/recovery target; and teardown operator/deadline. No account upgrade or MSK enablement is part of the recommendation.

Fresh baseline/bootstrap saved plan files are private local review artifacts summarized in `baseline-plan-summary.json`. The dev artifact is explicitly a **local-backend preview of unchanged baseline source**, not a final S3-backed apply plan or a plan for hardened phase A/B/C. Old October 23 previews are superseded as current evidence. Do not apply any saved preview. After cost/topology selection, implement the chosen scope, run the security/recovery/static tests, generate a new source-bound final plan and updated itemized cost estimate, then obtain approval for that concrete result before provisioning.

The learning chat owns `docs/nodejs-aws-study-path`, its packaging tools and Interview Study Desk import. This chat owns this cost/design packet and infrastructure/deployment documentation. All future lesson links must distinguish proposed design, checked source, local tests and live cloud evidence.
