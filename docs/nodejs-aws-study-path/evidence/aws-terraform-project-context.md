# Project context for the AWS/Terraform questionnaire

Inspected November 2, 2026 in the real checkout. These are literal excerpts, with source file paths, symbols, line ranges and file SHA-256 digests at inspection. Source/records that differed from HEAD at inspection are snapshots of that local checkpoint. The two full dated execution records are preserved under `questionnaire-records/` with their inspected hashes; publication does not turn them into current AWS observations. Dated records establish only their stated checkpoint; no fresh AWS query was made. The validator checks each excerpt and symbol against the selected source checkout.

[Questionnaire](../aws-terraform-questionnaire.md) · [Study index](../README.md)

<a id="source-q01"></a>
## Q01 · `infra/aws-ecs-dev/network.tf`

**Scope:** Current source. **Symbol/setting:** `capabilities     =`. **Lines at inspection:** 15–24.
**File SHA-256 at inspection:** `245073d06aac72e825494ef35a0db762e347162ea28bf3ae964528da04677873`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/network.tf#L15-L24)

````hcl
  azs              = slice(sort(data.aws_availability_zones.available.names), 0, 2)
  capabilities     = { identity = 8181, catalog = 8182, inquiries = 8183, notifications = 8184 }
  services         = merge(local.capabilities, { frontend = 8180 })
  brokers_clients  = toset(["inquiries", "notifications"])
  secret_names     = toset(concat(keys(local.capabilities), ["shared", "broker"]))
  arn_prefix       = "arn:${data.aws_partition.current.partition}"
}
resource "aws_vpc" "dev" {
  cidr_block           = "10.85.0.0/16"
  enable_dns_hostnames = true
````

<a id="source-q02"></a>
## Q02 · `infra/aws-ecs-dev/versions.tf`

**Scope:** Current source. **Symbol/setting:** `region = var.region`. **Lines at inspection:** 8–13.
**File SHA-256 at inspection:** `7e17ae4bc5f302ec96a74c7f0427aba6e91c3299033d3789f30917a5fc61ea51`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/versions.tf#L8-L13)

````hcl
provider "aws" {
  region = var.region
  default_tags {
    tags = { Project = var.project, Environment = "ecs-dev", ManagedBy = "Terraform", Owner = var.owner, ExpiresAt = var.expires_at }
  }
}
````

<a id="source-q03"></a>
## Q03 · `infra/aws-ecs-dev/iam.tf`

**Scope:** Current source. **Symbol/setting:** `ecs_trust       =`. **Lines at inspection:** 2–11.
**File SHA-256 at inspection:** `31d3823907c0c627f5d6d0c4af20c2d6bb7c4a7d552ee0182c704bb47babc704`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/iam.tf#L2-L11)

````hcl
  execution_names = var.image_digests == null ? toset([]) : toset(concat(keys(local.services), ["bootstrap"]))
  ecs_trust       = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Service = "ecs-tasks.amazonaws.com" }, Action = "sts:AssumeRole", Condition = { StringEquals = { "aws:SourceAccount" = data.aws_caller_identity.current.account_id }, ArnLike = { "aws:SourceArn" = "${local.arn_prefix}:ecs:${var.region}:${data.aws_caller_identity.current.account_id}:*" } } }] })
  execution_secrets = {
    frontend      = []
    identity      = [aws_secretsmanager_secret.runtime["identity"].arn, aws_secretsmanager_secret.runtime["shared"].arn]
    catalog       = [aws_secretsmanager_secret.runtime["catalog"].arn, aws_secretsmanager_secret.runtime["shared"].arn]
    inquiries     = [aws_secretsmanager_secret.runtime["inquiries"].arn, aws_secretsmanager_secret.runtime["shared"].arn]
    notifications = [aws_secretsmanager_secret.runtime["notifications"].arn, aws_secretsmanager_secret.runtime["shared"].arn]
    bootstrap     = concat([for k in keys(local.capabilities) : aws_secretsmanager_secret.runtime[k].arn], [aws_db_instance.dev.master_user_secret[0].secret_arn])
  }
````

<a id="source-q04"></a>
## Q04 · `infra/aws-ecs-dev/iam.tf`

**Scope:** Current source. **Symbol/setting:** `execution_secrets =`. **Lines at inspection:** 3–12.
**File SHA-256 at inspection:** `31d3823907c0c627f5d6d0c4af20c2d6bb7c4a7d552ee0182c704bb47babc704`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/iam.tf#L3-L12)

````hcl
  ecs_trust       = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Service = "ecs-tasks.amazonaws.com" }, Action = "sts:AssumeRole", Condition = { StringEquals = { "aws:SourceAccount" = data.aws_caller_identity.current.account_id }, ArnLike = { "aws:SourceArn" = "${local.arn_prefix}:ecs:${var.region}:${data.aws_caller_identity.current.account_id}:*" } } }] })
  execution_secrets = {
    frontend      = []
    identity      = [aws_secretsmanager_secret.runtime["identity"].arn, aws_secretsmanager_secret.runtime["shared"].arn]
    catalog       = [aws_secretsmanager_secret.runtime["catalog"].arn, aws_secretsmanager_secret.runtime["shared"].arn]
    inquiries     = [aws_secretsmanager_secret.runtime["inquiries"].arn, aws_secretsmanager_secret.runtime["shared"].arn]
    notifications = [aws_secretsmanager_secret.runtime["notifications"].arn, aws_secretsmanager_secret.runtime["shared"].arn]
    bootstrap     = concat([for k in keys(local.capabilities) : aws_secretsmanager_secret.runtime[k].arn], [aws_db_instance.dev.master_user_secret[0].secret_arn])
  }
}
````

<a id="source-q05"></a>
## Q05 · `.github/workflows/deploy-dev.yml`

