# Free testing hostname for the HTTPS ALB

**Proposed on 27 October 2026; not registered or deployed.** Use a free [dynv6 zone](https://dynv6.com/) for this short development lab. Its [official DNS API](https://dynv6.github.io/api-spec/) supports CNAME and CAA records; the [changelog](https://dynv6.com/docs/changelog) documents underscore-label support. This fits [ACM DNS validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html) while preserving the selected ALB → private ECS → RDS/Kafka architecture.

Proposed zone: `linked-in-node-rv.dynv6.net`  
Proposed application name: `app.linked-in-node-rv.dynv6.net`

The candidate returned NXDOMAIN in public and provider-authoritative DNS checks. **That does not prove availability, reservation, ownership or certificate eligibility.** Only a successful reservation in your account establishes control. If it is unavailable, choose another zone and substitute that zone consistently below.

## Cost and scope

The provider currently offers the hostname/DNS service free. The existing nonexportable public ACM certificate for an integrated ALB has [no additional certificate fee](https://aws.amazon.com/certificate-manager/pricing/). No new public Route53 zone, domain purchase, CloudFront distribution, imported certificate or HTTP listener is needed. The separate private Cloud Map zone remains part of the existing AWS estimate.

The reviewed AWS estimates are unchanged: expected staging $6.71/24h and future five-task activation $8.32/24h; their 720-hour comparisons are $187.40/$235.68 before credits, plus recovery exercises. See the [itemized ledger](evidence/ecs-preparation/staging-plan-cost-review.json). A free hostname does not make the ALB/NAT/RDS/EC2 deployment free or authorize applying the old preview.

[Provider terms](https://dynv6.com/terms) provide no SLA and permit inactive-account deletion. Use this for the temporary demonstration, rather than depending on it for durable production DNS. Certificate issuance and actual provider record behavior must be verified before paid infrastructure starts.

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

Current evidence establishes provider feature/pricing documentation and read-only DNS observations. It does not establish a reserved account zone, live record writes, ACM issuance, AWS creation or ALB success. The [independent hostname review](evidence/free-hostname/critic.md) records this remaining gap. Infrastructure source, saved plan hashes, application source and learning-owned study files are unchanged by this guide.
