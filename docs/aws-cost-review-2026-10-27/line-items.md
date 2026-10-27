# Itemized expected-use estimates

Generated from the exact ledger. USD gross; no credits/shared free allowances deducted.
24h and 720h runtime; 730h normalization for proratable monthly meters. Zone fees are nonprorated.

## 0 Current SSM baseline

| Meter | 24h quantity | 24h USD | 30d USD |
|---|---:|---:|---:|
| EC2 application host | 24.0000 host-hours | 2.29824 | 68.94720 |
| EC2 root gp3 | 1.3151 GB-month | 0.10521 | 3.15616 |
| Public IPv4 | 24.0000 address-hours | 0.12000 | 3.60000 |
| Secrets Manager storage | 0.0329 secret-month | 0.01315 | 0.39452 |
| Secrets Manager API | 240.0000 requests | 0.00120 | 0.03600 |
| ECR images | 0.0658 GB-month | 0.00658 | 0.19726 |
| S3 releases/state/backups | 0.0658 GB-month | 0.00151 | 0.04537 |
| S3 PUT/LIST | 240.0000 requests | 0.00120 | 0.03600 |
| S3 GET | 2400.0000 requests | 0.00096 | 0.02880 |
| Internet egress, first paid tier | 1.2000 GB | 0.10800 | 3.24000 |
| **Total** | | **$2.66** | **$79.68** |

Unused paid categories: WAF, customer-managed KMS keys, GuardDuty/Inspector/Security Hub/Config, MSK, new public DNS zone/domain (managed private zone included), EFS, RDS Proxy, CloudWatch Container Insights/detailed EC2 monitoring/dashboards/traces, EBS snapshots (logical backups modeled in S3 instead), extra gp3 IOPS/throughput.

## 1 Hardened SSM host

| Meter | 24h quantity | 24h USD | 30d USD |
|---|---:|---:|---:|
| EC2 application host | 24.0000 host-hours | 2.29824 | 68.94720 |
| EC2 root gp3 | 1.3151 GB-month | 0.10521 | 3.15616 |
| Public IPv4 | 24.0000 address-hours | 0.12000 | 3.60000 |
| Secrets Manager storage | 0.0329 secret-month | 0.01315 | 0.39452 |
| Secrets Manager API | 240.0000 requests | 0.00120 | 0.03600 |
| ECR images | 0.0658 GB-month | 0.00658 | 0.19726 |
| S3 releases/state/backups | 0.3288 GB-month | 0.00756 | 0.22685 |
| S3 PUT/LIST | 240.0000 requests | 0.00120 | 0.03600 |
| S3 GET | 2400.0000 requests | 0.00096 | 0.02880 |
| CloudWatch standard logs ingest | 0.9600 GB | 0.48000 | 14.40000 |
| CloudWatch logs seven-day retention | 0.0316 GB-month | 0.00095 | 0.19884 |
| Logs Insights queries | 4.8000 GB scanned | 0.02400 | 0.72000 |
| CloudWatch custom metrics | 0.0986 metric-month | 0.02959 | 0.88767 |
| CloudWatch standard alarms | 0.1644 alarm-metric-month | 0.01644 | 0.49315 |
| Internet egress, first paid tier | 1.2000 GB | 0.10800 | 3.24000 |
| **Total** | | **$3.21** | **$96.56** |

Unused paid categories: WAF, customer-managed KMS keys, GuardDuty/Inspector/Security Hub/Config, MSK, new public DNS zone/domain (managed private zone included), EFS, RDS Proxy, CloudWatch Container Insights/detailed EC2 monitoring/dashboards/traces, EBS snapshots (logical backups modeled in S3 instead), extra gp3 IOPS/throughput.

## 2 ALB HTTPS + same host

