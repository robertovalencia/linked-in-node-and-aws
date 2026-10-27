# Research: RDS, MSK, observability and security rates

Retrieved 2026-10-27. Region **US East (Ohio), us-east-2**; USD On-Demand list prices before tax, discounts, credits, free allowances and data-transfer charges. No AWS account changes. Public catalog files and SHA-256/publication manifest are alongside this note; catalog availability does **not** prove this account can create resources. RDS rates deliberately exclude UnusedBox capacity-reservation products.

## RDS PostgreSQL

Source: [regional AmazonRDS catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/us-east-2/index.json), published 2026-10-26T21:47:16Z.

| Item | USD rate | SKU |
|---|---:|---|
| db.t4g.micro Single-AZ, 2 vCPU / 1 GiB | 0.016 / hour | GGD6FE59WWUNDKDC |
| db.t4g.small Single-AZ, 2 vCPU / 2 GiB | 0.032 / hour | JBDFT6PN9ME2D9FK |
| db.t4g.micro Multi-AZ one standby (whole deployment) | 0.032 / hour | EHTN9E2TU39SJ75A |
| db.t4g.small Multi-AZ one standby (whole deployment) | 0.065 / hour | 3ACZ8T48EMVC2JAD |
| gp3 Single-AZ | 0.115 / GB-month | JQQGK6D789TWJF8B |
| gp3 Multi-AZ one standby | 0.230 / GB-month | CV3XZCH8KVNFGA7S |
| Backup above free regional allocation | 0.095 / GB-month | HQRQUXJ6DAN3XS6X |
| T4g CPU surplus | 0.075 / vCPU-hour | 8XWSNX36R6XDW7N8 |
| Additional gp3 IOPS Single-AZ | 0.020 / IOPS-month | JP3JR64EDJH7P7DQ |
| Additional gp3 throughput Single-AZ | 0.080 / MiB/s-month | JUFVCMQQRVQSYGPK |

Model **20 GiB** gp3 minimum: current [storage documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html) says PostgreSQL 20–399 GiB includes 3,000 IOPS and 125 MiB/s. Ignore the catalog's older minVolumeSize=5GB attribute. No per-request I/O fee for this gp3 configuration; optional above-baseline provisioned performance requires qualifying larger storage. A Multi-AZ rate already includes primary/standby: do not double again. Multi-AZ DB *cluster* with two readable standbys is a distinct three-node topology, not these prices.

