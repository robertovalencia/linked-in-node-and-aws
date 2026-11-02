---
title: "AWS/Terraform interview questionnaire and developer troubleshooting"
topic: "Project interview practice"
last_researched: 2026-11-02
source_labels: Current source; Dated execution; Local/mock definitions; Absent features explicitly labeled
---

# AWS/Terraform questionnaire: 30 questions and 12 incidents

[84-lesson study path](README.md) · [Foundations](generated/20-cloud-roadmap-and-lab.md) · [Full syllabus](generated/44-cloud-complete-syllabus-and-mastery-map.md)

Use this companion for short spoken answers and practical diagnosis. It adds no numbered lessons and does not change your progress. **Start now** covers prerequisites and everyday risks; **next** connects mechanisms; **extension** covers alternatives. If an answer feels unfamiliar, open its first Study link, explain that mechanism, then follow the remaining lessons and retry the answer without notes.

The questions select recurring engineering issues from official AWS troubleshooting guides and HashiCorp documentation, researched November 2, 2026. They are a project-specific selection, not a measured ranking of interview frequency. Each Project link opens a portable literal excerpt with the real path and setting; committed matches also have revision-pinned GitHub links. Local uncommitted files are explicitly labeled.

## Small acronym glossary

| Term | Plain-language meaning |
|---|---|
| AWS / IAM | Amazon Web Services / Identity and Access Management |
| EC2 / ECS / ECR | Elastic Compute Cloud virtual machines / Elastic Container Service scheduler / Elastic Container Registry image store |
| RDS / S3 / EBS | Relational Database Service / Simple Storage Service objects / Elastic Block Store disks |
| VPC / NAT / EIP | Virtual Private Cloud network / Network Address Translation for outbound connections / Elastic IP address allocation |
| ALB / ACM / DNS | Application Load Balancer / AWS Certificate Manager / Domain Name System |
| TLS / CA / SCRAM | Transport Layer Security encryption / certificate authority that validates identity / Salted Challenge Response Authentication Mechanism for password verification |
| API / HTTP / SQL | Application programming interface / Hypertext Transfer Protocol for web requests / Structured Query Language for database operations |
| SG / NACL / ACL | Security group / network access control list / access control list |
| SSM / OIDC / JWT | Systems Manager / OpenID Connect / JSON Web Token |
| CI / SHA / HCL | Continuous integration / Secure Hash Algorithm digest (here, exact commit identity) / HashiCorp Configuration Language |
| AZ / ARN / CIDR | Availability Zone / Amazon Resource Name / Classless Inter-Domain Routing, network prefix notation such as /32 for one IPv4 address |
| MSK / RPO / RTO | Managed Streaming for Apache Kafka / recovery point objective (data loss) / recovery time objective (duration) |

## Read the evidence by date

The original EC2/Systems Manager (SSM) baseline in lessons 20–43 is historical source. The selected newer source prepares private ECS/Fargate applications, private RDS PostgreSQL, EC2 Kafka with TLS/SCRAM, ALB/TLS, one zonal NAT, S3 gateway routing and scoped secrets. Four capabilities keep separate database ownership. **Source definition does not establish a running application.**

| Checkpoint | What its record establishes | What remains unproved here |
|---|---|---|
| October 30 micro completion | Infrastructure read-back/no-change plan; application tasks absent; alarms lacked delivery proof | Application release/bootstrap/activation, cloud SQL/security/recovery and business acceptance |
| October 30 cleanup transition and destroy rejection | Deletion-related settings changed; final destroy rejected before execution | Full teardown; do not retry through another route |
| October 31 reversible stop | EC2/RDS stopped then; storage/resources retained; recorded RDS restart November 7, 07:22 AM EST | Present-day inventory, protection flags, costs or continued stopped state |

