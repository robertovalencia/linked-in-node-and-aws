# Independent saved certificate plan review — 2026-10-27

**Verdict: ready for user review and approval of this certificate request only, subject to the execution guards below. No AWS or DNS mutation was performed by this review.** The request is not yet authorized to apply. This review does not approve the subsequent ECS/RDS/NAT/ALB deployment.

## Actual artifact and scope

Reviewed `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-ecs-certificate-2026-10-27/certificate.tfplan`, its ZIP contents, embedded source and provider lock, private variable file, saved JSON, and saved text. Read the repository's AGENTS.md. A fresh, successful `terraform show -json certificate.tfplan` decoded the actual binary; its parsed JSON exactly equals the supplied `plan.json`. Initial sandbox execution could not start the local provider schema process; the read-only show succeeded with local execution escalation. Neither command was an apply.

The complete, applyable, non-errored plan was generated at `2026-10-27T22:14:59Z` with Terraform 1.17.0. It has exactly one managed resource change: **create `aws_acm_certificate.application`**. No update, delete, DNS record, domain registration, hosted zone, certificate-validation waiter, provisioner, network, compute, database, IAM role, or other infrastructure is present. Embedded current and previous states have empty resources and outputs.

The certificate configuration is exactly `app.linked-in-node-rv.dynv6.net`, DNS validation, RSA_2048, certificate transparency enabled, and export DISABLED. The only SAN equals the requested hostname. Provider and resource region are `us-east-2` (Ohio). The embedded provider lock selects `hashicorp/aws` 6.70.0 with constraint `~> 6.0`. Embedded source and lock match the scratch files byte for byte, and source matches committed `HEAD:infra/aws-ecs-certificate/main.tf`. The hostname validation check passes. No source edits were needed.

The certificate ARN, real validation CNAME name/value/type, and certificate status are unknown until application. The human-readable plan's write-only private-key marker does not establish that a key was supplied: the decoded configuration and changes supply no private key, certificate body, or certificate chain. Pattern checks over local files and all plan members found no PEM private key, AWS access-key identifier, email address, or IPv4 address. This is scoped inspection, not a guarantee that arbitrary secrets can be identified by pattern matching. Saved plans/state must remain private and outside Git.

## Security and account guard

The source has no `allowed_account_ids` and the saved plan does not intrinsically bind its provider to account `772641336063`. The previously reported STS identity is contextual evidence, not a durable execution guarantee. This is a residual wrong-account risk.

For this narrowly scoped, non-exportable public certificate request, an enforced pre-apply identity check is sufficient; regenerating the plan solely to add an account allowlist is not a blocker to user review. Immediately before any approved apply, the operator must select `marketplace-dev`, verify STS account **772641336063** using the same effective credential environment Terraform will use, enforce `us-east-2`, and stop on any mismatch or expired credentials. CLI `--profile` alone is insufficient evidence if Terraform inherits different environment credentials. Resolve credential overrides before both commands and keep the credential environment unchanged between verification and execution. An intrinsic provider account allowlist would improve a future reusable configuration.

Also recheck the approved binary SHA-256, use this exact saved plan with its matching lock/provider, and keep its local state in this dedicated directory. A newly generated or altered plan needs a fresh review. User approval must explicitly cover the certificate request; DNS changes require their own authorized scope. Do not infer approval for the paid demo infrastructure.

## Cost, failure paths, and remaining gap

Current official [ACM pricing](https://aws.amazon.com/certificate-manager/pricing/) lists a non-exportable public certificate for integrated AWS services at no cost. This plan sets export DISABLED and creates no paid infrastructure, domain, or DNS service. Its certificate-only estimate is **$0 ACM certificate charge**. The later ALB/ECS/RDS/NAT demo has separate costs and requires its own concrete saved plan and current estimate.

The root reviewer reports the parent dynv6 zone is already user-owned and authoritative DNS exists; those external ownership and account observations were supplied context and were not independently repeated here. An IPv4 address is not a DNS zone. No email or IP address was copied into this report.

**Largest remaining gap: the certificate has not been requested, the real ACM validation CNAME does not yet exist, and ISSUED has not been observed.** Approval and application of this exact request will produce the account-specific CNAME. Only then can an authorized DNS edit add that exact record within the owned dynv6 zone, respecting the provider's relative-name behavior; public DNS resolution and ACM status must subsequently be verified. Do not fabricate a token or treat parent-zone A/SOA records as certificate validation. Official [ACM DNS validation documentation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html) requires the generated CNAME, explains DNS-provider name handling, and specifies validation timeout after 72 hours. Applying this resource does not prove issuance, HTTPS, a reachable application, or a successful deployment.

## SHA-256 evidence

| File | SHA-256 |
| --- | --- |
| `certificate.tfplan` | `5c040631a18c64beb6d912c05ae6e270df4a752e84e4b996470b5ce31ed1b701` |
| `main.tf` (scratch, embedded, and committed source match) | `26bebdbcb98c3c211c257fb8d5188a2413c5a209382db0ab0502ba50121a251c` |
| `.terraform.lock.hcl` (scratch and embedded match) | `795c03ec138135bd2913276060c796ab9b3588715e55d3f4081f65879ee67693` |
| `certificate.tfvars.json` | `96fda00827992f3ee0672ab1b5e74b3716f9487834ee6cd3ceaf0181dd88b609` |
| `plan.json` | `f09404e54299588a61246f433c487e6f61c092ba29128752268e47702237f252` |
| `plan.txt` | `5173b9fbd6ddeab783f39272c586d4ea189c6860ad38c9c6c572caa55cd9f75d` |

The fresh JSON was compared semantically; its serialization is not asserted to have the same byte hash. This critic inspected the saved plan independently and did not approve its own construction.