**Scope:** Current source. **Symbol/setting:** `role-to-assume:`. **Lines at inspection:** 80–89.
**File SHA-256 at inspection:** `022a3fde2671ef6c53af6417754eabd544c3acb07e99bd2aca01ae6580f1ebc1`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/.github/workflows/deploy-dev.yml#L80-L89)

````text
        with:
          role-to-assume: ${{ vars.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ${{ vars.AWS_REGION }}
      - uses: aws-actions/amazon-ecr-login@v2
      - uses: docker/setup-buildx-action@v3
      - name: Build and publish immutable source images
        run: |
          test -n "$BACKEND_REPOSITORY" && test -n "$FRONTEND_REPOSITORY"
          for app in backend frontend; do
            repo_var="${app^^}_REPOSITORY"
````

<a id="source-q06"></a>
## Q06 · `infra/aws-ecs-dev/network.tf`

**Scope:** Current source. **Symbol/setting:** `resource "aws_route_table" "private_active"`. **Lines at inspection:** 64–73.
**File SHA-256 at inspection:** `245073d06aac72e825494ef35a0db762e347162ea28bf3ae964528da04677873`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/network.tf#L64-L73)

````hcl
}
resource "aws_route_table" "private_active" {
  vpc_id = aws_vpc.dev.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.dev.id
  }
}
resource "aws_route_table_association" "private_active" {
  subnet_id      = aws_subnet.private[0].id
````

<a id="source-q07"></a>
## Q07 · `infra/aws-ecs-dev/network.tf`

**Scope:** Current source. **Symbol/setting:** `resource "aws_vpc_security_group_ingress_rule" "catalog_lookup"`. **Lines at inspection:** 154–163.
**File SHA-256 at inspection:** `245073d06aac72e825494ef35a0db762e347162ea28bf3ae964528da04677873`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/network.tf#L154-L163)

````hcl
}
resource "aws_vpc_security_group_ingress_rule" "catalog_lookup" {
  security_group_id            = aws_security_group.service["catalog"].id
  referenced_security_group_id = aws_security_group.service["inquiries"].id
  ip_protocol                  = "tcp"
  from_port                    = 8182
  to_port                      = 8182
}
resource "aws_vpc_security_group_egress_rule" "catalog_lookup" {
  security_group_id            = aws_security_group.service["inquiries"].id
````

<a id="source-q08"></a>
## Q08 · `infra/aws-ecs-dev/network.tf`

**Scope:** Current source. **Symbol/setting:** `resource "aws_vpc_endpoint" "s3"`. **Lines at inspection:** 81–90.
**File SHA-256 at inspection:** `245073d06aac72e825494ef35a0db762e347162ea28bf3ae964528da04677873`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/network.tf#L81-L90)

````hcl
}
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.dev.id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private_active.id, aws_route_table.private_standby.id]
  # ECR layers and AL2023 package repositories use regional AWS-owned S3 buckets.
  # The gateway route also intercepts package downloads, so NAT cannot repair a denied endpoint policy.
  policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = "*", Action = ["s3:GetObject"], Resource = ["${local.arn_prefix}:s3:::prod-${var.region}-starport-layer-bucket/*", "${local.arn_prefix}:s3:::al2023-repos-${var.region}-de612dc2/*"] }] })
}
````

<a id="source-q09"></a>
## Q09 · `infra/aws-ecs-dev/ingress.tf`

**Scope:** Current source. **Symbol/setting:** `resource "aws_lb_listener" "https"`. **Lines at inspection:** 35–44.
**File SHA-256 at inspection:** `52ad5a60b8213f09415abfbfadad83cc9a74b81df6fe8d04f1e41992cf8d3d23`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/ingress.tf#L35-L44)

