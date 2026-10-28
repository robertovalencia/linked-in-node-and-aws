# NodeJs/AWS

Study the Node.js concepts and libraries used by each service, one mechanism at a time. Explanations use short paragraphs, real source excerpts and fixed GitHub line links.

Start with the [roadmap](generated/00-roadmap-and-mastery-gates.md), or choose Identity (08), Catalog (06–07), Inquiries (09) or Notifications (10). Common NestJS tools are in 05.

## Follow the complete setup and delivery process

Start with [How this project was set up and verified](walkthroughs/README.md): eight short chapters explaining tools/local startup, application flow, AWS identity and cost decisions, Terraform roots/state/plans, hostname/DNS/certificate setup, future deployment/security/recovery, lesson building/review, and GitHub/Study Desk publication. Each chapter breaks the work into small concepts, links the real files, explains expected observations and common failures, and ends with a comprehension check. Historical execution, safe local reproduction and pending cloud work are explicitly separated. These supplementary chapters are included in the ZIP without changing existing numbered lesson IDs.

## Learn the AWS console visually

Open the [AWS screenshot study guide](visuals/README.md) for an actual blank sign-in capture and nine official AWS service examples, with small field explanations, source links, related lessons and recall questions. Official examples are clearly marked as unrelated to this account; remote example images require internet access. The guide includes the account-ID/IAM-user/role distinction that explained our sign-in issue.

## Read or download

Read these guides directly on GitHub, or [download the complete study pack](NodeJs-AWS-study-pack.zip). The [service technical handbooks](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/nodejs-beginner/README.md) organize tools by capability.

## Guides

- [00 · Roadmap and mastery gates](generated/00-roadmap-and-mastery-gates.md)
- [01 · JavaScript: values, closures, objects and collections](generated/01-javascript-language-foundations.md)
- [02 · TypeScript: erased types, narrowing, generics and ESM](generated/02-typescript-and-modules.md)
- [03 · Node runtime: event loop, promises and resource limits](generated/03-node-runtime-and-async.md)
- [04 · Node APIs: HTTP, Buffer, files, paths and processes](generated/04-node-http-processes-and-streams.md)
- [05 · NestJS tools: decorators, injection and lifecycle](generated/05-nestjs-service-wiring.md)
- [06 · Catalog tools: Zod, coercion, closures and JSONB](generated/06-http-contracts-and-validation.md)
- [07 · pg tools: pools, transactions, locks and migrations](generated/07-postgresql-and-transactions.md)
- [08 · Identity tools: scrypt, Buffer, JWT, Zod and Map](generated/08-identity-jwt-and-security.md)
- [09 · Inquiries tools: fetch, hashes, UUIDs and transaction locks](generated/09-inquiries-idempotency-and-outbox.md)
- [10 · Messaging tools: KafkaJS, offsets, Buffer and deduplication](generated/10-kafka-inbox-and-notifications.md)
- [11 · React tools: state, props, refs and controlled inputs](generated/11-react-foundations-and-state.md)
- [12 · React tools: effects, abort, HTTP errors and portals](generated/12-react-effects-http-and-accessibility.md)
- [13 · Testing tools: Jest, Vitest, mocks, types and browsers](generated/13-testing-and-debugging.md)
- [14 · Runtime tools: npm, tsc, Docker and process supervision](generated/14-local-runtime-and-containers.md)
- [15 · Infrastructure tools: Terraform, IAM, SSM, ECR and releases](generated/15-aws-terraform-and-delivery.md)
- [16 · Reliability concepts: timeouts, budgets, consistency and recovery](generated/16-reliability-and-senior-design.md)
- [17 · Delivery tools: specifications, CI, quality gates and traceability](generated/17-ai-assisted-engineering-and-toolchain.md)
- [18 · Interview practice: explain the mechanism, then prove it](generated/18-interview-drills-and-capstone.md)
- [19 · Source and interview coverage map](generated/19-source-and-requirement-coverage.md)

## AWS and Terraform: step-by-step extension

Start with [20 · the cloud roadmap](generated/20-cloud-roadmap-and-lab.md). The foundation block adds 24 focused lessons to the original 20: AWS foundations, operations/tradeoffs, eight Terraform lessons, release delivery, troubleshooting and interview practice. The default hands-on lab runs locally with Terraform’s built-in provider; it needs no AWS credentials and provisions no cloud resources.

