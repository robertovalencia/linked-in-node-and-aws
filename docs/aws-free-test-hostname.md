# Free testing hostname for the HTTPS ALB

**Zone registration and ACM issuance verified on 27 October 2026; ALB/application deployment pending.** Use a free [dynv6 zone](https://dynv6.com/) for this short development lab. Its [official DNS API](https://dynv6.github.io/api-spec/) supports CNAME and CAA records; the [changelog](https://dynv6.com/docs/changelog) documents underscore-label support. This fits [ACM DNS validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html) while preserving the selected ALB → private ECS → RDS/Kafka architecture.

Registered zone: `linked-in-node-rv.dynv6.net`

Selected application name: `app.linked-in-node-rv.dynv6.net`

Before registration, the candidate returned NXDOMAIN; that did not prove availability. The development chat has now verified the zone in the owner’s signed-in provider account and confirmed public A/authoritative SOA responses. The IPv4 value in the provider is an address, not the zone name, and is not an ALB target. The existing apex address does not conflict with a later `app` CNAME. Certificate issuance has now been verified separately through the live ACM API. ALB reachability is still unverified.

## Cost and scope

The provider currently offers the hostname/DNS service free. The existing nonexportable public ACM certificate for an integrated ALB has [no additional certificate fee](https://aws.amazon.com/certificate-manager/pricing/). No new public Route53 zone, domain purchase, CloudFront distribution, imported certificate or HTTP listener is needed. The separate private Cloud Map zone remains part of the existing AWS estimate.

The reviewed AWS estimates are unchanged: expected staging $6.71/24h and future five-task activation $8.32/24h; their 720-hour comparisons are $187.40/$235.68 before credits, plus recovery exercises. See the [itemized ledger](evidence/ecs-preparation/staging-plan-cost-review.json). A free hostname does not make the ALB/NAT/RDS/EC2 deployment free or authorize applying the old preview.

[Provider terms](https://dynv6.com/terms) provide no SLA and permit inactive-account deletion. Use this for the temporary demonstration, rather than depending on it for durable production DNS. Certificate issuance and actual provider record behavior must be verified before paid infrastructure starts.

## Current checkpoint: certificate issued after approved request

The user approved the exact [one-create saved certificate plan](evidence/certificate-request/plan-review.json) and its DNS validation. Terraform created only `aws_acm_certificate.application` in account `772641336063`, region `us-east-2`. [Live issuance evidence](evidence/certificate-request/issuance.json) reports **ISSUED**, DNS validation **SUCCESS**, RSA2048 and export disabled. The authoritative nameserver and two public resolvers all return the exact ACM CNAME. A post-issuance Terraform plan reports no changes. [Independent operational review](evidence/certificate-request/issuance-critic.md).

Certificate ARN: `arn:aws:acm:us-east-2:772641336063:certificate/ae18667c-47ac-4fda-8039-e877bafe9705`

The original approved binary SHA256 is `5c040631a18c64beb6d912c05ae6e270df4a752e84e4b996470b5ce31ed1b701`. Its private plan/outputs and **live local Terraform state** remain ignored under `work/aws-ecs-certificate-2026-10-27/`. Preserve that directory until deliberate state migration or reviewed certificate destruction; it is no longer disposable generated output. Do not reapply the consumed create plan. State contains certificate/DNS metadata, not the AWS-managed private key. The request-phase state may still say PENDING_VALIDATION; live ACM status is the issuance evidence.

STS and Terraform used the same effective credential environment, with account, region, source/provider-lock and approved-plan hashes checked immediately before apply. The selected certificate has no additional integrated-service fee. It is not yet attached (`InUseBy=[]`, renewal eligibility currently INELIGIBLE); the validation CNAME alone does not establish automatic renewal while unused. No ALB, application tasks, NAT, RDS or Kafka host was provisioned. Approved client CIDRs, a final S3-backed infrastructure plan/current costs, images/bootstrap and actual cloud smoke remain separate gates.

The remaining numbered sections are the repeatable procedure for another hostname; reservation and certificate request are already completed for this one.

## 1. Reserve a zone in your own account

1. [Create a free dynv6 account](https://dynv6.com/users/sign_up) using an email you control, and complete its confirmation step.
2. Open [new zone](https://dynv6.com/zones/new) and reserve `linked-in-node-rv.dynv6.net` if available, or a similar available zone.
3. An ALB uses DNS rather than a fixed server IP. No home/public IP update client is needed for this setup. Leave address fields empty where supported; the API documents IPv4/IPv6 values as optional for zone creation.
4. Return the successfully reserved public zone name to the development chat. Keep the account password, HTTP token and TSIG key private. We can use manual record entry; no provider token needs to enter Terraform or Git.

The application is the `app` child name. **Do not put a CNAME on the zone apex**, where SOA/NS records belong. Do not pin an A record to one of the ALB's current IP addresses.

## 2. Prepare and review the certificate-only plan

After the actual zone is known, use the existing `infra/aws-ecs-certificate` root with `application_hostname=app.YOUR_RESERVED_ZONE`. It requests only the nonexportable public DNS certificate in Ohio; it buys no domain or hosted zone. Prepare a saved plan and review it before applying, as described in [the deployment guide](aws-ecs-dev.md#step-1--obtain-a-hostname-before-paid-infrastructure). The old hostname-free staging plan is not an activation plan.

After an explicitly approved certificate request, ACM returns the real validation record. The following values are examples, not executable AWS-generated tokens:

| Purpose | Relative owner within your zone | Type | Target |
|---|---|---|---|
| Prove control to ACM | `_ACTUAL_ACM_TOKEN.app` | CNAME | Exact `_ACTUAL_VALUE.acm-validations.aws.` returned by ACM |
| Route the application, after an approved ALB exists | `app` | CNAME | Actual `load_balancer_dns_name` output, as an absolute DNS name |

Provider forms differ in whether they accept relative or full names and whether they append the zone to target values. Verify the final DNS result instead of assuming UI field behavior. The ACM record's final owner must be `_ACTUAL_ACM_TOKEN.app.YOUR_RESERVED_ZONE`, and its target must match ACM exactly. Preserve the leading underscore. Avoid a duplicated zone suffix. Keep the validation record for renewal while the certificate is in use.

Read-only checks, substituting actual public names:

```bash
dig @1.1.1.1 +short CNAME _ACTUAL_ACM_TOKEN.app.YOUR_RESERVED_ZONE
AWS_PROFILE=marketplace-dev aws acm describe-certificate \
  --region us-east-2 --certificate-arn ACTUAL_CERTIFICATE_ARN \
  --query 'Certificate.{Status:Status,Domain:DomainName,Validation:DomainValidationOptions}'
```

Proceed only after the certificate is **ISSUED** for the exact application name. A DNS record being visible is not itself issuance proof. If ACM reports a CAA restriction, inspect CAA at the application/zone/parent names and follow [AWS CAA troubleshooting](https://docs.aws.amazon.com/acm/latest/userguide/troubleshooting-caa.html); do not replace trusted TLS with a warning bypass or open an HTTP login path. The initial parent `dynv6.net` check returned no CAA answer, but that is a dated observation, not a guarantee about the reserved zone.

## 3. Review the final infrastructure plan and test the ALB

Use the real hostname, issued same-account Ohio certificate ARN and owner-approved client CIDRs in a newly saved S3-backed plan. Refresh credits, prices and the 24-hour expiry proposal, then obtain explicit provisioning approval. The current no-listener preview remains a review artifact. No billable resources should wait for DNS validation.

After approved provisioning, add the application CNAME to the real ALB DNS output. Remove conflicting A/AAAA records at the same `app` owner before creating its CNAME. Keep backend services, database and Kafka private; only the reviewed client CIDRs get HTTPS443 to the ALB.

```bash
dig @1.1.1.1 +short CNAME app.YOUR_RESERVED_ZONE
curl --fail --show-error https://app.YOUR_RESERVED_ZONE/health
node scripts/acceptance.mjs https://app.YOUR_RESERVED_ZONE work/aws-ecs-acceptance.json
```

Do not use `curl -k`. Require certificate/hostname verification, healthy targets, all48APIchecks, real browser journeys and a denial test from an unapproved client. Verify direct backend/DB/Kafka access remains denied. ALB health alone does not prove the marketplace is functional. The full [cloud security/recovery/rollback gates](aws-ecs-dev.md#operations-recovery-and-rollout-boundaries) still apply.

## 4. Close the temporary lab

At the approved teardown deadline, remove the application CNAME as part of closing the endpoint, follow the reviewed AWS destroy/retention plan and verify residual resources/costs. Retain or remove ACM validation and the certificate together according to the chosen retention decision. Delete unused provider records/zone deliberately; never leave a dangling application CNAME pointing to a deleted load balancer. No deadline or teardown timer has started from this documentation.

## Verification boundary

Current evidence establishes owner-account zone registration, the approved one-resource Terraform apply, one saved provider validation CNAME, matching authoritative/public DNS, live ACM ISSUED/DNS SUCCESS and no-change post-issuance planning. It does not establish ALB/application deployment, actual HTTPS serving, renewal eligibility while unused, cloud recovery or billable-resource teardown. The [independent issuance review](evidence/certificate-request/issuance-critic.md) confirms the completed certificate stage and the remaining ALB/application gap. The earlier free-hostname review is retained as historical preparation evidence. Infrastructure source, saved plan hashes, application source and learning-owned study files are unchanged by this guide.