| Meter | 24h quantity | 24h USD | 30d USD |
|---|---:|---:|---:|
| EC2 application host | 24.0000 host-hours | 2.29824 | 68.94720 |
| EC2 root gp3 | 1.3151 GB-month | 0.10521 | 3.15616 |
| Public IPv4 | 72.0000 address-hours | 0.36000 | 10.80000 |
| ALB hourly | 24.0000 ALB-hours | 0.54000 | 16.20000 |
| ALB maximum LCU dimension | 2.4000 LCU-hours | 0.01920 | 0.57600 |
| Secrets Manager storage | 0.0329 secret-month | 0.01315 | 0.39452 |
| Secrets Manager API | 240.0000 requests | 0.00120 | 0.03600 |
| ECR images | 0.0658 GB-month | 0.00658 | 0.19726 |
| S3 releases/state/backups | 0.3288 GB-month | 0.00756 | 0.22685 |
| S3 PUT/LIST | 240.0000 requests | 0.00120 | 0.03600 |
| S3 GET | 2400.0000 requests | 0.00096 | 0.02880 |
| CloudWatch standard logs ingest | 0.9600 GB | 0.48000 | 14.40000 |
| CloudWatch logs seven-day retention | 0.0316 GB-month | 0.00095 | 0.19884 |
| Logs Insights queries | 4.8000 GB scanned | 0.02400 | 0.72000 |
| CloudWatch custom metrics | 0.0986 metric-month | 0.02959 | 0.88767 |
| CloudWatch standard alarms | 0.1644 alarm-metric-month | 0.01644 | 0.49315 |
| Internet egress, first paid tier | 1.2000 GB | 0.10800 | 3.24000 |
| **Total** | | **$4.01** | **$120.54** |

Unused paid categories: WAF, customer-managed KMS keys, GuardDuty/Inspector/Security Hub/Config, MSK, new public DNS zone/domain (managed private zone included), EFS, RDS Proxy, CloudWatch Container Insights/detailed EC2 monitoring/dashboards/traces, EBS snapshots (logical backups modeled in S3 instead), extra gp3 IOPS/throughput.

## 3 Private ECS/RDS + one NAT

| Meter | 24h quantity | 24h USD | 30d USD |
|---|---:|---:|---:|
| EC2 Kafka host (single point of failure) | 24.0000 host-hours | 2.29824 | 68.94720 |
| EC2 root gp3 | 1.3151 GB-month | 0.10521 | 3.15616 |
| Cloud Map registered task resources | 0.1644 resource-month | 0.01644 | 0.49315 |
| Private DNS hosted zone | 1.0000 zone-month-charges | 0.50000 | 1.00000 |
| Cloud Map API discovery requests | 0.0000 requests | 0.00000 | 0.00000 |
| Fargate CPU: five tasks per replica | 30.0000 vCPU-hours | 1.21440 | 36.43200 |
| Fargate RAM: five tasks per replica | 60.0000 GB-hours | 0.26670 | 8.00100 |
| Fargate additional ephemeral storage | 0.0000 GB-hours | 0.00000 | 0.00000 |
| RDS PostgreSQL db.t4g.small | 24.0000 instance-hours | 0.76800 | 23.04000 |
| RDS 20 GiB gp3 | 0.6575 GB-month | 0.07562 | 2.26849 |
| RDS excess backups | 0.1644 GB-month | 0.01562 | 0.46849 |
| RDS burst CPU surplus | 0.0000 vCPU-hours | 0.00000 | 0.00000 |
| NAT gateway AZ-hours | 24.0000 AZ-hours | 1.08000 | 32.40000 |
| NAT data processed | 6.0000 GB | 0.27000 | 8.10000 |
| Billable cross-AZ data (two charged sides) | 2.4000 side-GB | 0.02400 | 0.72000 |
| Public IPv4 | 72.0000 address-hours | 0.36000 | 10.80000 |
| ALB hourly | 24.0000 ALB-hours | 0.54000 | 16.20000 |
| ALB maximum LCU dimension | 2.4000 LCU-hours | 0.01920 | 0.57600 |
| Secrets Manager storage | 0.1644 secret-month | 0.06575 | 1.97260 |
| Secrets Manager API | 1200.0000 requests | 0.00600 | 0.18000 |
| ECR images | 0.0658 GB-month | 0.00658 | 0.19726 |
| S3 releases/state/backups | 0.3288 GB-month | 0.00756 | 0.22685 |
| S3 PUT/LIST | 240.0000 requests | 0.00120 | 0.03600 |
| S3 GET | 2400.0000 requests | 0.00096 | 0.02880 |
| CloudWatch standard logs ingest | 0.9600 GB | 0.48000 | 14.40000 |
| CloudWatch logs seven-day retention | 0.0316 GB-month | 0.00095 | 0.19884 |
| Logs Insights queries | 4.8000 GB scanned | 0.02400 | 0.72000 |
| CloudWatch custom metrics | 0.2630 metric-month | 0.07890 | 2.36712 |
| CloudWatch standard alarms | 0.3288 alarm-metric-month | 0.03288 | 0.98630 |
| Internet egress, first paid tier | 1.2000 GB | 0.10800 | 3.24000 |
| **Total** | | **$8.37** | **$237.16** |