RDS [On-Demand billing](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_OnDemandDBInstances.html): per-second with a 10-minute minimum after create/start/modify; synchronous primary→standby replication transfer included. [PostgreSQL pricing](https://aws.amazon.com/rds/postgresql/pricing/) documents Unlimited burstable CPU charges; pick a currently supported engine version to avoid Extended Support. One small shared RDS instance can host four service-owned logical DBs/roles; this preserves ownership but shares availability/capacity and is a demo compromise. Connection pools must fit the small RAM allocation; db.t4g.micro price is a floor, not a demonstrated fit.

Backups are free up to the regional running database allocation, subject to [RDS backup accounting](https://docs.aws.amazon.com/aws-backup/latest/devguide/rds-backup.html); don't assume retained backups stay free after deleting the DB. Model retained final snapshot GB at 0.095/GB-month if no running allocation remains. [Stopping](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html) retains storage/backup charges and automatically restarts after seven days. Use deletion plus explicitly reviewed retained snapshots for teardown; recovery test creates a separately billed restore instance.

## MSK: optional isolated streaming lab

**Eligibility gate:** the official [new-experience supported-services table](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html) lists MSK under **Paid Plan only**, whereas ECS, RDS, ELB, CloudWatch, Secrets Manager and WAF are in the Free Tier service list. Therefore MSK is a comparison/learning design only while this account remains Free; credits alone do not permit this service, and no account upgrade is authorized. Service listings still do not prove exact action/region permissions.

Source: [regional AmazonMSK catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonMSK/current/us-east-2/index.json), published 2026-10-14T17:00:39Z.

| Item | USD rate | SKU |
|---|---:|---|
| Standard kafka.t3.small broker | 0.0456 / broker-hour | NXRXQS4RQR3WWD66 |
| Standard GP2 storage | 0.10 / provisioned GB-month per broker | 85MD2N76SV79HAP8 |
| Optional provisioned storage throughput | 0.08 / MiB/s-month | B9WKDSJ5HVQEWGRE |
| Serverless cluster | 0.75 / cluster-hour | QGY4AMP47UDBJ8ST |
| Serverless partition | 0.0015 / partition-hour | H68TMWTFX7Y8WHYA |
| Serverless ingress | 0.10 / GB | NGBTP6ZKNUKV7VQU |
| Serverless egress/read | 0.05 / GB | 3BVDAHM6WGWTE7BH |
| Serverless retained storage | 0.10 / GB-month | RNATBFUEM2TUGBS8 |

[Minimum Standard broker storage](https://docs.aws.amazon.com/msk/latest/developerguide/limits.html) is 1 GiB; use a more realistic 20 GiB per broker in an educational estimate, not a capacity guarantee. [Standard clusters support two or three AZ subnets in Ohio; Express requires three](https://docs.aws.amazon.com/msk/latest/developerguide/create-cluster-cli.html). Minimum one broker per AZ, therefore two Standard brokers is the small educational topology. Three AZ/brokers with replication factor 3 and min ISR 2 teaches stronger resilience; two brokers cannot maintain both write quorum and two-copy durability during a broker outage. Verify chosen Kafka version/instance combination before planning.

[T3 brokers suit development](https://docs.aws.amazon.com/msk/latest/developerguide/broker-instance-sizes.html); they have finite CPU-credit and GP2 I/O-burst budgets, so test and monitor sustained throughput. There is no separate Standard per-GB throughput tariff in this selected configuration; network transfer, optional storage throughput, logs and broker scaling remain additional. Do not infer unlimited capacity from absence of a per-byte fee. Tiered storage does not support t3.small, and MSK Replicator does not support t3.small. Do not add either to this small lab.

The following reproducible Decimal calculations use storage prorated with **730 hours per GB-month**, and runtime 24 or exactly 720 hours. They are **incremental MSK charges only**, before logs/client cross-AZ transfer/secrets/KMS/other application costs. Serverless shows six application partitions, no traffic/storage; it does not have a zero-cost idle cluster.

| Runtime | 2 Standard brokers + 40 GiB total | 3 Standard brokers + 60 GiB total | Serverless + 6 partitions, idle |
|---|---:|---:|---:|
| 24 hours | $2.3203 | $3.4805 | $18.2160 |
| 720 hours | $69.6092 | $104.4138 | $546.4800 |

Serverless formula: hours × (0.75 + partitions × 0.0015) + producer_GB × 0.10 + consumer_GB × 0.05 + retained_GB × 0.10 × hours/730. Cluster baseline alone is $18/24h or $540/720h, even with zero partitions. Ohio support and the same charge components are confirmed in the official [MSK pricing example](https://aws.amazon.com/msk/pricing/) and [Serverless documentation](https://docs.aws.amazon.com/msk/latest/developerguide/serverless.html). Keep clients private with TLS/IAM authorization. Existing local Kafka event contracts still need an actual client IAM authentication adaptation and duplicate/replay/retry tests; managed service alone does not prove parity.

MSK does not offer an EC2-style stop state; do not plan to pause its baseline charge overnight. Delete the isolated cluster after exporting only data actually required for learning. Cluster deletion destroys broker data; rolling back an application image cannot undo that or reverse published/consumed events. Restore/replay/deduplication drills must be explicit acceptance tests. Avoid claiming availability or recovery from broker count alone.

## CloudWatch classic scoped telemetry

Source: [regional catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/us-east-2/index.json), published 2026-10-07T11:55:40Z.

| Item | USD rate | SKU |
|---|---:|---|
| Standard custom/app log ingestion | 0.50 / GB | 5T6Z6V26DSR7SZ49 |
| Compressed log storage | 0.03 / GB-month | X7X4WD4A95NDR9U5 |
| Logs Insights scan | 0.005 / GB scanned | 87CRGPXM6NNHU6NU |
| First 10,000 classic custom metric series | 0.30 / metric-month | XK7C3D2X45XTHURD |
| Standard resolution alarm metric | 0.10 / metric-month | 28VSMYRVQXUWCTMA |
| High resolution alarm metric | 0.30 / metric-month | 5AFZE3M2V3FQYUWB |
| Composite alarm | 0.50 / alarm-month | TAVNM49PAPXVHJ37 |

The official [CloudWatch pricing page](https://aws.amazon.com/cloudwatch/pricing/) lists account-wide recurring free allowances of 5 GB in each log category, 10 eligible custom/detailed metrics and 10 eligible standard alarm metrics; existing use can consume them. Estimate gross usage separately from possible allowances/credits. AWS-vended default metrics usually have no metric publishing fee; alarm charges still apply. A CloudWatch agent has no separate license price but publishing memory/disk metrics and app/system logs produces billable usage. Metrics are distinct dimension sets, so per-process/PID/container-label cardinality can multiply cost. Explicitly opt out of blanket enhanced Container Insights/Application Signals until separately priced. Set retention (e.g. seven days), bound queries, redact auth/inquiry payloads. Logs retained after destroy continue storage charges unless separately removed/exported; alarm/metric resources must also be removed.

## Secrets, KMS, WAF

[Secrets regional catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSSecretsManager/current/us-east-2/index.json), published 2026-09-11: $0.40/secret-month (HHK3AZN6HN5CFDJM), $0.05/10,000 API requests = $0.000005 each (DYZUZWKV5HMGF5A9). Prorated hourly. Versions not charged separately; cache reads. See [pricing](https://aws.amazon.com/secrets-manager/pricing/). Service-specific identities may justify several service secrets; don't reuse the one-secret baseline estimate for four independent service credentials without explanation.

[KMS regional catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/awskms/current/us-east-2/index.json), published 2026-10-26: $1/customer-managed key-version-month (FEMX7ZQ4DJ6QE2KP), $0.03/10,000 symmetric requests = $0.000003 each (9XXHSZC4PS7S6AY2), account-wide20,000 eligible request allowance. [KMS pricing](https://aws.amazon.com/kms/pricing/) says AWS-managed/owned key creation/storage is free, operations may incur charges; first two rotations add $1 each monthly, then capped. Pending-deletion customer key storage isn't billed unless deletion canceled. Never destroy a key while retaining dependent encrypted snapshots/state. Prefer managed keys for a cheap baseline unless customer-key control is an explicit lesson. MSK IAM authentication avoids SCRAM-specific credential infrastructure; MSK SCRAM would require customer-managed KMS plus appropriately named Secrets Manager secrets, not default secret encryption.

[WAF regional catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/awswaf/current/us-east-2/index.json), published 2026-09-14: current WebACLV2 $5/month (2R9CM7WJ2KQ6AWDQ), RuleV2 $1/rule-month (D2BYWPHKSXKTQSXA), basic request tier $0.60/million = $0.0000006/request (U3X5XEMQ9BUXCQD5). Base fees prorated hourly; additional WCU/body/bot/fraud/CAPTCHA/paid vendor rule fees and logging can apply. [Official examples](https://aws.amazon.com/waf/pricing/) show one ACL + two custom rules = $7/month plus requests. WAF is a **separately approved optional lab**; a narrowly scoped ALB client allowlist alone does not justify WAF subscription or paid managed rules. Do not enable Shield Advanced (paid commitment); the new-experience table specifically says AWS Shield is unsupported alongside WAF, so make no claim that Shield service administration is available. Other paid security services remain zero only if not enabled; don't assume trials are a permanent free operating mode.

## Research limitations

Prices are freshly retrieved public Ohio list prices. This agent performed no account eligibility, credits or live infrastructure checks; root agent owns those checks. Application telemetry volumes, backup footprints/compression, actual CPU, RDS size fit and Kafka throughput remain assumptions pending load/recovery tests. RDS-specific `rds-oss` and MSK service skills were not installed/available; database routing's documented fallback used official knowledge card/docs and public catalogs without installing software.