- [20 · AWS and Terraform: a practical learning roadmap](generated/20-cloud-roadmap-and-lab.md)
- [21 · AWS accounts, regions, resource names and CLI identity](generated/21-aws-accounts-regions-and-cli.md)
- [22 · IAM: principals, roles, trust and scoped permissions](generated/22-aws-iam-roles-and-policies.md)
- [23 · Networking: CIDR, VPCs, subnets and route tables](generated/23-aws-vpc-subnets-and-routing.md)
- [24 · Security groups, SSM access and encrypted tunnels](generated/24-aws-security-groups-and-ssm.md)
- [25 · EC2, AMIs, EBS, metadata and bootstrap](generated/25-aws-ec2-ebs-and-bootstrap.md)
- [26 · Docker images, ECR, tags, digests and scanning](generated/26-aws-docker-and-ecr.md)
- [27 · S3 release objects, runtime secrets and state boundaries](generated/27-aws-s3-artifacts-and-secrets.md)
- [28 · Cloud data choices: PostgreSQL, Kafka and managed alternatives](generated/28-aws-data-and-messaging-decisions.md)
- [29 · Observability: health, logs, metrics, audit and incidents](generated/29-aws-observability-and-incidents.md)
- [30 · AWS costs, budgets, retention and complete cleanup](generated/30-aws-costs-and-cleanup.md)
- [31 · From this dev stack to a production design](generated/31-aws-production-design-tradeoffs.md)
- [32 · Terraform: HCL and your first local lab](generated/32-terraform-hcl-and-first-local-lab.md)
- [33 · Terraform: providers, version constraints and init](generated/33-terraform-providers-versions-and-init.md)
- [34 · Terraform: inputs, locals and output contracts](generated/34-terraform-inputs-locals-and-outputs.md)
- [35 · Terraform: dependency graphs, loops and module boundaries](generated/35-terraform-graph-loops-and-modules.md)
- [36 · Terraform: state, locking and the bootstrap boundary](generated/36-terraform-state-locking-and-bootstrap.md)
- [37 · Terraform: plans, apply, drift and review](generated/37-terraform-plan-apply-and-drift.md)
- [38 · Terraform: lifecycle, import and safe address refactoring](generated/38-terraform-lifecycle-import-and-refactoring.md)
- [39 · Terraform: validation, mocked tests and evidence limits](generated/39-terraform-validation-and-mocked-tests.md)
- [40 · Release delivery: GitHub verification, OIDC and exact identity](generated/40-aws-release-pipeline-and-oidc.md)
- [41 · Deployment on SSM: readiness, acceptance and rollback](generated/41-aws-ssm-deployment-and-rollback.md)
- [42 · AWS and Terraform troubleshooting workbook](generated/42-aws-terraform-troubleshooting-workbook.md)
- [43 · Capstone: explain, review and defend the AWS/Terraform design](generated/43-aws-terraform-capstone-and-interview.md)

Each lesson links the actual pinned GitHub implementation, walks the mechanism, gives observable practice evidence and asks recall questions with answers. Complete the gates in lesson 20 rather than rushing through topic names. The [local Terraform lab](labs/terraform-local/README.md) and [source excerpt manifest](cloud-source-excerpts.json) are included in the download. Personal progress remains in its existing protected file.

## How to use a concept card

Read What and How. Open Real code and explain its lines. Answer the question without notes, then complete the practice check.

Code blocks are source excerpts unless explicitly labeled as runnable practice. Pinned code links keep their meaning when the branch later changes.

The existing implementation and suggested extensions are labeled separately. Personal progress and saved notes are preserved.


## Complete professional AWS and Terraform core

The path now has **84 lessons**, including **64 cloud/Terraform lessons (20–83)**. Start with [44 · the full syllabus and concept checklist](generated/44-cloud-complete-syllabus-and-mastery-map.md) for the broad professional route. Keep 20–43 as foundations; 44–83 teach important concepts even when no matching resource exists in the current project. New examples are labeled illustrative and are not claims of deployment.

