# AWS dev cost model

> **Current review: 27 October 2026.** The [phased cost/design packet](aws-cost-review-2026-10-27/README.md) supersedes the currentness of this historical core estimate. It includes refreshed Free-plan/credit/resource checks, 24-hour and 30-day idle/expected/higher comparisons, itemized regional rates, proposed architecture/recovery gates and fresh baseline-only previews. Cost/topology selection is pending; no AWS apply occurred.

Updated 23 October 2026 for the selected **24-hour Free plan demonstration in `us-east-2`**: one Linux On Demand `m7i-flex.large`, one 40 GiB gp3 root disk, one public IPv4, and one Secrets Manager secret. The account preflight reported an active Free plan with $100 available credits. Live EC2 discovery reported this instance as Free Tier eligible with 2 vCPU and 8 GiB RAM. No resources have been provisioned. These are list-price credit-consumption estimates, not an account invoice or a guarantee of remaining balance.

| Meter | Current modeled rate | 24 hours | 48 hours for comparison |
|---|---|---:|---:|
| EC2 `m7i-flex.large` | $0.09576/hour | $2.29824 | $4.59648 |
| Public IPv4 | $0.005/hour | $0.12000 | $0.24000 |
| gp3 root disk | 40 GiB × $0.08/GB-month; 730-hour approximation | $0.10521 | $0.21041 |
| Secrets Manager | one secret × $0.40/month; 730-hour approximation | $0.01315 | $0.02630 |
| ECR storage | modeled 1 GB × $0.10/GB-month | $0.00329 | $0.00658 |
| **Core including modeled ECR storage** | sum of the above | **$2.53988 ≈ $2.54** | **$5.07977 ≈ $5.08** |

The approved duration is **24 hours**, not 48. The proposed Free plan instance replaces the earlier `t3.medium` model. Its 8 GiB RAM gives PostgreSQL, Kafka, four Node processes, and the frontend more headroom. m7i-flex uses baseline/burst behavior but does not use T-family surplus CPU credits. Actual workload performance remains unverified until deployment.

The compute, gp3, IPv4, secret, and ECR rates were retrieved from official AWS Price List data for the selected region. Raw responses and calculations are retained under ignored `work/aws-preparation/`; they are preparation evidence, not deployment results. See the [AWS Price List API](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html), [EC2 On Demand pricing](https://aws.amazon.com/ec2/pricing/on-demand/), [IPv4 pricing](https://aws.amazon.com/vpc/pricing/), [EBS pricing](https://aws.amazon.com/ebs/pricing/), and [Secrets Manager pricing](https://aws.amazon.com/secrets-manager/pricing/), and [ECR pricing](https://aws.amazon.com/ecr/pricing/).

Add ECR storage above the modeled 1 GB, S3 versioned state/release storage and requests, Secrets Manager API requests, outbound internet traffic, optional snapshots, tax where applicable, and GitHub Actions minutes/artifacts. Do not present the $2.54 core as an all-inclusive cap. ECR basic scanning and runner Trivy checks do not imply Inspector enhanced scanning is enabled. No ALB, NAT gateway, RDS, MSK, paid VPC endpoints, or CloudWatch log ingestion is in the prepared Terraform stack.

The selected Free plan uses available credits for eligible usage and does not automatically upgrade to Paid. Confirm the credit balance and plan before each apply. Account-specific service restrictions remain: this account denied IAM OIDC-provider operations through an AWS-managed service control policy, so GitHub verifies while a temporary local AWS login performs the release. Do not upgrade the account or remove restrictions merely to use OIDC. See [AWS Free plan rules](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html) and [EC2 Free Tier eligibility](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html).

Stopping compute leaves storage, secrets, images, and S3 objects. The model assumes complete dev teardown at hour 24, including the EC2 root disk. [AWS does not charge for a secret marked for deletion](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_delete-secret.html), despite its seven-day recovery window. The protected, versioned bootstrap state bucket requires separate final cleanup after secure state export. See the [24-hour runbook](short-run.md). No automatic teardown or reminder has been scheduled; record the actual start and deadline only when provisioning begins.
