# NodeJs/AWS

Study the Node.js concepts and libraries used by each service, one mechanism at a time. Explanations use short paragraphs, real source excerpts and fixed GitHub line links.

Start with the [roadmap](generated/00-roadmap-and-mastery-gates.md), or choose Identity (08), Catalog (06–07), Inquiries (09) or Notifications (10). Common NestJS tools are in 05.

## Read or download

Read these guides directly on GitHub, or [download the complete study pack](NodeJs-AWS-study-pack.zip). The [service technical handbooks](../nodejs-beginner/README.md) organize tools by capability.

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

Start with [20 · the cloud roadmap](generated/20-cloud-roadmap-and-lab.md). This adds 24 focused lessons to the original 20: AWS foundations, operations/tradeoffs, eight Terraform lessons, release delivery, troubleshooting and interview practice. The default hands-on lab runs locally with Terraform’s built-in provider; it needs no AWS credentials and provisions no cloud resources.

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