- [44 · Cloud curriculum: syllabus and mastery map](generated/44-cloud-complete-syllabus-and-mastery-map.md)
- [45 · AWS accounts, governance, and landing zones](generated/45-aws-account-governance-and-landing-zones.md)
- [46 · IAM policy evaluation, federation, and temporary access](generated/46-iam-policy-evaluation-and-federation.md)
- [47 · VPC addressing, IPv6, and subnet design](generated/47-vpc-cidr-ipv6-and-subnet-design.md)
- [48 · Ingress, egress, security groups, and network ACLs](generated/48-ingress-egress-security-groups-and-nacls.md)
- [49 · Private connectivity, NAT, and VPC endpoints](generated/49-private-connectivity-nat-and-endpoints.md)
- [50 · DNS, Route 53, ACM, and TLS](generated/50-dns-route53-acm-and-tls.md)
- [51 · ALB listeners, target groups, and health checks](generated/51-alb-target-groups-and-health-checks.md)
- [52 · CloudFront, private S3 origins, and cache correctness](generated/52-cloudfront-s3-origins-and-caching.md)
- [53 · ECS Fargate task definitions and services](generated/53-ecs-fargate-tasks-and-services.md)
- [54 · ECS networking, workload identity, and secrets](generated/54-ecs-networking-identity-and-secrets.md)
- [55 · ECS service scaling and deployment strategies](generated/55-ecs-scaling-and-deployment-strategies.md)
- [56 · EC2 Auto Scaling and EKS: choosing an operating model](generated/56-ec2-autoscaling-and-eks-comparison.md)
- [57 · RDS PostgreSQL: backups, failover, and connection recovery](generated/57-rds-postgresql-backups-and-failover.md)
- [58 · Caching and DynamoDB access-pattern design](generated/58-data-caching-and-dynamodb-design.md)
- [59 · Amazon MSK: Kafka security and operations](generated/59-msk-kafka-security-and-operations.md)
- [60 · SQS, SNS, EventBridge, and workflow orchestration](generated/60-sqs-sns-eventbridge-and-workflows.md)
- [61 · Lambda, API Gateway, and serverless application design](generated/61-lambda-apigateway-and-serverless-design.md)
- [62 · S3, EBS, EFS, and recoverable storage](generated/62-s3-ebs-efs-storage-and-recovery.md)
- [63 · KMS, Secrets Manager, and credential rotation](generated/63-kms-secrets-and-rotation.md)
- [64 · WAF, DDoS protection and security findings](generated/64-waf-shield-and-security-detection.md)
- [65 · CloudWatch agent, logs, metrics and alarms](generated/65-cloudwatch-agent-logs-metrics-and-alarms.md)
- [66 · CloudTrail, Config and audit evidence](generated/66-cloudtrail-config-and-audit-evidence.md)
- [67 · OpenTelemetry, tracing, SLOs and incident response](generated/67-otel-tracing-slos-and-incidents.md)
- [68 · Disaster recovery, backup and resilience testing](generated/68-disaster-recovery-and-resilience-testing.md)
- [69 · Cloud cost allocation and optimization concepts](generated/69-cloud-cost-allocation-and-optimization.md)
- [70 · Terraform expressions and type system](generated/70-terraform-expressions-and-type-system.md)
- [71 · Terraform modules and contracts](generated/71-terraform-modules-and-contracts.md)
- [72 · Terraform provider aliases and environments](generated/72-terraform-provider-aliases-and-environments.md)
- [73 · Terraform remote state and access control](generated/73-terraform-remote-state-and-access-control.md)
- [74 · Terraform sensitive and ephemeral values](generated/74-terraform-sensitive-and-ephemeral-values.md)
- [75 · Terraform import, moves and provider upgrades](generated/75-terraform-import-moves-and-provider-upgrades.md)
- [76 · Terraform testing and policy as code](generated/76-terraform-testing-and-policy-as-code.md)
- [77 · Terraform team CI and approval workflows](generated/77-terraform-team-ci-and-approval-workflows.md)
- [78 · Terraform drift recovery and state surgery](generated/78-terraform-drift-recovery-and-state-surgery.md)
- [79 · Threat modeling and architecture security review](generated/79-cloud-threat-model-and-security-review.md)
- [80 · Staged modernization and deployment-owner coordination](generated/80-staged-modernization-and-traceability.md)
- [81 · Local network-security reasoning lab](generated/81-network-security-local-lab.md)
- [82 · Terraform advanced local lab](generated/82-terraform-advanced-local-lab.md)
- [83 · Professional AWS/Terraform capstone and question bank](generated/83-professional-cloud-capstone-and-question-bank.md)

Practice with the [network-security lab](labs/network-security/README.md) and [advanced Terraform module/state lab](labs/terraform-advanced/README.md), both credential-free. Existing personal progress and saved notes remain separate from generated material. The [cost-first deployment handoff](deployment-handoff.md) was acknowledged by the owner chat; [coordination status](deployment-coordination.json) records the latest owner report and pending deployment gates. This curriculum does not select, price or deploy the modernization.


Deployment status: the owner published reviewed plans and costs on 2026-10-28; only certificate issuance is verified. Bootstrap and application provisioning remain pending approval. Consult the deployment coordination record and owner report rather than inferring live resources from these learning examples.