Read the [micro-completion excerpt](evidence/aws-terraform-project-context.md#source-q17), [stop/cost excerpt](evidence/aws-terraform-project-context.md#source-q18) and [later cleanup-setting excerpt](evidence/aws-terraform-project-context.md#source-i12). Full preserved records: [October 30 micro completion](evidence/questionnaire-records/aws-micro-completion-execution-2026-10-30.md) and [October 31 reversible stop, including the later cleanup/deletion settings and rejected destroy](evidence/questionnaire-records/aws-reversible-compute-stop-2026-10-31.md). These are exact dated source copies, not fresh cloud observations. The original files were inspected in the author’s local checkout; they were not assumed committed. The latter records supersede earlier protection/operating-state claims for those checkpoints. No fresh cloud status or cost check was performed for this guide.

## Choose a starting point

- First AWS interview: Q01–Q07, Q09–Q14, Q16 and Q18; then I03 and I08.
- First Terraform interview: Q19–Q29; run the [credential-free command workbook](walkthroughs/09-terraform-local-commands.md).
- Troubleshooting: choose I01–I12, identify the failing layer, and explain checks → repair → recovery evidence. These are rehearsal scenarios unless a dated execution scope explicitly says otherwise.
- Longer rehearsal: use [42 · troubleshooting exercises](generated/42-aws-terraform-troubleshooting-workbook.md), [43 · five-minute defense](generated/43-aws-terraform-capstone-and-interview.md) and [83 · professional question bank](generated/83-professional-cloud-capstone-and-question-bank.md). Their pinned examples can describe older checkpoints; use the dated context above for this companion.

Read-only learning and local validation are authorized here. The incident repairs describe future operator decisions, not commands executed by this guide. Cloud plan/apply, activation, secret access, cleanup and paid feature enablement remain with the deployment owner and their approval process. For that process see the [AWS command workflow](walkthroughs/10-terraform-aws-commands.md) and [historical execution journal](walkthroughs/11-aws-execution-journal.md).

## Interview questions

<a id="q01"></a>
### Q01 · What do AWS, Terraform and Docker each do?

**Priority:** start now. **Evidence:** Current source.

AWS (Amazon Web Services) provides cloud resources. Terraform describes and manages their desired configuration; Docker packages processes into images. Here, four NestJS capabilities remain separate even though they share a backend image; infrastructure creation and application activation are separate steps.

**Project:** [infra/aws-ecs-dev/network.tf](evidence/aws-terraform-project-context.md#source-q01) · setting/symbol: `capabilities     =`.

**Study:** [20 · cloud roadmap and lab](generated/20-cloud-roadmap-and-lab.md) → [53 · ecs fargate tasks and services](generated/53-ecs-fargate-tasks-and-services.md) → [80 · staged modernization and traceability](generated/80-staged-modernization-and-traceability.md).

**More foundation reading:** [AWS account basics](https://docs.aws.amazon.com/accounts/latest/reference/accounts-welcome.html) · [Docker architecture](https://docs.docker.com/get-started/docker-overview/).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/intro).

<a id="q02"></a>
### Q02 · What is an account, Region, Availability Zone and ARN?

**Priority:** start now. **Evidence:** Current source.

An account is an ownership/billing boundary; a Region is a geographic deployment area; an Availability Zone (AZ) is an isolated location within it. An Amazon Resource Name (ARN) identifies a resource. This provider uses a region input; inspect its value and effective account before any operator action. Two subnet AZs do not make the single active application/database AZ highly available.

**Project:** [infra/aws-ecs-dev/versions.tf](evidence/aws-terraform-project-context.md#source-q02) · setting/symbol: `region = var.region`.

**Study:** [21 · aws accounts regions and cli](generated/21-aws-accounts-regions-and-cli.md) → [45 · aws account governance and landing zones](generated/45-aws-account-governance-and-landing-zones.md) → [47 · vpc cidr ipv6 and subnet design](generated/47-vpc-cidr-ipv6-and-subnet-design.md).

**More foundation reading:** [AWS accounts](https://docs.aws.amazon.com/accounts/latest/reference/accounts-welcome.html) · [Regions and Availability Zones](https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-availability-zones.html).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html).

<a id="q03"></a>
### Q03 · How do IAM trust and permissions differ?

**Priority:** start now. **Evidence:** Current source.

Identity and Access Management (IAM) trust says who may assume a role; permissions say which actions it can perform on which resources. Applicable explicit denies override allows. Check session, boundary and organization controls too; attaching an allow alone does not settle every denial. The ECS trust restricts the source account and ECS ARN.

**Project:** [infra/aws-ecs-dev/iam.tf](evidence/aws-terraform-project-context.md#source-q03) · setting/symbol: `ecs_trust       =`.

**Study:** [22 · aws iam roles and policies](generated/22-aws-iam-roles-and-policies.md) → [46 · iam policy evaluation and federation](generated/46-iam-policy-evaluation-and-federation.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html).

<a id="q04"></a>
### Q04 · What is the task execution role versus task role?

**Priority:** start now. **Evidence:** Current source.

The execution role lets the ECS agent pull images, write logs and inject allowed secrets. The task role supplies permissions to application code. These application task roles have no AWS API grants because the services use PostgreSQL, Kafka and HTTP; the bootstrap execution role has a distinct privileged secret scope.

**Project:** [infra/aws-ecs-dev/iam.tf](evidence/aws-terraform-project-context.md#source-q04) · setting/symbol: `execution_secrets =`.

**Study:** [22 · aws iam roles and policies](generated/22-aws-iam-roles-and-policies.md) → [54 · ecs networking identity and secrets](generated/54-ecs-networking-identity-and-secrets.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html).

<a id="q05"></a>
### Q05 · Is GitHub OIDC the same as marketplace login?

**Priority:** next. **Evidence:** Current source.

No. OpenID Connect (OIDC) can exchange a trusted workflow identity for temporary AWS credentials. The marketplace uses a JSON Web Token (JWT) and server-side role/ownership checks for customers. The preserved EC2 workflow has an optional OIDC deployment job; it does not establish ECS activation or replace application authentication.

**Project:** [.github/workflows/deploy-dev.yml](evidence/aws-terraform-project-context.md#source-q05) · setting/symbol: `role-to-assume:`.

**Study:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md) → [40 · aws release pipeline and oidc](generated/40-aws-release-pipeline-and-oidc.md) → [46 · iam policy evaluation and federation](generated/46-iam-policy-evaluation-and-federation.md) → [77 · terraform team ci and approval workflows](generated/77-terraform-team-ci-and-approval-workflows.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html).

<a id="q06"></a>
### Q06 · What makes a subnet private, and why use NAT?

**Priority:** start now. **Evidence:** Current source.

A route table controls where packets go; a public subnet has an internet-gateway route. Private tasks here have no public IP address and use a Network Address Translation (NAT) gateway for selected outbound access. Only the first private subnet has the active NAT route; the second supports database subnet-group eligibility. One zonal NAT is a failure/cost tradeoff.

**Project:** [infra/aws-ecs-dev/network.tf](evidence/aws-terraform-project-context.md#source-q06) · setting/symbol: `resource "aws_route_table" "private_active"`.

**Study:** [23 · aws vpc subnets and routing](generated/23-aws-vpc-subnets-and-routing.md) → [47 · vpc cidr ipv6 and subnet design](generated/47-vpc-cidr-ipv6-and-subnet-design.md) → [49 · private connectivity nat and endpoints](generated/49-private-connectivity-nat-and-endpoints.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html).

<a id="q07"></a>
### Q07 · How do security groups differ from network ACLs?

**Priority:** start now. **Evidence:** Current source.

A security group (SG) filters traffic for attached network interfaces and tracks connection state. A network access control list (NACL) filters subnet traffic without tracking state, so return ports matter. This source defines explicit SG edges, such as inquiries to catalog on 8182; it does not define custom NACL resources. Neither replaces application ownership checks.

**Project:** [infra/aws-ecs-dev/network.tf](evidence/aws-terraform-project-context.md#source-q07) · setting/symbol: `resource "aws_vpc_security_group_ingress_rule" "catalog_lookup"`.

**Study:** [24 · aws security groups and ssm](generated/24-aws-security-groups-and-ssm.md) → [48 · ingress egress security groups and nacls](generated/48-ingress-egress-security-groups-and-nacls.md) → [81 · network security local lab](generated/81-network-security-local-lab.md).

**Absent feature / official worked example:** Custom NACL resources are absent. Read AWS’s worked inbound/outbound rule tables and explain the response-port rules; this is an external example, not this project’s deployed policy. [Open example](https://docs.aws.amazon.com/vpc/latest/userguide/custom-network-acl.html).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/vpc/latest/userguide/custom-network-acl.html).

<a id="q08"></a>
### Q08 · Does having NAT bypass an S3 endpoint denial?

**Priority:** next. **Evidence:** Current source.

No. An Amazon Simple Storage Service (S3) gateway endpoint installs a more specific route for S3. Its policy still controls that path; a NAT default route does not override it. Here the endpoint permits image-layer and Amazon Linux package bucket reads, while other required AWS HTTPS destinations use the chosen NAT path.

**Project:** [infra/aws-ecs-dev/network.tf](evidence/aws-terraform-project-context.md#source-q08) · setting/symbol: `resource "aws_vpc_endpoint" "s3"`.

**Study:** [27 · aws s3 artifacts and secrets](generated/27-aws-s3-artifacts-and-secrets.md) → [49 · private connectivity nat and endpoints](generated/49-private-connectivity-nat-and-endpoints.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html).

<a id="q09"></a>
### Q09 · How do DNS, a certificate and ALB routing fit together?

**Priority:** start now. **Evidence:** Current source.

Domain Name System (DNS) resolves the application name. AWS Certificate Manager (ACM) proves ownership and provides the certificate for Transport Layer Security (TLS). The Application Load Balancer (ALB) listener terminates client TLS, forwards the approved host name and returns 403 for other hosts. Its frontend target uses HTTP internally; client TLS is not end-to-end HTTP encryption.

**Project:** [infra/aws-ecs-dev/ingress.tf](evidence/aws-terraform-project-context.md#source-q09) · setting/symbol: `resource "aws_lb_listener" "https"`.

**Study:** [50 · dns route53 acm and tls](generated/50-dns-route53-acm-and-tls.md) → [51 · alb target groups and health checks](generated/51-alb-target-groups-and-health-checks.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html).

<a id="q10"></a>
### Q10 · What do EC2, ECS and Fargate manage?

**Priority:** start now. **Evidence:** Current source.

Elastic Compute Cloud (EC2) supplies a virtual machine that you operate. Elastic Container Service (ECS) schedules tasks; Fargate runs them without your managing their hosts. This design prepares private Fargate application services and one private EC2 Kafka broker. The historical all-in-one EC2/SSM release remains a separate baseline.

**Project:** [infra/aws-ecs-dev/compute.tf](evidence/aws-terraform-project-context.md#source-q10) · setting/symbol: `requires_compatibilities = ["FARGATE"]`.

**Study:** [25 · aws ec2 ebs and bootstrap](generated/25-aws-ec2-ebs-and-bootstrap.md) → [53 · ecs fargate tasks and services](generated/53-ecs-fargate-tasks-and-services.md) → [56 · ec2 autoscaling and eks comparison](generated/56-ec2-autoscaling-and-eks-comparison.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html).

<a id="q11"></a>
### Q11 · Why deploy an image digest and check its architecture?

**Priority:** start now. **Evidence:** Current source.

A digest identifies image content; a mutable tag can point to different content later. Elastic Container Registry (ECR) stores the images. This publisher requires exact-source verification and builds linux/amd64 images for the source-defined X86_64 tasks. A successful image build alone proves neither an authorized release nor a healthy application.

**Project:** [scripts/aws-ecs-publish-local.mjs](evidence/aws-terraform-project-context.md#source-q11) · setting/symbol: `'--platform', 'linux/amd64'`.

**Study:** [26 · aws docker and ecr](generated/26-aws-docker-and-ecr.md) → [53 · ecs fargate tasks and services](generated/53-ecs-fargate-tasks-and-services.md) → [40 · aws release pipeline and oidc](generated/40-aws-release-pipeline-and-oidc.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_cannot_pull_image.html).

<a id="q12"></a>
### Q12 · Can four services use one RDS server without sharing their data?

**Priority:** start now. **Evidence:** Current source.

Yes. Relational Database Service (RDS) runs the PostgreSQL server, while each capability retains a separate database and login. bootstrapDatabases creates/reconciles those boundaries; normal services must not receive administrator credentials. Shared physical infrastructure still creates a common outage boundary, and this RDS definition is Single-AZ.

**Project:** [backend/src/operations/database-bootstrap.ts](evidence/aws-terraform-project-context.md#source-q12) · setting/symbol: `export async function bootstrapDatabases`.

**Study:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md) → [28 · aws data and messaging decisions](generated/28-aws-data-and-messaging-decisions.md) → [57 · rds postgresql backups and failover](generated/57-rds-postgresql-backups-and-failover.md).

**Official reference:** [Read the relevant guidance](https://www.postgresql.org/docs/17/manage-ag-createdb.html).

<a id="q13"></a>
### Q13 · Does encrypted storage mean connections and passwords are safe?

**Priority:** start now. **Evidence:** Current source.

It covers only one layer. RDS storage encryption, verified TLS connections and secret access permissions solve different problems. databaseOptions requires a trusted certificate authority (CA) for ECS and rejects database-URL TLS overrides. ECS injects scoped runtime secrets outside Terraform; rotation needs a coordinated client restart/reconnect and verification.

**Project:** [backend/src/common/connections.ts](evidence/aws-terraform-project-context.md#source-q13) · setting/symbol: `export function databaseOptions`.

**Study:** [27 · aws s3 artifacts and secrets](generated/27-aws-s3-artifacts-and-secrets.md) → [57 · rds postgresql backups and failover](generated/57-rds-postgresql-backups-and-failover.md) → [63 · kms secrets and rotation](generated/63-kms-secrets-and-rotation.md) → [74 · terraform sensitive and ephemeral values](generated/74-terraform-sensitive-and-ephemeral-values.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html).

<a id="q14"></a>
### Q14 · Is this managed Kafka, and can events arrive twice?

**Priority:** start now. **Evidence:** Current source.

The selected source uses self-managed Kafka on EC2, not Amazon Managed Streaming for Apache Kafka (MSK). An inquiry and outbox row commit together; the publisher marks delivery after a broker acknowledgment. A crash between acknowledgment and marking can cause a repeat, so notifications deduplicate by event identity. This is at-least-once delivery, not a cross-system exactly-once transaction.

**Project:** [backend/src/common/messaging.ts](evidence/aws-terraform-project-context.md#source-q14) · setting/symbol: `export class OutboxPublisher`.

**Study:** [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md) → [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md) → [28 · aws data and messaging decisions](generated/28-aws-data-and-messaging-decisions.md) → [59 · msk kafka security and operations](generated/59-msk-kafka-security-and-operations.md).

**Absent feature / official worked example:** MSK is absent. Read the official create/produce/consume/monitor/cleanup tutorial as an external example; do not run its paid steps for this questionnaire. [Open example](https://docs.aws.amazon.com/msk/latest/developerguide/getting-started.html).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/msk/latest/developerguide/getting-started.html).

<a id="q15"></a>
### Q15 · When do I choose S3 versus EBS?

**Priority:** next. **Evidence:** Current source.

S3 stores objects such as logs/artifacts and remote state; Elastic Block Store (EBS) is disk storage attached to EC2. The broker root EBS volume is encrypted but has delete_on_termination=true, so instance replacement threatens Kafka data. The state bucket has separate ownership and retention; it is not the operations/log bucket.

**Project:** [infra/aws-ecs-dev/compute.tf](evidence/aws-terraform-project-context.md#source-q15) · setting/symbol: `delete_on_termination = true`.

**Study:** [25 · aws ec2 ebs and bootstrap](generated/25-aws-ec2-ebs-and-bootstrap.md) → [27 · aws s3 artifacts and secrets](generated/27-aws-s3-artifacts-and-secrets.md) → [62 · s3 ebs efs storage and recovery](generated/62-s3-ebs-efs-storage-and-recovery.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html).

<a id="q16"></a>
### Q16 · What do live, serve and ready health checks prove?

**Priority:** start now. **Evidence:** Current source.

/health/live shows the process can answer. /health/serve checks PostgreSQL so HTTP serving can continue while Kafka retries. /health/ready also checks the messaging worker for inquiries/notifications. ECS uses serve for backend container checks; the ALB checks frontend /health. None proves the complete inquiry-to-notification journey.

**Project:** [backend/src/common/health.ts](evidence/aws-terraform-project-context.md#source-q16) · setting/symbol: `@Get('health/serve')`.

**Study:** [29 · aws observability and incidents](generated/29-aws-observability-and-incidents.md) → [51 · alb target groups and health checks](generated/51-alb-target-groups-and-health-checks.md) → [53 · ecs fargate tasks and services](generated/53-ecs-fargate-tasks-and-services.md) → [65 · cloudwatch agent logs metrics and alarms](generated/65-cloudwatch-agent-logs-metrics-and-alarms.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-troubleshooting.html).

<a id="q17"></a>
### Q17 · Do logs, alarms and backups prove recoverability?

**Priority:** next. **Evidence:** Dated execution: 2026-10-30.

No. Logs explain events; metrics quantify behavior; an alarm evaluates a metric. Recovery also needs a tested restore and measured Recovery Point Objective (RPO: acceptable data loss) and Recovery Time Objective (RTO: acceptable recovery duration). The October 30 record reports seven alarms without notification destinations/delivery proof and leaves runtime restore testing pending.

**Project:** [docs/aws-micro-completion-execution-2026-10-30.md](evidence/aws-terraform-project-context.md#source-q17) · setting/symbol: `The marketplace application is not activated`.

**Study:** [29 · aws observability and incidents](generated/29-aws-observability-and-incidents.md) → [65 · cloudwatch agent logs metrics and alarms](generated/65-cloudwatch-agent-logs-metrics-and-alarms.md) → [66 · cloudtrail config and audit evidence](generated/66-cloudtrail-config-and-audit-evidence.md) → [67 · otel tracing slos and incidents](generated/67-otel-tracing-slos-and-incidents.md) → [68 · disaster recovery and resilience testing](generated/68-disaster-recovery-and-resilience-testing.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html).

<a id="q18"></a>
### Q18 · Does stopping compute finish teardown and stop every charge?

**Priority:** start now. **Evidence:** Dated execution: 2026-10-31.

No. The October 31 record verifies EC2/RDS stopped at that checkpoint while ALB, NAT, storage and other allocations remained. RDS restarts after seven stopped days; that record gives November 7 at 07:22 AM EST. Storage and retained infrastructure may still bill. Expiry tags and budget alerts are not automatic deletion, and old prices are not a current estimate.

**Project:** [docs/aws-reversible-compute-stop-2026-10-31.md](evidence/aws-terraform-project-context.md#source-q18) · setting/symbol: `This is not full teardown`.

**Study:** [30 · aws costs and cleanup](generated/30-aws-costs-and-cleanup.md) → [62 · s3 ebs efs storage and recovery](generated/62-s3-ebs-efs-storage-and-recovery.md) → [69 · cloud cost allocation and optimization](generated/69-cloud-cost-allocation-and-optimization.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html).

<a id="q19"></a>
### Q19 · What are HCL blocks and Terraform dependencies?

**Priority:** start now. **Evidence:** Current source.

HashiCorp Configuration Language (HCL) describes resources, data lookups and expressions. References create dependency edges; file order does not. Here NAT references its subnet and explicitly waits for the internet gateway. Terraform manages a graph, so an apply can partially succeed before another resource fails.

**Project:** [infra/aws-ecs-dev/network.tf](evidence/aws-terraform-project-context.md#source-q19) · setting/symbol: `depends_on        = [aws_internet_gateway.dev]`.

**Study:** [32 · terraform hcl and first local lab](generated/32-terraform-hcl-and-first-local-lab.md) → [35 · terraform graph loops and modules](generated/35-terraform-graph-loops-and-modules.md) → [70 · terraform expressions and type system](generated/70-terraform-expressions-and-type-system.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/language/syntax/configuration).

<a id="q20"></a>
### Q20 · What do init, provider constraints and the lockfile do?

**Priority:** start now. **Evidence:** Current source.

init initializes backend access and provider installation. A provider implements resource APIs; its version constraint permits a range, while .terraform.lock.hcl records selected provider versions/checksums. Review upgrades deliberately. This application root configures one regional AWS provider; multi-region aliases are an extension, not evidence of multi-region deployment.

**Project:** [infra/aws-ecs-dev/versions.tf](evidence/aws-terraform-project-context.md#source-q20) · setting/symbol: `required_providers`.

**Study:** [33 · terraform providers versions and init](generated/33-terraform-providers-versions-and-init.md) → [72 · terraform provider aliases and environments](generated/72-terraform-provider-aliases-and-environments.md) → [75 · terraform import moves and provider upgrades](generated/75-terraform-import-moves-and-provider-upgrades.md).

**Absent feature / official worked example:** Multi-region provider aliases are absent in this application root. Use the official provider-configuration tutorial for the multiple-provider example before designing another environment. [Open example](https://developer.hashicorp.com/terraform/tutorials/configuration-language/configure-providers).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/tutorials/configuration-language/configure-providers).

<a id="q21"></a>
### Q21 · How do variables, locals, outputs and null differ?

**Priority:** start now. **Evidence:** Current source.

Variables are caller inputs, locals are derived values, and outputs expose a root/module result. null represents absence, not an empty string. Here null image_digests suppresses application definitions; hostname/certificate/client inputs separately gate HTTPS. Default protection settings in source do not reveal the inputs applied during the later cleanup transition.

**Project:** [infra/aws-ecs-dev/compute.tf](evidence/aws-terraform-project-context.md#source-q21) · setting/symbol: `active_services =`.

**Study:** [34 · terraform inputs locals and outputs](generated/34-terraform-inputs-locals-and-outputs.md) → [70 · terraform expressions and type system](generated/70-terraform-expressions-and-type-system.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/language/values/variables).

<a id="q22"></a>
### Q22 · Why use separate roots and stable for_each keys?

**Priority:** next. **Evidence:** Current source.

A root is a separately initialized configuration/state boundary; a child module is reusable configuration called by another. This project separates bootstrap, certificate, ECS and legacy EC2 roots. for_each uses capability names as addresses, preserving identity when map order changes. Splitting .tf files alone does not create separate states or security boundaries.

**Project:** [infra/aws-ecs-dev/network.tf](evidence/aws-terraform-project-context.md#source-q22) · setting/symbol: `services         =`.

**Study:** [35 · terraform graph loops and modules](generated/35-terraform-graph-loops-and-modules.md) → [71 · terraform modules and contracts](generated/71-terraform-modules-and-contracts.md) → [72 · terraform provider aliases and environments](generated/72-terraform-provider-aliases-and-environments.md) → [73 · terraform remote state and access control](generated/73-terraform-remote-state-and-access-control.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/tutorials/modules/module-use).

<a id="q23"></a>
### Q23 · What is state, and why separate the backend from the provider?

**Priority:** start now. **Evidence:** Current source.

State maps Terraform addresses to real resource identities. The backend stores/locks that state; the AWS provider manages cloud resource APIs. Their authentication can fail independently. The ECS example key is linked-in-node/ecs-dev/terraform.tfstate, distinct from the legacy key; bootstrap state does not automatically migrate into its new bucket.

**Project:** [infra/aws-ecs-dev/backend.hcl.example](evidence/aws-terraform-project-context.md#source-q23) · setting/symbol: `key =`.

**Study:** [36 · terraform state locking and bootstrap](generated/36-terraform-state-locking-and-bootstrap.md) → [73 · terraform remote state and access control](generated/73-terraform-remote-state-and-access-control.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/language/backend/s3).

<a id="q24"></a>
### Q24 · Why is a state lock useful?

**Priority:** start now. **Evidence:** Current source.

It prevents competing writers to the same state. The S3 backend example enables use_lockfile=true; relevant object/lock permissions are needed. Inspect the lock holder and wait for an active run. Only an owner-confirmed abandoned lock warrants controlled unlocking; disabling locks can corrupt shared lifecycle decisions.

**Project:** [infra/aws-ecs-dev/backend.hcl.example](evidence/aws-terraform-project-context.md#source-q24) · setting/symbol: `use_lockfile = true`.

**Study:** [36 · terraform state locking and bootstrap](generated/36-terraform-state-locking-and-bootstrap.md) → [73 · terraform remote state and access control](generated/73-terraform-remote-state-and-access-control.md) → [78 · terraform drift recovery and state surgery](generated/78-terraform-drift-recovery-and-state-surgery.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/language/state/locking).

<a id="q25"></a>
### Q25 · What exactly does saved-plan approval approve?

**Priority:** start now. **Evidence:** Current source.

A plan proposes actions; applying a saved binary executes its recorded decisions without another confirmation prompt. Project review binds the binary, source, inputs, provider lock, backend, identity and current costs. A changed source/context needs a new review. Plan JSON may contain sensitive values and belongs in private ignored storage.

**Project:** [scripts/aws-ecs-review-plan.py](evidence/aws-terraform-project-context.md#source-q25) · setting/symbol: `Saved plan source differs:`.

**Study:** [37 · terraform plan apply and drift](generated/37-terraform-plan-apply-and-drift.md) → [40 · aws release pipeline and oidc](generated/40-aws-release-pipeline-and-oidc.md) → [77 · terraform team ci and approval workflows](generated/77-terraform-team-ci-and-approval-workflows.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/cli/commands/plan).

<a id="q26"></a>
### Q26 · What should I do after drift or a partially failed apply?

**Priority:** next. **Evidence:** Dated execution: 2026-10-30.

Preserve the errors and resulting state, then compare observed resources with intended configuration. Successful operations are not automatically rolled back. The October 30 micro-completion record follows earlier partial failures and verifies preserved identities; that history cannot authorize replaying an old artifact. Prepare a fresh scoped recovery plan and new approval.

**Project:** [docs/aws-micro-completion-execution-2026-10-30.md](evidence/aws-terraform-project-context.md#source-q26) · setting/symbol: `All 104 existing resource identities are preserved`.

**Study:** [37 · terraform plan apply and drift](generated/37-terraform-plan-apply-and-drift.md) → [78 · terraform drift recovery and state surgery](generated/78-terraform-drift-recovery-and-state-surgery.md) → [80 · staged modernization and traceability](generated/80-staged-modernization-and-traceability.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/cli/commands/apply).

<a id="q27"></a>
### Q27 · How do replacement, import and moved addresses differ?

**Priority:** next. **Evidence:** Local/mock check definition; not a new execution.

Replacement recreates an object and may lose data. Import adopts an existing object into state; a moved declaration changes its Terraform address without intending recreation. The credential-free advanced lab teaches moves; importing live resources needs separately reviewed matching configuration and a safe plan. prevent_destroy is a limited configuration guard, not an AWS-wide deletion control.

**Project:** [docs/nodejs-aws-study-path/labs/terraform-advanced/run.py](evidence/aws-terraform-project-context.md#source-q27) · setting/symbol: `child.write_text(`.

**Study:** [38 · terraform lifecycle import and refactoring](generated/38-terraform-lifecycle-import-and-refactoring.md) → [75 · terraform import moves and provider upgrades](generated/75-terraform-import-moves-and-provider-upgrades.md) → [82 · terraform advanced local lab](generated/82-terraform-advanced-local-lab.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/tutorials/state/state-import).

<a id="q28"></a>
### Q28 · Does sensitive=true keep a secret out of state?

**Priority:** start now. **Evidence:** Current source.

No: sensitive normally redacts display, while values may remain in state/plans. Ephemeral values and supported write-only arguments have different version/provider constraints. This root defines secret containers and lets RDS manage the master password, leaving runtime values out of Terraform. Keep .env, state and plan artifacts out of Git and never paste secret output into troubleshooting notes.

**Project:** [infra/aws-ecs-dev/data.tf](evidence/aws-terraform-project-context.md#source-q28) · setting/symbol: `manage_master_user_password     = true`.

**Study:** [27 · aws s3 artifacts and secrets](generated/27-aws-s3-artifacts-and-secrets.md) → [63 · kms secrets and rotation](generated/63-kms-secrets-and-rotation.md) → [74 · terraform sensitive and ephemeral values](generated/74-terraform-sensitive-and-ephemeral-values.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/language/manage-sensitive-data).

<a id="q29"></a>
### Q29 · What do formatting, validation, mocks and runtime tests each establish?

**Priority:** start now. **Evidence:** Local/mock check definition; not a new execution.

Formatting checks style; validation checks configuration consistency; mock tests assert selected Terraform behavior without exercising AWS authorization or availability. This mock run asserts unpublished images cannot create application tasks. CI (continuous integration), release verification and later running HTTP/security/recovery tests answer different questions; a mock pass is not a deployed-system pass.

**Project:** [infra/aws-ecs-dev/tests/security.tftest.hcl](evidence/aws-terraform-project-context.md#source-q29) · setting/symbol: `run "infrastructure_without_unpublished_images"`.

**Study:** [39 · terraform validation and mocked tests](generated/39-terraform-validation-and-mocked-tests.md) → [76 · terraform testing and policy as code](generated/76-terraform-testing-and-policy-as-code.md) → [77 · terraform team ci and approval workflows](generated/77-terraform-team-ci-and-approval-workflows.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/language/tests/mocking).

<a id="q30"></a>
### Q30 · When would Lambda/API Gateway be an alternative?

**Priority:** extension. **Evidence:** Current source.

Lambda runs function invocations and API Gateway exposes HTTP APIs; compare request/event lifecycles, latency, state and operations with long-running services. This marketplace has no Lambda/API Gateway/DynamoDB application implementation. Study the official HTTP-to-function-to-table worked example, then explain which contracts would need preserving rather than describing it as a deployed migration.

**Project:** [infra/aws-ecs-dev/compute.tf](evidence/aws-terraform-project-context.md#source-q30) · setting/symbol: `resource "aws_ecs_service" "app"`.

**Study:** [58 · data caching and dynamodb design](generated/58-data-caching-and-dynamodb-design.md) → [61 · lambda apigateway and serverless design](generated/61-lambda-apigateway-and-serverless-design.md) → [80 · staged modernization and traceability](generated/80-staged-modernization-and-traceability.md) → [83 · professional cloud capstone and question bank](generated/83-professional-cloud-capstone-and-question-bank.md).

**Absent feature / official worked example:** Lambda, API Gateway and DynamoDB are absent application features. Read the official worked tutorial and identify its resource/cleanup steps; cloud execution needs separate authorization. [Open example](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html).

## Developer troubleshooting scenarios

For each scenario, preserve a redacted failure, test one hypothesis and rerun the same check after repair. Verification below is an expected recovery criterion, not an execution claim.

<a id="i01"></a>
### I01 · ECS cannot pull an image or exits before starting

**Priority:** next. **Evidence:** Current source; rehearsal scenario.

**Diagnostic checks:** Read the stopped task reason and service events; distinguish CannotPullContainerError from an application exit. Check the exact ECR account/Region/digest, linux/amd64 manifest, execution-role pull permissions, DNS and outbound route. A pre-start failure may produce no application log.

**Repair:** Correct the identified image/platform, scoped permission or network error in the source/release inputs. Keep approved digests and gates; submit a new reviewed release/plan rather than enabling public task IPs as a shortcut.

**Verify recovery:** After separately approved activation, inspect the new task revision/digest and stable running tasks, then serving health and the unchanged HTTP acceptance journey.

**Project:** [scripts/aws-ecs-publish-local.mjs](evidence/aws-terraform-project-context.md#source-i01) · setting/symbol: `'--platform', 'linux/amd64'`.

**Study:** [26 · aws docker and ecr](generated/26-aws-docker-and-ecr.md) → [49 · private connectivity nat and endpoints](generated/49-private-connectivity-nat-and-endpoints.md) → [53 · ecs fargate tasks and services](generated/53-ecs-fargate-tasks-and-services.md) → [54 · ecs networking identity and secrets](generated/54-ecs-networking-identity-and-secrets.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_cannot_pull_image.html).

<a id="i02"></a>
### I02 · Secret injection or an AWS action returns AccessDenied

**Priority:** next. **Evidence:** Current source; rehearsal scenario.

**Diagnostic checks:** Identify the denied action, resource and caller from redacted events. Secret injection uses the execution role; application AWS calls use the task role. Check trust, applicable deny/boundary/session controls and any key policy before changing grants.

**Repair:** Repair only the matching scoped grant/trust or secret reference. Keep ordinary task roles unprivileged unless a specified application AWS operation requires permission. Never attach broad administrator access or print secret values.

**Verify recovery:** Under approved execution, verify the intended task can start/use its own resource and that another capability still cannot obtain the privileged/master secret.

**Project:** [infra/aws-ecs-dev/iam.tf](evidence/aws-terraform-project-context.md#source-i02) · setting/symbol: `resource "aws_iam_role_policy" "execution"`.

**Study:** [22 · aws iam roles and policies](generated/22-aws-iam-roles-and-policies.md) → [46 · iam policy evaluation and federation](generated/46-iam-policy-evaluation-and-federation.md) → [54 · ecs networking identity and secrets](generated/54-ecs-networking-identity-and-secrets.md) → [63 · kms secrets and rotation](generated/63-kms-secrets-and-rotation.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html).

<a id="i03"></a>
### I03 · ALB returns 503 or a backend appears unhealthy

**Priority:** next. **Evidence:** Current source; rehearsal scenario.

**Diagnostic checks:** Check whether any target is registered before assuming an outage. Inspect ALB target-health reasons, hostname rule, port 8180 and SG path. Compare frontend /health, backend /health/serve and /health/ready directly on their authorized internal paths; management routes are not public proxy routes.

**Repair:** If the application is intentionally unactivated, report an empty target group instead of starting tasks. Otherwise fix the actual routing, database or process fault; a Kafka outage alone must not replace serve with strict ready in ECS serving checks.

**Verify recovery:** With approved runtime, require healthy registered frontend targets and backend serve responses. Test the business journey and strict ready separately. The October 30 empty-target 503 was infrastructure evidence, not successful marketplace serving.

**Project:** [backend/src/common/health.ts](evidence/aws-terraform-project-context.md#source-i03) · setting/symbol: `@Get('health/serve')`.

**Study:** [29 · aws observability and incidents](generated/29-aws-observability-and-incidents.md) → [51 · alb target groups and health checks](generated/51-alb-target-groups-and-health-checks.md) → [53 · ecs fargate tasks and services](generated/53-ecs-fargate-tasks-and-services.md) → [65 · cloudwatch agent logs metrics and alarms](generated/65-cloudwatch-agent-logs-metrics-and-alarms.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-troubleshooting.html).

<a id="i04"></a>
### I04 · Private tasks or broker packages time out despite NAT

**Priority:** next. **Evidence:** Current source; rehearsal scenario.

**Diagnostic checks:** Check the source subnet route association, DNS, outbound SG ports and NAT path. For S3 downloads, inspect the actual endpoint route and denied bucket/object; the S3 endpoint policy can intercept traffic even when NAT exists.

**Repair:** Fix the exact missing route or scoped endpoint bucket read. Broker package HTTP egress is broker-specific. Keep application tasks private; do not bypass policy with wildcard access or move databases into public subnets.

**Verify recovery:** After approved repair, repeat the same image-layer/package request from the affected private path, then verify service startup and forbidden ingress. A local source assertion alone cannot prove connectivity.

**Project:** [infra/aws-ecs-dev/network.tf](evidence/aws-terraform-project-context.md#source-i04) · setting/symbol: `resource "aws_vpc_endpoint" "s3"`.

**Study:** [23 · aws vpc subnets and routing](generated/23-aws-vpc-subnets-and-routing.md) → [48 · ingress egress security groups and nacls](generated/48-ingress-egress-security-groups-and-nacls.md) → [49 · private connectivity nat and endpoints](generated/49-private-connectivity-nat-and-endpoints.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html).

<a id="i05"></a>
### I05 · RDS connection fails with TLS, password or ownership errors

**Priority:** next. **Evidence:** Current source; rehearsal scenario.

**Diagnostic checks:** Classify timeout versus certificate/hostname verification failure versus authentication/SQL permission denial. Check the private 5432 SG path, DB_HOST/DB_NAME/DB_USER, DB_SSL CA settings and the intended secret version without logging its value.

**Repair:** Restore the correct CA/endpoint and service-owned credentials. For missing roles/databases use the separately approved bootstrap process. Never disable certificate verification or give normal services master credentials to make the error disappear.

**Verify recovery:** From the authorized runtime, verify TLS and SELECT 1, own-database reads/writes and denied cross-database access. Recheck migrations, restart/reconnect after a credential update and prove the application journey.

**Project:** [backend/src/common/connections.ts](evidence/aws-terraform-project-context.md#source-i05) · setting/symbol: `export function databaseOptions`.

**Study:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md) → [54 · ecs networking identity and secrets](generated/54-ecs-networking-identity-and-secrets.md) → [57 · rds postgresql backups and failover](generated/57-rds-postgresql-backups-and-failover.md) → [63 · kms secrets and rotation](generated/63-kms-secrets-and-rotation.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html).

<a id="i06"></a>
### I06 · Kafka fails TLS, SCRAM authentication or topic authorization

**Priority:** next. **Evidence:** Current source; rehearsal scenario.

**Diagnostic checks:** Confirm private broker DNS/9093 reachability, certificate CA/hostname, configured SCRAM mechanism, per-service username and broker topic/group ACLs. SCRAM is a password challenge mechanism; an ACL (access control list) controls allowed operations after authentication.

**Repair:** Correct the mismatched CA/credential or narrow producer/consumer ACL and provision the intended topic through the reviewed process. Keep verified TLS, scram-sha-512 and separate users; disabling security or resetting offsets is not a repair.

**Verify recovery:** After approved runtime recovery, show the intended producer can publish, consumer can durably consume and forbidden operations remain denied; ready and pending outbox counts must recover. This scenario does not claim a new cloud Kafka security drill.

**Project:** [backend/src/common/connections.ts](evidence/aws-terraform-project-context.md#source-i06) · setting/symbol: `export function kafkaOptions`.

**Study:** [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md) → [28 · aws data and messaging decisions](generated/28-aws-data-and-messaging-decisions.md) → [59 · msk kafka security and operations](generated/59-msk-kafka-security-and-operations.md) → [63 · kms secrets and rotation](generated/63-kms-secrets-and-rotation.md).

**Official reference:** [Read the relevant guidance](https://kafka.apache.org/40/security/authentication-using-sasl/).

<a id="i07"></a>
### I07 · Certificate is pending or the application hostname fails

**Priority:** next. **Evidence:** Current source; rehearsal scenario.

**Diagnostic checks:** Check authoritative DNS delegation, the exact ACM validation CNAME, issued certificate names and its ALB account/Region. A validation CNAME proves ownership; a separate application record must route users. Preserve the correct Host header and TLS server name when diagnosing.

**Repair:** Correct only the owned validation/application DNS or listener certificate/rule after approval. Keep validation records for renewal. A Cloud Map-owned private namespace must be managed through its owning service; do not insert arbitrary Route 53 records there.

**Verify recovery:** Confirm issued status and trusted TLS for the real hostname, then allowed-client routing and deliberate wrong-host rejection. DNS and TLS success still need a healthy application target before claiming a working site.

**Project:** [infra/aws-ecs-certificate/main.tf](evidence/aws-terraform-project-context.md#source-i07) · setting/symbol: `resource "aws_acm_certificate" "application"`.

**Study:** [50 · dns route53 acm and tls](generated/50-dns-route53-acm-and-tls.md) → [51 · alb target groups and health checks](generated/51-alb-target-groups-and-health-checks.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html).

<a id="i08"></a>
### I08 · Inquiry saved, but notification is missing or replayed

**Priority:** start now. **Evidence:** Current source; rehearsal scenario.

**Diagnostic checks:** Trace one inquiry/event ID through the transaction, pending outbox, acknowledged publish and notification row; inspect consumer/group errors without disclosing recipient data. Retrying after lost acknowledgment can legitimately repeat an event.

**Repair:** Restore the broker/consumer dependency and let persisted pending events retry. Retain event IDs, unique notification deduplication and HTTP idempotency comparisons. Do not fabricate a UI notification, discard the outbox or reset offsets blindly.

**Verify recovery:** Use the local controlled failure drill or approved cloud drill: persist an inquiry during broker loss, recover delivery, replay the same event and show exactly one notification; changed HTTP payload with the same key must still conflict.

**Project:** [backend/src/common/messaging.ts](evidence/aws-terraform-project-context.md#source-i08) · setting/symbol: `export class OutboxPublisher`.

**Study:** [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md) → [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md) → [29 · aws observability and incidents](generated/29-aws-observability-and-incidents.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html).

<a id="i09"></a>
### I09 · Terraform init cannot access the backend or acquire a lock

**Priority:** next. **Evidence:** Current source; rehearsal scenario.

**Diagnostic checks:** Read the first backend error, not just the final exit. Check the initialized root, actual bucket/Region/ECS key and backend caller permissions for state and lock objects. A functioning provider identity does not prove backend access. Inspect lock ID/owner and active CI runs.

**Repair:** Correct the intended backend/auth configuration without creating a competing state. Wait for a real lock holder. Any migration or owner-confirmed abandoned-lock recovery needs a controlled state decision; do not delete state or use -lock=false.

**Verify recovery:** The authorized operator reruns init against the intended backend, verifies workspace/key and state lineage, then prepares a fresh locked plan. Inspect it for unintended creates caused by accidentally empty state.

**Project:** [infra/aws-ecs-dev/backend.hcl.example](evidence/aws-terraform-project-context.md#source-i09) · setting/symbol: `use_lockfile = true`.

**Study:** [33 · terraform providers versions and init](generated/33-terraform-providers-versions-and-init.md) → [36 · terraform state locking and bootstrap](generated/36-terraform-state-locking-and-bootstrap.md) → [73 · terraform remote state and access control](generated/73-terraform-remote-state-and-access-control.md) → [78 · terraform drift recovery and state surgery](generated/78-terraform-drift-recovery-and-state-surgery.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/language/backend/s3).

<a id="i10"></a>
### I10 · Saved plan is stale, source changed, or apply partially failed

**Priority:** next. **Evidence:** Dated execution: 2026-10-30; recovery rehearsal based on recorded partial failures.

**Diagnostic checks:** Preserve the exact binary, errors and resulting protected state. Check source/input/provider/backend bindings and compare recorded versus observed resources. Distinguish successful creates from the failed step; do not infer transactional rollback.

**Repair:** Correct the cause, reconcile identities and prepare a fresh complete plan plus current costs for review/approval. Do not force the old binary, remove checks, edit state blindly or retry a previously rejected destroy through another route.

**Verify recovery:** Require the newly approved exact plan to finish and verify its actual resource scope/read-back. A subsequent no-change plan is infrastructure evidence; runtime, data recovery and acceptance remain separate gates.

**Project:** [docs/aws-micro-completion-execution-2026-10-30.md](evidence/aws-terraform-project-context.md#source-i10) · setting/symbol: `fresh full Terraform plan reports`.

**Study:** [37 · terraform plan apply and drift](generated/37-terraform-plan-apply-and-drift.md) → [38 · terraform lifecycle import and refactoring](generated/38-terraform-lifecycle-import-and-refactoring.md) → [77 · terraform team ci and approval workflows](generated/77-terraform-team-ci-and-approval-workflows.md) → [78 · terraform drift recovery and state surgery](generated/78-terraform-drift-recovery-and-state-surgery.md).

**Official reference:** [Read the relevant guidance](https://developer.hashicorp.com/terraform/tutorials/state/resource-drift).

<a id="i11"></a>
### I11 · Rollout fails, or the old image cannot use the new schema

**Priority:** next. **Evidence:** Current source; rehearsal scenario.

**Diagnostic checks:** Check deployment events, circuit-breaker status, prior completed deployment, image digest, serve/ready and migration compatibility. The legacy SSM rollback script and prepared ECS circuit breaker are different mechanisms; neither reverses committed SQL automatically.

**Repair:** For an approved rollout, restore a known compatible task revision only when schema permits. Otherwise use a reviewed roll-forward or tested backup/restore decision with data-loss boundaries. Keep migrations backward compatible when possible.

**Verify recovery:** Prove stable tasks, unchanged 48-check acceptance with zero failures, durable data and notification recovery. Measure restore loss/time if used. With current source alone, record this as a recovery plan, not a successful AWS rollback.

**Project:** [infra/aws-ecs-dev/compute.tf](evidence/aws-terraform-project-context.md#source-i11) · setting/symbol: `deployment_circuit_breaker`.

**Study:** [40 · aws release pipeline and oidc](generated/40-aws-release-pipeline-and-oidc.md) → [41 · aws ssm deployment and rollback](generated/41-aws-ssm-deployment-and-rollback.md) → [55 · ecs scaling and deployment strategies](generated/55-ecs-scaling-and-deployment-strategies.md) → [57 · rds postgresql backups and failover](generated/57-rds-postgresql-backups-and-failover.md) → [68 · disaster recovery and resilience testing](generated/68-disaster-recovery-and-resilience-testing.md) → [80 · staged modernization and traceability](generated/80-staged-modernization-and-traceability.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html).

<a id="i12"></a>
### I12 · Charges continue after EC2 and RDS were stopped

**Priority:** start now. **Evidence:** Dated execution: 2026-10-31; retained-cost diagnosis rehearsal.

**Diagnostic checks:** Reconcile the dated stop receipt with current billing/inventory only during a separately authorized inspection. Account for NAT/EIP, ALB, EBS, RDS storage/backups, logs, S3 versions and secrets. Billing can lag. The October 31 receipt records a November 7 RDS automatic restart.

**Repair:** Prepare a current retained-resource and cost review for the deployment owner. Full teardown remains unexecuted after automatic-review rejection. Cleanup-transition deletion settings remained changed; do not treat earlier protected defaults as current or bypass the rejection.

**Verify recovery:** Only actual approved deletion plus scoped inventory/retention and later billing checks establish completed cleanup. This learning task performs none of those operations and gives no fresh cost estimate or live stopped-status claim.

**Project:** [docs/aws-reversible-compute-stop-2026-10-31.md](evidence/aws-terraform-project-context.md#source-i12) · setting/symbol: `previously approved cleanup-transition settings remain`.

**Study:** [30 · aws costs and cleanup](generated/30-aws-costs-and-cleanup.md) → [62 · s3 ebs efs storage and recovery](generated/62-s3-ebs-efs-storage-and-recovery.md) → [69 · cloud cost allocation and optimization](generated/69-cloud-cost-allocation-and-optimization.md) → [78 · terraform drift recovery and state surgery](generated/78-terraform-drift-recovery-and-state-surgery.md) → [80 · staged modernization and traceability](generated/80-staged-modernization-and-traceability.md).

**Official reference:** [Read the relevant guidance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html).

## Check your understanding

Pick three questions and one scenario. Explain each answer, open its source setting, predict a failure and name the evidence that would verify recovery. If you cannot do that, return to its first mapped lesson. Keep personal answers in your existing notes; do not edit generated lesson IDs or mark a cloud drill complete without execution.

Content/link/source validation runs through `python3 scripts/check-cloud-study.py`; the companion map is machine-readable and included in the managed ZIP. Offline validation cannot prove that external documentation remains reachable or that AWS permissions/networking work. The initial review was local-only. Local validation does not itself publish this guide or update the live Study Desk reader; authorized GitHub publication is recorded separately.