Unused paid categories: WAF, customer-managed KMS keys, GuardDuty/Inspector/Security Hub/Config, MSK, new public DNS zone/domain (managed private zone included), EFS, RDS Proxy, CloudWatch Container Insights/detailed EC2 monitoring/dashboards/traces, EBS snapshots (logical backups modeled in S3 instead), extra gp3 IOPS/throughput.

## 3e Private ECS/RDS + six endpoints

| Meter | 24h quantity | 24h USD | 30d USD |
|---|---:|---:|---:|
| EC2 Kafka host (single point of failure) | 24.0000 host-hours | 2.29824 | 68.94720 |
| EC2 root gp3 | 1.3151 GB-month | 0.10521 | 3.15616 |
| Cloud Map registered task resources | 0.1644 resource-month | 0.01644 | 0.49315 |
| Private DNS hosted zone | 1.0000 zone-month-charges | 0.50000 | 1.00000 |
| Cloud Map API discovery requests | 0.0000 requests | 0.00000 | 0.00000 |
| Fargate CPU: five tasks per replica | 30.0000 vCPU-hours | 1.21440 | 36.43200 |
| Fargate RAM: five tasks per replica | 60.0000 GB-hours | 0.26670 | 8.00100 |
| Fargate additional ephemeral storage | 0.0000 GB-hours | 0.00000 | 0.00000 |
| RDS PostgreSQL db.t4g.small | 24.0000 instance-hours | 0.76800 | 23.04000 |
| RDS 20 GiB gp3 | 0.6575 GB-month | 0.07562 | 2.26849 |
| RDS excess backups | 0.1644 GB-month | 0.01562 | 0.46849 |
| RDS burst CPU surplus | 0.0000 vCPU-hours | 0.00000 | 0.00000 |
| Six interface endpoints per active AZ | 144.0000 endpoint-AZ-hours | 1.44000 | 43.20000 |
| Interface endpoint data processed | 6.0000 GB | 0.06000 | 1.80000 |
| Billable cross-AZ data (two charged sides) | 2.4000 side-GB | 0.02400 | 0.72000 |
| Public IPv4 | 48.0000 address-hours | 0.24000 | 7.20000 |
| ALB hourly | 24.0000 ALB-hours | 0.54000 | 16.20000 |
| ALB maximum LCU dimension | 2.4000 LCU-hours | 0.01920 | 0.57600 |
| Secrets Manager storage | 0.1644 secret-month | 0.06575 | 1.97260 |
| Secrets Manager API | 1200.0000 requests | 0.00600 | 0.18000 |
| ECR images | 0.0658 GB-month | 0.00658 | 0.19726 |
| S3 releases/state/backups | 0.3288 GB-month | 0.00756 | 0.22685 |
| S3 PUT/LIST | 240.0000 requests | 0.00120 | 0.03600 |
| S3 GET | 2400.0000 requests | 0.00096 | 0.02880 |
| CloudWatch standard logs ingest | 0.9600 GB | 0.48000 | 14.40000 |
| CloudWatch logs seven-day retention | 0.0316 GB-month | 0.00095 | 0.19884 |
| Logs Insights queries | 4.8000 GB scanned | 0.02400 | 0.72000 |
| CloudWatch custom metrics | 0.2630 metric-month | 0.07890 | 2.36712 |
| CloudWatch standard alarms | 0.3288 alarm-metric-month | 0.03288 | 0.98630 |
| Internet egress, first paid tier | 1.2000 GB | 0.10800 | 3.24000 |
| **Total** | | **$8.40** | **$238.06** |

