# AWS dev cost model

Researched October 21, 2026 from current official pages. USD, `us-east-1`, Linux On Demand, one `t3.medium`, 730-hour comparison month, no free-tier/trial/credit assumptions. These are reproducible estimates, not account-specific quotes or a spending cap. Verify the actual account/region and saved Terraform plan before approving provisioning. The short-run estimate assumes complete AWS dev teardown at hour 24 or 48, including its EC2 root volume, release bucket and ECR images. See [the one/two-day runbook](short-run.md).

| Meter | Assumption | 24 hours | 48 hours | 730 hours |
|---|---|---:|---:|---:|
| EC2 | $0.0418/hour x one host | $1.00 | $2.01 | $30.51 |
| Public IPv4 | $0.005/hour x one active address | $0.12 | $0.24 | $3.65 |
| Encrypted gp3 root disk | 40 GB x $0.08/GB-month, baseline IOPS/throughput | $0.11 | $0.21 | $3.20 |
| Secrets Manager | one secret x $0.40/month | $0.01 | $0.03 | $0.40 |
| ECR storage | assumed 1 GB x $0.10/GB-month | < $0.01 | < $0.01 | $0.10 |
| **Core estimate** | before variable meters; conservative approximation | **about $1.25** | **about $2.49** | **$37.86** |

The EC2 rate comes from [AWS's T3 price table](https://aws.amazon.com/ec2/instance-types/t3/), explicitly for Linux/Unix in US East (Northern Virginia); confirm the account's rate in the [EC2 On Demand calculator](https://aws.amazon.com/ec2/pricing/on-demand/). T3 uses `standard` credits to avoid surplus-credit charges; exhausting credits can throttle CPU. Actual performance is unmeasured until cloud testing.

[IPv4 pricing](https://aws.amazon.com/vpc/pricing/) applies despite no public ingress. [gp3 pricing](https://aws.amazon.com/ebs/general-purpose/) includes baseline 3,000 IOPS / 125 MB/s at the modeled storage rate. [Secrets Manager](https://aws.amazon.com/secrets-manager/pricing/) also meters API requests. [ECR](https://aws.amazon.com/ecr/pricing/) charges for retained image storage; in-region ECR-to-EC2 transfers are free under the documented pricing. Database and Kafka storage are within the root disk capacity assumption.

Add variable S3 state/release storage and requests, outbound internet traffic, Secrets Manager requests, optional snapshots, tax, GitHub Actions minutes/storage, and a hosted SonarQube subscription/server if used. The default Terraform has no ALB, NAT gateway, RDS, MSK, CloudWatch log ingestion, or paid private endpoints. Do not treat their absence as a production architecture recommendation. Security scans run on the GitHub runner; ECR basic scan-on-push is enabled rather than Inspector enhanced scanning.

Stopping compute stops its EC2 meter and releases its auto-assigned IPv4, while disk, secrets, repositories, S3 and snapshots can keep billing. The 24/48-hour model assumes AWS dev storage is destroyed at the deadline. [AWS says secrets marked for deletion are not charged](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_delete-secret.html), despite the seven-day recovery window. The separately bootstrapped, versioned Terraform state bucket remains until its state has been exported and its object versions and bucket deliberately deleted. A tiny storage/request bill can persist if it is retained. Use a billing alert and an explicitly recorded cleanup time; neither is created automatically.