````hcl
}
resource "aws_lb_listener" "https" {
  count             = local.https_configured ? 1 : 0
  load_balancer_arn = aws_lb.dev.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn
  lifecycle {
    precondition {
````

<a id="source-q10"></a>
## Q10 · `infra/aws-ecs-dev/compute.tf`

**Scope:** Current source. **Symbol/setting:** `requires_compatibilities = ["FARGATE"]`. **Lines at inspection:** 137–146.
**File SHA-256 at inspection:** `5a3c8e35c1077e7e00753cc264874de2a42cfa6dd87bdb5bfd12ceb34ce2e8d2`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/compute.tf#L137-L146)

````hcl
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.execution[each.key].arn
  task_role_arn            = aws_iam_role.task[each.key].arn
  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }
````

<a id="source-q11"></a>
## Q11 · `scripts/aws-ecs-publish-local.mjs`

**Scope:** Current source. **Symbol/setting:** `'--platform', 'linux/amd64'`. **Lines at inspection:** 106–115.
**File SHA-256 at inspection:** `93323c162fd871b1e030d19a476eee663964b5ab32ccd47d0723d420991441f1`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/scripts/aws-ecs-publish-local.mjs#L106-L115)

````text
      cleanSource(sha);
      execute('docker', ['buildx', 'build', '--platform', 'linux/amd64', '--label', `org.opencontainers.image.revision=${sha}`, '--push', '--tag', `${repo}:${sha}`, '--metadata-file', join(evidence, `${app}-build.json`), join(source, app)]);
      digest = getDigest();
    }
    requireThat(/^sha256:[a-f0-9]{64}$/.test(digest || ''), 'ECR did not return a valid immutable image digest');
    const image = `${repo}@${digest}`;
    execute('docker', ['pull', '--platform', 'linux/amd64', image]);
    const inspection = json('docker', ['image', 'inspect', image]);
    await saved(`${app}-image.json`, inspection);
    requireThat(inspection.length === 1 && inspection[0].Architecture === 'amd64' && inspection[0].Os === 'linux' && inspection[0].Config?.Labels?.['org.opencontainers.image.revision'] === sha, 'Published image architecture/source label does not match the verified source');
````

<a id="source-q12"></a>
## Q12 · `backend/src/operations/database-bootstrap.ts`

**Scope:** Current source. **Symbol/setting:** `export async function bootstrapDatabases`. **Lines at inspection:** 7–16.
**File SHA-256 at inspection:** `044d5978d1e9fc6e6553e5971f9c509d6a94c1ff6bf57f1ffbbe87e293cb7fe2`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/backend/src/operations/database-bootstrap.ts#L7-L16)

````typescript
const literal = (value: string) => `'${value.replaceAll("'", "''")}'`;
export async function bootstrapDatabases(client?: Client): Promise<void> {
  // Standalone one-shot task only. Normal capabilities never receive administrator credentials.
  const options = databaseOptions();
  if (!options.ssl) throw new Error('Database bootstrap requires verified TLS');
  const passwords = Object.fromEntries(
    SERVICES.map((service) => [service, required(`${service.toUpperCase()}_DB_PASSWORD`)]),
  );
  for (const password of Object.values(passwords)) {
    if (password.length < 32 || password.includes('\0'))
````

<a id="source-q13"></a>
## Q13 · `backend/src/common/connections.ts`

**Scope:** Current source. **Symbol/setting:** `export function databaseOptions`. **Lines at inspection:** 11–20.
**File SHA-256 at inspection:** `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/backend/src/common/connections.ts#L11-L20)

````typescript
}
export function databaseOptions(): PoolConfig {
  const sslEnabled = enabled('DB_SSL');
  let connection: PoolConfig;
  if (process.env.DB_URL) {
    const url = new URL(process.env.DB_URL);
    if (!['postgres:', 'postgresql:'].includes(url.protocol))
      throw new Error('DB_URL must be PostgreSQL');
    // pg connection-string ssl parameters override the explicit TLS object.
    if ([...url.searchParams.keys()].some((key) => key.toLowerCase().startsWith('ssl')))
````

<a id="source-q14"></a>
## Q14 · `backend/src/common/messaging.ts`

**Scope:** Current source. **Symbol/setting:** `export class OutboxPublisher`. **Lines at inspection:** 13–22.
**File SHA-256 at inspection:** `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/backend/src/common/messaging.ts#L13-L22)

````typescript
@Injectable()
export class OutboxPublisher implements OnApplicationBootstrap, OnModuleDestroy {
  private readonly logger = new Logger('OutboxPublisher');
  private producer?: Producer;
  private stopping = false;
  constructor(
    private readonly db: Database,
    private readonly health: WorkerHealth,
  ) {}
  onApplicationBootstrap(): void {
````

<a id="source-q15"></a>
## Q15 · `infra/aws-ecs-dev/compute.tf`

**Scope:** Current source. **Symbol/setting:** `delete_on_termination = true`. **Lines at inspection:** 52–61.
**File SHA-256 at inspection:** `5a3c8e35c1077e7e00753cc264874de2a42cfa6dd87bdb5bfd12ceb34ce2e8d2`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/compute.tf#L52-L61)

````hcl
    encrypted             = true
    delete_on_termination = true
    tags                  = { ExpiresAt = var.expires_at }
  }
  user_data = templatefile("${path.module}/kafka-user-data.sh.tftpl", {
    aws_region        = var.region
    broker_secret_arn = aws_secretsmanager_secret.runtime["broker"].arn
    broker_dns        = "kafka.${local.namespace}"
    kafka_image       = var.kafka_image
    log_group         = aws_cloudwatch_log_group.broker.name
````

<a id="source-q16"></a>
## Q16 · `backend/src/common/health.ts`

**Scope:** Current source. **Symbol/setting:** `@Get('health/serve')`. **Lines at inspection:** 17–26.
**File SHA-256 at inspection:** `2941f0c699974fd0f6e27c82200cd617693eae335afdd4710066eb3fadf4c5b8`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/backend/src/common/health.ts#L17-L26)

````typescript
  // Routing readiness preserves durable inquiry writes while Kafka retries asynchronously.
  @Get('health/serve') async serving() {
    try {
      await this.db.query('SELECT 1');
    } catch {
      throw new ServiceUnavailableException('Database dependency unavailable');
    }
    return { status: 'UP', service: serviceName(), database: 'UP' };
  }
  @Get(['health/ready', 'health', 'actuator/health', 'actuator/health/readiness']) async ready() {
````

<a id="source-q17"></a>
## Q17 · `docs/aws-micro-completion-execution-2026-10-30.md`

**Scope:** Dated execution: 2026-10-30. **Symbol/setting:** `The marketplace application is not activated`. **Lines at inspection:** 8–17.
**File SHA-256 at inspection:** `25153505affa28065857062fcc7c40359bc9d7700e50ad05543a6b69c5c7a6df`.

The original was untracked at inspection. [Preserved full dated record](questionnaire-records/aws-micro-completion-execution-2026-10-30.md) has the file SHA-256 above; no current cloud check is asserted.

````text

**The marketplace application is not activated:** no ECS services or running/pending tasks. Database SQL/TLS client testing, schema bootstrap, recovery/restore and marketplace acceptance are separate runtime gates. The alarms have no notification destination or delivery proof; current alarm states are {'INSUFFICIENT_DATA': 7}. Alarm existence alone is not a health/notification success claim. Exact-source hosted release verification and successful amd64 image builds/scans/publication are still required. The earlier Docker Hub metadata stall and missing hosted SonarCloud configuration remain accurately recorded; no gates were waived.

The shutdown deadline remains **today, October 30, 2026, 9:51:25 PM EDT** (`2026-10-31T01:51:25.219221Z`). Original start is unchanged. **Begin operator-assisted cleanup review by 7:51 PM EDT.** There is no automatic cleanup or reminder. Real current protection-transition and destroy artifacts need their own approval; state and the existing certificate must be preserved. This apply did not authorize or perform cleanup.

## Commands and actual outcomes

Working directory: `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/infra/aws-ecs-dev`. Profile `marketplace-dev`, Ohio `us-east-2`; conflicting credential and Terraform overrides cleared. All raw state, plan/API receipts and diagnostics remain owner-only under ignored `work/`.

| Command | Purpose | Actual exit |
````

<a id="source-q18"></a>
## Q18 · `docs/aws-reversible-compute-stop-2026-10-31.md`

**Scope:** Dated execution: 2026-10-31. **Symbol/setting:** `This is not full teardown`. **Lines at inspection:** 11–20.
**File SHA-256 at inspection:** `ac37677f9448b1d5737b19d8a88c41e041aa1d799405d1ca8b879fb48ab07625`.

The original was untracked at inspection. [Preserved full dated record](questionnaire-records/aws-reversible-compute-stop-2026-10-31.md) has the file SHA-256 above; no current cloud check is asserted.

````text

**This is not full teardown or zero ongoing cost.** ALB, NAT gateway/EIP, EBS and RDS storage/backups, secrets, logs/S3/discovery and retained state remain allocated and may incur charges. Only the two compute operating states changed. Historical AWS billing/metric data may lag.

AWS automatically restarts RDS after seven consecutive stopped days. AWS currently reports an automatic restart at **November 07, 2026, 07:22 AM EST**; UTC value: `2026-11-07T12:22:07.316000+00:00`. [AWS documents the retained storage charges and restart behavior](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html). No new scheduler, reminder or cleanup controller was created.

The previously approved cleanup-transition settings remain in place: RDS deletion protection is off, future snapshot/backup discard flags are set, operations force_destroy is enabled and six runtime-secret recovery windows are0. This reversible stop does not execute any of those deletion settings. The earlier broad destroy remains blocked by automatic approval review; it was not retried or split into delete batches, and no alternate execution route was used.

## Actual commands

Working directory: `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws`. Runtime profile marketplace-dev, Ohio/us-east-2; conflicting credential/Terraform overrides cleared by the established helper. Raw API responses/approval/steps remain owner-only under ignored `work/aws-reversible-compute-stop-2026-10-31/`.
````

<a id="source-q19"></a>
## Q19 · `infra/aws-ecs-dev/network.tf`

**Scope:** Current source. **Symbol/setting:** `depends_on        = [aws_internet_gateway.dev]`. **Lines at inspection:** 61–70.
**File SHA-256 at inspection:** `245073d06aac72e825494ef35a0db762e347162ea28bf3ae964528da04677873`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/network.tf#L61-L70)

````hcl
  subnet_id         = aws_subnet.public[0].id
  depends_on        = [aws_internet_gateway.dev]
  tags              = { Name = "${local.name}-zonal-nat" }
}
resource "aws_route_table" "private_active" {
  vpc_id = aws_vpc.dev.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.dev.id
  }
````

<a id="source-q20"></a>
## Q20 · `infra/aws-ecs-dev/versions.tf`

**Scope:** Current source. **Symbol/setting:** `required_providers`. **Lines at inspection:** 2–11.
**File SHA-256 at inspection:** `7e17ae4bc5f302ec96a74c7f0427aba6e91c3299033d3789f30917a5fc61ea51`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/versions.tf#L2-L11)

````hcl
  required_version = ">= 1.10, < 2.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
  backend "s3" {}
}
provider "aws" {
  region = var.region
  default_tags {
    tags = { Project = var.project, Environment = "ecs-dev", ManagedBy = "Terraform", Owner = var.owner, ExpiresAt = var.expires_at }
````

<a id="source-q21"></a>
## Q21 · `infra/aws-ecs-dev/compute.tf`

**Scope:** Current source. **Symbol/setting:** `active_services =`. **Lines at inspection:** 89–98.
**File SHA-256 at inspection:** `5a3c8e35c1077e7e00753cc264874de2a42cfa6dd87bdb5bfd12ceb34ce2e8d2`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/compute.tf#L89-L98)

````hcl
locals {
  active_services = var.image_digests == null || !local.https_configured ? {} : local.services
  app_containers = { for service, port in local.active_services : service => {
    name                   = service
    image                  = "${aws_ecr_repository.app[service == "frontend" ? "frontend" : "backend"].repository_url}@${service == "frontend" ? var.image_digests.frontend : var.image_digests.backend}"
    essential              = true
    readonlyRootFilesystem = service != "frontend"
    user                   = service == "frontend" ? "101" : "1000"
    stopTimeout            = 60
    linuxParameters        = { initProcessEnabled = true, capabilities = { drop = ["ALL"] } }
````

<a id="source-q22"></a>
## Q22 · `infra/aws-ecs-dev/network.tf`

**Scope:** Current source. **Symbol/setting:** `services         =`. **Lines at inspection:** 16–25.
**File SHA-256 at inspection:** `245073d06aac72e825494ef35a0db762e347162ea28bf3ae964528da04677873`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/network.tf#L16-L25)

````hcl
  capabilities     = { identity = 8181, catalog = 8182, inquiries = 8183, notifications = 8184 }
  services         = merge(local.capabilities, { frontend = 8180 })
  brokers_clients  = toset(["inquiries", "notifications"])
  secret_names     = toset(concat(keys(local.capabilities), ["shared", "broker"]))
  arn_prefix       = "arn:${data.aws_partition.current.partition}"
}
resource "aws_vpc" "dev" {
  cidr_block           = "10.85.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
````

<a id="source-q23"></a>
## Q23 · `infra/aws-ecs-dev/backend.hcl.example`

**Scope:** Current source. **Symbol/setting:** `key =`. **Lines at inspection:** 1–5.
**File SHA-256 at inspection:** `3fa72f7b81bf2e7deb3710625587c5f978f2c7cc5e5f122dd97a77ae95917a7c`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/backend.hcl.example#L1-L5)

````hcl
bucket = "REPLACE_WITH_APPROVED_PRIVATE_STATE_BUCKET"
key = "linked-in-node/ecs-dev/terraform.tfstate"
region = "us-east-2"
encrypt = true
use_lockfile = true
````

<a id="source-q24"></a>
## Q24 · `infra/aws-ecs-dev/backend.hcl.example`

**Scope:** Current source. **Symbol/setting:** `use_lockfile = true`. **Lines at inspection:** 4–5.
**File SHA-256 at inspection:** `3fa72f7b81bf2e7deb3710625587c5f978f2c7cc5e5f122dd97a77ae95917a7c`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/backend.hcl.example#L4-L5)

````hcl
encrypt = true
use_lockfile = true
````

<a id="source-q25"></a>
## Q25 · `scripts/aws-ecs-review-plan.py`

**Scope:** Current source. **Symbol/setting:** `Saved plan source differs:`. **Lines at inspection:** 171–180.
**File SHA-256 at inspection:** `f2e29ce7dc6e053774f758c0cb6944ac8e8129aada4fea3b2e454a8dccf92518`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/scripts/aws-ecs-review-plan.py#L171-L180)

````text
        for name, path in expected.items():
            assert saved.read(name) == path.read_bytes(), f'Saved plan source differs: {path.name}'
        assert saved.read('.terraform.lock.hcl') == (ROOT/'infra/aws-ecs-dev/.terraform.lock.hcl').read_bytes(), 'Saved provider lock differs'
        saved_tf = {n for n in saved.namelist() if n.startswith('tfconfig/m-/') and n.endswith('.tf')}
        if s3_backend_context is None:
            assert saved_tf == set(expected) | {'tfconfig/m-/backend_override.tf'}, 'Unexpected saved Terraform configuration'
            assert ''.join(saved.read('tfconfig/m-/backend_override.tf').decode().split()) == 'terraform{backend"local"{}}', 'Preview must use local backend only'
        else:
            assert len(saved.namelist()) == len(set(saved.namelist())), 'Duplicate saved ZIP members are forbidden'
            saved_config = {name for name in saved.namelist() if name.startswith('tfconfig/')}
````

<a id="source-q26"></a>
## Q26 · `docs/aws-micro-completion-execution-2026-10-30.md`

**Scope:** Dated execution: 2026-10-30. **Symbol/setting:** `All 104 existing resource identities are preserved`. **Lines at inspection:** 2–11.
**File SHA-256 at inspection:** `25153505affa28065857062fcc7c40359bc9d7700e50ad05543a6b69c5c7a6df`.

The original was untracked at inspection. [Preserved full dated record](questionnaire-records/aws-micro-completion-execution-2026-10-30.md) has the file SHA-256 above; no current cloud check is asserted.

````text

The human-approved plan `cb438bc065c4` **completed successfully**, Terraform exit **0**, with **8 creates**. All 104 existing resource identities are preserved. Actual protected application state now contains **112 managed resources, serial 8, no taints**. A fresh full Terraform plan reports **no changes**.

Live read-back verifies an **available `db.t4g.micro` PostgreSQL instance**, private access, encrypted storage, **one-day automated backup retention**, deletion protection, active RDS-managed master-secret metadata and `rds.force_ssl=1`. No secret values were retrieved. All **seven alarms** match their approved thresholds, dimensions and evaluation settings. The broker disk's actual expiry tag still matches the approved deadline. The account remains **Free/ACTIVE**.

The prior approved repair's ALB, certificate verification, correct-host empty-target503/wrong-host403, logging test and actual access-log delivery, broker registration/private DNS and explicit custom-health controls remain preserved. They were verified in the preceding execution; the current full no-change plan and 104 identity checks detect unintended changes.

**The marketplace application is not activated:** no ECS services or running/pending tasks. Database SQL/TLS client testing, schema bootstrap, recovery/restore and marketplace acceptance are separate runtime gates. The alarms have no notification destination or delivery proof; current alarm states are {'INSUFFICIENT_DATA': 7}. Alarm existence alone is not a health/notification success claim. Exact-source hosted release verification and successful amd64 image builds/scans/publication are still required. The earlier Docker Hub metadata stall and missing hosted SonarCloud configuration remain accurately recorded; no gates were waived.

The shutdown deadline remains **today, October 30, 2026, 9:51:25 PM EDT** (`2026-10-31T01:51:25.219221Z`). Original start is unchanged. **Begin operator-assisted cleanup review by 7:51 PM EDT.** There is no automatic cleanup or reminder. Real current protection-transition and destroy artifacts need their own approval; state and the existing certificate must be preserved. This apply did not authorize or perform cleanup.
````

<a id="source-q27"></a>
## Q27 · `docs/nodejs-aws-study-path/labs/terraform-advanced/run.py`

**Scope:** Local/mock check definition; not a new execution. **Symbol/setting:** `child.write_text(`. **Lines at inspection:** 78–87.
**File SHA-256 at inspection:** `31f448c8cf7c0ec389f9b17ec38b3b37532c412022d41b2e4c9dbb2c10bc71a7`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/docs/nodejs-aws-study-path/labs/terraform-advanced/run.py#L78-L87)

````python
        child = root / 'modules' / 'service' / 'main.tf'
        child.write_text(child.read_text().replace('"terraform_data" "record"', '"terraform_data" "entry"').replace('terraform_data.record.', 'terraform_data.entry.') + '\nmoved {\n  from = terraform_data.record\n  to   = terraform_data.entry\n}\n')
        tf('fmt', '-recursive')
        tf('validate', '-no-color')
        tf('plan', '-input=false', '-no-color', '-detailed-exitcode', '-out=move.tfplan', expected=2)
        moved = tf('show', '-json', 'move.tfplan', capture_json=True)
        require(len(moved['resource_changes']) == 3 and all(c['change']['actions'] == ['no-op'] and c.get('previous_address', '').endswith('.terraform_data.record') for c in moved['resource_changes']), 'child moved block maps all three instances without replacement')
        tf('apply', '-input=false', '-no-color', 'move.tfplan')
        moved_outputs = tf('output', '-json', capture_json=True)
        require(moved_outputs['identities']['value'] == after['identities']['value'], 'every ID survives the child-module address migration')
````

<a id="source-q28"></a>
## Q28 · `infra/aws-ecs-dev/data.tf`

**Scope:** Current source. **Symbol/setting:** `manage_master_user_password     = true`. **Lines at inspection:** 44–53.
**File SHA-256 at inspection:** `283d1868e232dfb676e5264b1707b1f70a1b33f48c2ea054a1be88156a8b9e7f`.

This file differs from HEAD or is untracked: inspect the real local file; no published-source link is asserted.

````hcl
  username                        = "marketplace_admin"
  manage_master_user_password     = true
  db_name                         = "postgres"
  db_subnet_group_name            = aws_db_subnet_group.dev.name
  parameter_group_name            = aws_db_parameter_group.dev.name
  vpc_security_group_ids          = [aws_security_group.database.id]
  availability_zone               = local.azs[0]
  publicly_accessible             = false
  multi_az                        = false
  port                            = 5432
````

<a id="source-q29"></a>
## Q29 · `infra/aws-ecs-dev/tests/security.tftest.hcl`

**Scope:** Local/mock check definition; not a new execution. **Symbol/setting:** `run "infrastructure_without_unpublished_images"`. **Lines at inspection:** 51–60.
**File SHA-256 at inspection:** `ec9ff5a8889ee81068e46cb2e021a34abf7b1e828c6cc309ff933aa5472563c2`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/tests/security.tftest.hcl#L51-L60)

````hcl
}
run "infrastructure_without_unpublished_images" {
  command = apply
  assert {
    condition     = length(aws_ecs_service.app) == 0 && length(aws_ecs_task_definition.app) == 0 && length(aws_ecs_task_definition.bootstrap) == 0
    error_message = "An infrastructure-only plan must not invent images or start application tasks."
  }
  assert {
    condition     = length(aws_subnet.public) == 2 && length(aws_subnet.private) == 2 && aws_subnet.public[0].availability_zone != aws_subnet.public[1].availability_zone && aws_nat_gateway.dev.subnet_id == aws_subnet.public[0].id && aws_nat_gateway.dev.availability_mode == "zonal"
    error_message = "ALB requires two AZs; the selected lab uses exactly one zonal NAT in active AZ."
````

<a id="source-q30"></a>
## Q30 · `infra/aws-ecs-dev/compute.tf`

**Scope:** Current source. **Symbol/setting:** `resource "aws_ecs_service" "app"`. **Lines at inspection:** 149–158.
**File SHA-256 at inspection:** `5a3c8e35c1077e7e00753cc264874de2a42cfa6dd87bdb5bfd12ceb34ce2e8d2`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/compute.tf#L149-L158)

````hcl
}
resource "aws_ecs_service" "app" {
  for_each                           = local.active_services
  name                               = each.key
  cluster                            = aws_ecs_cluster.dev.id
  task_definition                    = aws_ecs_task_definition.app[each.key].arn
  desired_count                      = var.deploy_application ? 1 : 0
  launch_type                        = "FARGATE"
  platform_version                   = "1.4.0"
  enable_execute_command             = false
````

<a id="source-i01"></a>
## I01 · `scripts/aws-ecs-publish-local.mjs`

**Scope:** Current source; rehearsal scenario. **Symbol/setting:** `'--platform', 'linux/amd64'`. **Lines at inspection:** 106–115.
**File SHA-256 at inspection:** `93323c162fd871b1e030d19a476eee663964b5ab32ccd47d0723d420991441f1`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/scripts/aws-ecs-publish-local.mjs#L106-L115)

````text
      cleanSource(sha);
      execute('docker', ['buildx', 'build', '--platform', 'linux/amd64', '--label', `org.opencontainers.image.revision=${sha}`, '--push', '--tag', `${repo}:${sha}`, '--metadata-file', join(evidence, `${app}-build.json`), join(source, app)]);
      digest = getDigest();
    }
    requireThat(/^sha256:[a-f0-9]{64}$/.test(digest || ''), 'ECR did not return a valid immutable image digest');
    const image = `${repo}@${digest}`;
    execute('docker', ['pull', '--platform', 'linux/amd64', image]);
    const inspection = json('docker', ['image', 'inspect', image]);
    await saved(`${app}-image.json`, inspection);
    requireThat(inspection.length === 1 && inspection[0].Architecture === 'amd64' && inspection[0].Os === 'linux' && inspection[0].Config?.Labels?.['org.opencontainers.image.revision'] === sha, 'Published image architecture/source label does not match the verified source');
````

<a id="source-i02"></a>
## I02 · `infra/aws-ecs-dev/iam.tf`

**Scope:** Current source; rehearsal scenario. **Symbol/setting:** `resource "aws_iam_role_policy" "execution"`. **Lines at inspection:** 17–26.
**File SHA-256 at inspection:** `31d3823907c0c627f5d6d0c4af20c2d6bb7c4a7d552ee0182c704bb47babc704`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/iam.tf#L17-L26)

````hcl
}
resource "aws_iam_role_policy" "execution" {
  for_each = local.execution_names
  role     = aws_iam_role.execution[each.key].id
  policy = jsonencode({ Version = "2012-10-17", Statement = concat([
    { Sid = "RegistryAuthentication", Effect = "Allow", Action = ["ecr:GetAuthorizationToken"], Resource = "*" },
    { Sid = "ReadOwnedImage", Effect = "Allow", Action = ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer", "ecr:BatchCheckLayerAvailability"], Resource = aws_ecr_repository.app[each.key == "frontend" ? "frontend" : "backend"].arn },
    { Sid = "WriteOwnedLogs", Effect = "Allow", Action = ["logs:CreateLogStream", "logs:PutLogEvents"], Resource = "${aws_cloudwatch_log_group.task[each.key].arn}:*" }
  ], length(local.execution_secrets[each.key]) == 0 ? [] : [{ Sid = "ReadOwnedConfiguration", Effect = "Allow", Action = ["secretsmanager:GetSecretValue"], Resource = local.execution_secrets[each.key] }]) })
}
````

<a id="source-i03"></a>
## I03 · `backend/src/common/health.ts`

**Scope:** Current source; rehearsal scenario. **Symbol/setting:** `@Get('health/serve')`. **Lines at inspection:** 17–26.
**File SHA-256 at inspection:** `2941f0c699974fd0f6e27c82200cd617693eae335afdd4710066eb3fadf4c5b8`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/backend/src/common/health.ts#L17-L26)

````typescript
  // Routing readiness preserves durable inquiry writes while Kafka retries asynchronously.
  @Get('health/serve') async serving() {
    try {
      await this.db.query('SELECT 1');
    } catch {
      throw new ServiceUnavailableException('Database dependency unavailable');
    }
    return { status: 'UP', service: serviceName(), database: 'UP' };
  }
  @Get(['health/ready', 'health', 'actuator/health', 'actuator/health/readiness']) async ready() {
````

<a id="source-i04"></a>
## I04 · `infra/aws-ecs-dev/network.tf`

**Scope:** Current source; rehearsal scenario. **Symbol/setting:** `resource "aws_vpc_endpoint" "s3"`. **Lines at inspection:** 81–90.
**File SHA-256 at inspection:** `245073d06aac72e825494ef35a0db762e347162ea28bf3ae964528da04677873`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/network.tf#L81-L90)

````hcl
}
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.dev.id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private_active.id, aws_route_table.private_standby.id]
  # ECR layers and AL2023 package repositories use regional AWS-owned S3 buckets.
  # The gateway route also intercepts package downloads, so NAT cannot repair a denied endpoint policy.
  policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = "*", Action = ["s3:GetObject"], Resource = ["${local.arn_prefix}:s3:::prod-${var.region}-starport-layer-bucket/*", "${local.arn_prefix}:s3:::al2023-repos-${var.region}-de612dc2/*"] }] })
}
````

<a id="source-i05"></a>
## I05 · `backend/src/common/connections.ts`

**Scope:** Current source; rehearsal scenario. **Symbol/setting:** `export function databaseOptions`. **Lines at inspection:** 11–20.
**File SHA-256 at inspection:** `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/backend/src/common/connections.ts#L11-L20)

````typescript
}
export function databaseOptions(): PoolConfig {
  const sslEnabled = enabled('DB_SSL');
  let connection: PoolConfig;
  if (process.env.DB_URL) {
    const url = new URL(process.env.DB_URL);
    if (!['postgres:', 'postgresql:'].includes(url.protocol))
      throw new Error('DB_URL must be PostgreSQL');
    // pg connection-string ssl parameters override the explicit TLS object.
    if ([...url.searchParams.keys()].some((key) => key.toLowerCase().startsWith('ssl')))
````

<a id="source-i06"></a>
## I06 · `backend/src/common/connections.ts`

**Scope:** Current source; rehearsal scenario. **Symbol/setting:** `export function kafkaOptions`. **Lines at inspection:** 47–56.
**File SHA-256 at inspection:** `00d0ac41cb814d758ca49ed9d0ca67df6c1caf84bab90ddd02eae1274d0ec4cf`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/backend/src/common/connections.ts#L47-L56)

````typescript
}
export function kafkaOptions(): KafkaConfig {
  const sslEnabled = enabled('KAFKA_SSL');
  const ca = process.env.KAFKA_SSL_CA;
  const mechanism = process.env.KAFKA_SASL_MECHANISM;
  if (ca && !sslEnabled) throw new Error('KAFKA_SSL_CA requires KAFKA_SSL=true');
  if (mechanism && mechanism !== 'scram-sha-512')
    throw new Error('KAFKA_SASL_MECHANISM must be scram-sha-512');
  if ((mechanism || process.env.KAFKA_USERNAME || process.env.KAFKA_PASSWORD) && !sslEnabled)
    throw new Error('Kafka credentials require verified TLS');
````

<a id="source-i07"></a>
## I07 · `infra/aws-ecs-certificate/main.tf`

**Scope:** Current source; rehearsal scenario. **Symbol/setting:** `resource "aws_acm_certificate" "application"`. **Lines at inspection:** 19–28.
**File SHA-256 at inspection:** `26bebdbcb98c3c211c257fb8d5188a2413c5a209382db0ab0502ba50121a251c`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-certificate/main.tf#L19-L28)

````hcl
}
resource "aws_acm_certificate" "application" {
  domain_name       = var.application_hostname
  validation_method = "DNS"
  key_algorithm     = "RSA_2048"
  options {
    certificate_transparency_logging_preference = "ENABLED"
    export                                      = "DISABLED"
  }
  lifecycle { create_before_destroy = true }
````

<a id="source-i08"></a>
## I08 · `backend/src/common/messaging.ts`

**Scope:** Current source; rehearsal scenario. **Symbol/setting:** `export class OutboxPublisher`. **Lines at inspection:** 13–22.
**File SHA-256 at inspection:** `ad4c562971987d7ec8dfb8d733074cbd95eedce362cff87b4abe32c6350d7237`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/backend/src/common/messaging.ts#L13-L22)

````typescript
@Injectable()
export class OutboxPublisher implements OnApplicationBootstrap, OnModuleDestroy {
  private readonly logger = new Logger('OutboxPublisher');
  private producer?: Producer;
  private stopping = false;
  constructor(
    private readonly db: Database,
    private readonly health: WorkerHealth,
  ) {}
  onApplicationBootstrap(): void {
````

<a id="source-i09"></a>
## I09 · `infra/aws-ecs-dev/backend.hcl.example`

**Scope:** Current source; rehearsal scenario. **Symbol/setting:** `use_lockfile = true`. **Lines at inspection:** 4–5.
**File SHA-256 at inspection:** `3fa72f7b81bf2e7deb3710625587c5f978f2c7cc5e5f122dd97a77ae95917a7c`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/backend.hcl.example#L4-L5)

````hcl
encrypt = true
use_lockfile = true
````

<a id="source-i10"></a>
## I10 · `docs/aws-micro-completion-execution-2026-10-30.md`

**Scope:** Dated execution: 2026-10-30; recovery rehearsal based on recorded partial failures. **Symbol/setting:** `fresh full Terraform plan reports`. **Lines at inspection:** 2–11.
**File SHA-256 at inspection:** `25153505affa28065857062fcc7c40359bc9d7700e50ad05543a6b69c5c7a6df`.

The original was untracked at inspection. [Preserved full dated record](questionnaire-records/aws-micro-completion-execution-2026-10-30.md) has the file SHA-256 above; no current cloud check is asserted.

````text

The human-approved plan `cb438bc065c4` **completed successfully**, Terraform exit **0**, with **8 creates**. All 104 existing resource identities are preserved. Actual protected application state now contains **112 managed resources, serial 8, no taints**. A fresh full Terraform plan reports **no changes**.

Live read-back verifies an **available `db.t4g.micro` PostgreSQL instance**, private access, encrypted storage, **one-day automated backup retention**, deletion protection, active RDS-managed master-secret metadata and `rds.force_ssl=1`. No secret values were retrieved. All **seven alarms** match their approved thresholds, dimensions and evaluation settings. The broker disk's actual expiry tag still matches the approved deadline. The account remains **Free/ACTIVE**.

The prior approved repair's ALB, certificate verification, correct-host empty-target503/wrong-host403, logging test and actual access-log delivery, broker registration/private DNS and explicit custom-health controls remain preserved. They were verified in the preceding execution; the current full no-change plan and 104 identity checks detect unintended changes.

**The marketplace application is not activated:** no ECS services or running/pending tasks. Database SQL/TLS client testing, schema bootstrap, recovery/restore and marketplace acceptance are separate runtime gates. The alarms have no notification destination or delivery proof; current alarm states are {'INSUFFICIENT_DATA': 7}. Alarm existence alone is not a health/notification success claim. Exact-source hosted release verification and successful amd64 image builds/scans/publication are still required. The earlier Docker Hub metadata stall and missing hosted SonarCloud configuration remain accurately recorded; no gates were waived.

The shutdown deadline remains **today, October 30, 2026, 9:51:25 PM EDT** (`2026-10-31T01:51:25.219221Z`). Original start is unchanged. **Begin operator-assisted cleanup review by 7:51 PM EDT.** There is no automatic cleanup or reminder. Real current protection-transition and destroy artifacts need their own approval; state and the existing certificate must be preserved. This apply did not authorize or perform cleanup.
````

<a id="source-i11"></a>
## I11 · `infra/aws-ecs-dev/compute.tf`

**Scope:** Current source; rehearsal scenario. **Symbol/setting:** `deployment_circuit_breaker`. **Lines at inspection:** 161–170.
**File SHA-256 at inspection:** `5a3c8e35c1077e7e00753cc264874de2a42cfa6dd87bdb5bfd12ceb34ce2e8d2`.

[Exact committed source](https://github.com/robertovalencia/linked-in-node-and-aws/blob/7e778a01d6be739feafda36e17df8d42095f79f1/infra/aws-ecs-dev/compute.tf#L161-L170)

````hcl
  health_check_grace_period_seconds  = each.key == "frontend" ? 60 : null
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  network_configuration {
    subnets          = [aws_subnet.private[0].id]
    security_groups  = [aws_security_group.service[each.key].id]
    assign_public_ip = false
  }
````

<a id="source-i12"></a>
## I12 · `docs/aws-reversible-compute-stop-2026-10-31.md`

**Scope:** Dated execution: 2026-10-31; retained-cost diagnosis rehearsal. **Symbol/setting:** `previously approved cleanup-transition settings remain`. **Lines at inspection:** 15–24.
**File SHA-256 at inspection:** `ac37677f9448b1d5737b19d8a88c41e041aa1d799405d1ca8b879fb48ab07625`.

The original was untracked at inspection. [Preserved full dated record](questionnaire-records/aws-reversible-compute-stop-2026-10-31.md) has the file SHA-256 above; no current cloud check is asserted.

````text

The previously approved cleanup-transition settings remain in place: RDS deletion protection is off, future snapshot/backup discard flags are set, operations force_destroy is enabled and six runtime-secret recovery windows are0. This reversible stop does not execute any of those deletion settings. The earlier broad destroy remains blocked by automatic approval review; it was not retried or split into delete batches, and no alternate execution route was used.

## Actual commands

Working directory: `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws`. Runtime profile marketplace-dev, Ohio/us-east-2; conflicting credential/Terraform overrides cleared by the established helper. Raw API responses/approval/steps remain owner-only under ignored `work/aws-reversible-compute-stop-2026-10-31/`.

| Command | Actual exit |
|---|---:|
| `aws sts get-caller-identity --region us-east-2 --output json` | 0 |
````