Unused paid categories: WAF, customer-managed KMS keys, GuardDuty/Inspector/Security Hub/Config, MSK, new public DNS zone/domain (managed private zone included), EFS, RDS Proxy, CloudWatch Container Insights/detailed EC2 monitoring/dashboards/traces, EBS snapshots (logical backups modeled in S3 instead), extra gp3 IOPS/throughput.

## 3r Two-AZ tasks/RDS + two NATs

| Meter | 24h quantity | 24h USD | 30d USD |
|---|---:|---:|---:|
| EC2 Kafka host (single point of failure) | 24.0000 host-hours | 2.29824 | 68.94720 |
| EC2 root gp3 | 1.3151 GB-month | 0.10521 | 3.15616 |
| Cloud Map registered task resources | 0.3288 resource-month | 0.03288 | 0.98630 |
| Private DNS hosted zone | 1.0000 zone-month-charges | 0.50000 | 1.00000 |
| Cloud Map API discovery requests | 0.0000 requests | 0.00000 | 0.00000 |
| Fargate CPU: five tasks per replica | 60.0000 vCPU-hours | 2.42880 | 72.86400 |
| Fargate RAM: five tasks per replica | 120.0000 GB-hours | 0.53340 | 16.00200 |
| Fargate additional ephemeral storage | 0.0000 GB-hours | 0.00000 | 0.00000 |
| RDS PostgreSQL db.t4g.small | 24.0000 instance-hours | 1.56000 | 46.80000 |
| RDS 20 GiB gp3 | 0.6575 GB-month | 0.15123 | 4.53699 |
| RDS excess backups | 0.1644 GB-month | 0.01562 | 0.46849 |
| RDS burst CPU surplus | 0.0000 vCPU-hours | 0.00000 | 0.00000 |
| NAT gateway AZ-hours | 48.0000 AZ-hours | 2.16000 | 64.80000 |
| NAT data processed | 6.0000 GB | 0.27000 | 8.10000 |
| Billable cross-AZ data (two charged sides) | 2.4000 side-GB | 0.02400 | 0.72000 |
| Public IPv4 | 96.0000 address-hours | 0.48000 | 14.40000 |
| ALB hourly | 24.0000 ALB-hours | 0.54000 | 16.20000 |
| ALB maximum LCU dimension | 2.4000 LCU-hours | 0.01920 | 0.57600 |
| Secrets Manager storage | 0.1644 secret-month | 0.06575 | 1.97260 |
| Secrets Manager API | 1200.0000 requests | 0.00600 | 0.18000 |
| ECR images | 0.0658 GB-month | 0.00658 | 0.19726 |
| S3 releases/state/backups | 0.3288 GB-month | 0.00756 | 0.22685 |
| S3 PUT/LIST | 240.0000 requests | 0.00120 | 0.03600 |
| S3 GET | 2400.0000 requests | 0.00096 | 0.02880 |
| CloudWatch standard logs ingest | 0.9600 GB | 0.48000 | 14.40000 |
| CloudWatch logs seven-day retention | 0.0316 GB-month | 0.00095 | 0.19884 |
| Logs Insights queries | 4.8000 GB scanned | 0.02400 | 0.72000 |
| CloudWatch custom metrics | 0.2630 metric-month | 0.07890 | 2.36712 |
| CloudWatch standard alarms | 0.3288 alarm-metric-month | 0.03288 | 0.98630 |
| Internet egress, first paid tier | 1.2000 GB | 0.10800 | 3.24000 |
| **Total** | | **$11.93** | **$344.11** |

