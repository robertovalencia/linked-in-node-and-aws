# AWS dev cost model

Researched October 21, 2026 from current official pages. USD, `us-east-1`, Linux On Demand, one `t3.medium`,730-hour month, no free-tier/trial/credit assumptions. These are reproducible estimates, not account-specific quotes or a spending cap. Verify the actual account/region and saved Terraform plan before approving provisioning.

| Meter | Assumption | 730 hours | 24 hours |
|---|---|---:|---:|
| EC2 | $0.0416/hour x one host | $30.37 | $1.00 |
| Public IPv4, outbound connectivity | $0.005/hour x one active address | $3.65 | $0.12 |
| Encrypted gp3 root disk |40 GB x $0.08/GB-month, baseline IOPS/throughput | $3.20 | $0.11 |
| Secrets Manager | one secret x $0.40/month | $0.40 | $0.01 |
| ECR storage | assumed 1 GB x $0.10/GB-month | $0.10 | <$0.01 |
| Core estimate | before variable meters | **$37.72** | **about $1.24** |

EC2 rate matches the [AWS published instance table](https://docs.aws.amazon.com/prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html); confirm Linux pricing in the [EC2 On Demand calculator](https://aws.amazon.com/ec2/pricing/on-demand/). T3 uses `standard` credits to avoid surplus-credit charges; exhausting credits can throttle CPU. Actual performance is unmeasured until cloud testing.

[IPv4 pricing](https://aws.amazon.com/vpc/pricing/) applies despite no public ingress. [gp3 pricing](https://aws.amazon.com/ebs/general-purpose/) includes baseline 3,000 IOPS / 125 MB/s at the modeled storage rate. [Secrets Manager](https://aws.amazon.com/secrets-manager/pricing/) also meters API requests. [ECR](https://aws.amazon.com/ecr/pricing/) charges for retained image storage; in-region ECR-to-EC2 transfers are free under the documented pricing. Database and Kafka storage are within the root disk capacity assumption.

Add variable S3 state/release storage and requests, outbound internet traffic, Secrets Manager requests, optional snapshots, tax, GitHub Actions minutes/storage, and a hosted SonarQube subscription/server if used. The default Terraform has no ALB, NAT gateway, RDS, MSK, CloudWatch log ingestion, or paid private endpoints. Do not treat their absence as a production architecture recommendation. Security scans run on the GitHub runner; ECR basic scan-on-push is enabled rather than Inspector enhanced scanning.

Stopping compute stops its EC2 meter and releases its auto-assigned IPv4, while disk, secrets, repositories, S3, and snapshots keep billing. The 24-hour model assumes storage is deleted after 24 hours; retaining it for a month adds the monthly storage meters. Secrets retain their seven-day recovery lifecycle according to AWS policy; verify billing treatment rather than assuming immediate disappearance. Use a billing alert and an explicitly approved cleanup time; neither is created automatically.