Unused paid categories: WAF, customer-managed KMS keys, GuardDuty/Inspector/Security Hub/Config, MSK, new public DNS zone/domain (managed private zone included), EFS, RDS Proxy, CloudWatch Container Insights/detailed EC2 monitoring/dashboards/traces, EBS snapshots (logical backups modeled in S3 instead), extra gp3 IOPS/throughput.

## 3re Two-AZ tasks/RDS + twelve endpoints

| Meter | 24h quantity | 24h USD | 30d USD |
|---|---:|---:|---:|
| EC2 Kafka host (single point of failure) | 24.0000 host-hours | 2.29824 | 68.94720 |
| EC2 root gp3 | 1.3151 GB-month | 0.10521 | 3.15616 |
| Cloud Map registered task resources | 0.3288 resource-month | 0.03288 | 0.98630 |
| Private DNS hosted zone | 1.0000 zone-month-charges | 0.50000 | 1.00000 |
| Cloud Map API discovery requests | 0.0000 requests | 0.00000 | 0.00000 |
| Fargate CPU: five tasks per replica | 60.0000 vCPU-hours | 2.42880 | 72.86400 |
| Fargate RAM: five tasks per replica | 120.0000 GB-hours | 0.53340 | 16.00200 |
| Fargate additional ephemeral storage | 0.0000 GB-hours | 0.00000 | 0.00000 |
| RDS PostgreSQL db.t4g.small | 24.0000 instance-hours | 1.56000 | 46.80000 |
| RDS 20 GiB gp3 | 0.6575 GB-month | 0.15123 | 4.53699 |
| RDS excess backups | 0.1644 GB-month | 0.01562 | 0.46849 |
| RDS burst CPU surplus | 0.0000 vCPU-hours | 0.00000 | 0.00000 |
| Six interface endpoints per active AZ | 288.0000 endpoint-AZ-hours | 2.88000 | 86.40000 |
| Interface endpoint data processed | 6.0000 GB | 0.06000 | 1.80000 |
| Billable cross-AZ data (two charged sides) | 2.4000 side-GB | 0.02400 | 0.72000 |
| Public IPv4 | 48.0000 address-hours | 0.24000 | 7.20000 |
| ALB hourly | 24.0000 ALB-hours | 0.54000 | 16.20000 |
| ALB maximum LCU dimension | 2.4000 LCU-hours | 0.01920 | 0.57600 |
| Secrets Manager storage | 0.1644 secret-month | 0.06575 | 1.97260 |
| Secrets Manager API | 1200.0000 requests | 0.00600 | 0.18000 |
| ECR images | 0.0658 GB-month | 0.00658 | 0.19726 |
| S3 releases/state/backups | 0.3288 GB-month | 0.00756 | 0.22685 |
| S3 PUT/LIST | 240.0000 requests | 0.00120 | 0.03600 |
| S3 GET | 2400.0000 requests | 0.00096 | 0.02880 |
| CloudWatch standard logs ingest | 0.9600 GB | 0.48000 | 14.40000 |
| CloudWatch logs seven-day retention | 0.0316 GB-month | 0.00095 | 0.19884 |
| Logs Insights queries | 4.8000 GB scanned | 0.02400 | 0.72000 |
| CloudWatch custom metrics | 0.2630 metric-month | 0.07890 | 2.36712 |
| CloudWatch standard alarms | 0.3288 alarm-metric-month | 0.03288 | 0.98630 |
| Internet egress, first paid tier | 1.2000 GB | 0.10800 | 3.24000 |
| **Total** | | **$12.20** | **$352.21** |

Unused paid categories: WAF, customer-managed KMS keys, GuardDuty/Inspector/Security Hub/Config, MSK, new public DNS zone/domain (managed private zone included), EFS, RDS Proxy, CloudWatch Container Insights/detailed EC2 monitoring/dashboards/traces, EBS snapshots (logical backups modeled in S3 instead), extra gp3 IOPS/throughput.
