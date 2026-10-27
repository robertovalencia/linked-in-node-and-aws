# All providers are mocked. The apply command below only evaluates local mock resources; it never contacts AWS.
mock_provider "aws" {
  mock_data "aws_partition" { defaults = { partition = "aws" } }
  mock_data "aws_caller_identity" { defaults = { account_id = "123456789012" } }
  mock_data "aws_ssm_parameter" { defaults = { value = "ami-0123456789abcdef0" } }
  mock_data "aws_availability_zones" { defaults = { names = ["us-east-2b", "us-east-2a", "us-east-2c"] } }
  mock_resource "aws_ecr_repository" { defaults = { arn = "arn:aws:ecr:us-east-2:123456789012:repository/mock", repository_url = "123456789012.dkr.ecr.us-east-2.amazonaws.com/mock" } }
  mock_resource "aws_iam_role" { defaults = { arn = "arn:aws:iam::123456789012:role/mock" } }
  mock_resource "aws_db_instance" { defaults = { address = "mock.rds.amazonaws.com", master_user_secret = [{ secret_arn = "arn:aws:secretsmanager:us-east-2:123456789012:secret:master-abcdef", secret_status = "active", kms_key_id = "arn:aws:kms:us-east-2:123456789012:key/00000000-0000-0000-0000-000000000000" }] } }
  mock_resource "aws_cloudwatch_log_group" { defaults = { arn = "arn:aws:logs:us-east-2:123456789012:log-group:mock" } }
  mock_resource "aws_ecs_cluster" { defaults = { id = "arn:aws:ecs:us-east-2:123456789012:cluster/mock" } }
  mock_resource "aws_ecs_task_definition" { defaults = { arn = "arn:aws:ecs:us-east-2:123456789012:task-definition/mock:1" } }
  mock_resource "aws_service_discovery_service" { defaults = { arn = "arn:aws:servicediscovery:us-east-2:123456789012:service/srv-mock" } }
  mock_resource "aws_lb_target_group" { defaults = { arn = "arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/mock/0000000000000000" } }
  mock_resource "aws_lb_listener" { defaults = { arn = "arn:aws:elasticloadbalancing:us-east-2:123456789012:listener/app/mock/0000000000000000/0000000000000000" } }
  mock_resource "aws_lb" { defaults = { arn = "arn:aws:elasticloadbalancing:us-east-2:123456789012:loadbalancer/app/mock/0000000000000000" } }
  mock_resource "aws_s3_bucket" { defaults = { arn = "arn:aws:s3:::mock-operations-bucket" } }
}
override_resource {
  target = aws_secretsmanager_secret.runtime["identity"]
  values = { arn = "arn:aws:secretsmanager:us-east-2:123456789012:secret:identity-abcdef" }
}
override_resource {
  target = aws_secretsmanager_secret.runtime["catalog"]
  values = { arn = "arn:aws:secretsmanager:us-east-2:123456789012:secret:catalog-abcdef" }
}
override_resource {
  target = aws_secretsmanager_secret.runtime["inquiries"]
  values = { arn = "arn:aws:secretsmanager:us-east-2:123456789012:secret:inquiries-abcdef" }
}
override_resource {
  target = aws_secretsmanager_secret.runtime["notifications"]
  values = { arn = "arn:aws:secretsmanager:us-east-2:123456789012:secret:notifications-abcdef" }
}
override_resource {
  target = aws_secretsmanager_secret.runtime["shared"]
  values = { arn = "arn:aws:secretsmanager:us-east-2:123456789012:secret:shared-abcdef" }
}
override_resource {
  target = aws_secretsmanager_secret.runtime["broker"]
  values = { arn = "arn:aws:secretsmanager:us-east-2:123456789012:secret:broker-abcdef" }
}
variables {
  owner                    = "mock-reviewer"
  expires_at               = "2026-10-29T18:00:00Z"
  approved_client_cidrs    = ["192.0.2.1/32"]
  application_hostname     = "marketplace.example.invalid"
  certificate_arn          = "arn:aws:acm:us-east-2:123456789012:certificate/00000000-0000-0000-0000-000000000000"
  kafka_image              = "apache/kafka:4.0.1@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  recovery_snapshot_suffix = "mock-review"
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
  }
  assert {
    condition     = !aws_instance.broker.associate_public_ip_address && !aws_db_instance.dev.publicly_accessible && !aws_db_instance.dev.multi_az
    error_message = "The single-AZ database and broker must remain private."
  }
  assert {
    condition     = aws_db_instance.dev.storage_encrypted && aws_db_instance.dev.manage_master_user_password && aws_db_instance.dev.deletion_protection && !aws_db_instance.dev.skip_final_snapshot && !aws_db_instance.dev.delete_automated_backups
    error_message = "RDS must manage admin credentials, encrypt storage and require explicit recovery/teardown review."
  }
  assert {
    condition     = length(aws_secretsmanager_secret.runtime) == 6 && output.cost_quantities.rds_managed_master_secrets == 1
    error_message = "Price six owned/runtime/broker secret resources plus the RDS-managed master secret."
  }
  assert {
    condition     = contains(jsondecode(aws_vpc_endpoint.s3.policy).Statement[0].Resource, "arn:aws:s3:::al2023-repos-us-east-2-de612dc2/*") && contains(jsondecode(aws_vpc_endpoint.s3.policy).Statement[0].Resource, "arn:aws:s3:::prod-us-east-2-starport-layer-bucket/*")
    error_message = "Gateway policy must permit both ECR layers and AL2023 bootstrap package downloads."
  }
  assert {
    condition     = alltrue([for p in aws_db_parameter_group.dev.parameter : p.name != "rds.force_ssl" || p.value == "1"])
    error_message = "Database connections must require TLS."
  }
  assert {
    condition     = anytrue([for p in aws_db_parameter_group.dev.parameter : p.name == "log_min_error_statement" && p.value == "panic"])
    error_message = "Password-bearing bootstrap SQL must not be logged on failure."
  }
  assert {
    condition     = length(aws_cloudwatch_metric_alarm.dev) == 7 && aws_cloudwatch_metric_alarm.dev["broker_disk"].treat_missing_data == "breaching" && aws_cloudwatch_metric_alarm.dev["broker_process"].treat_missing_data == "breaching" && alltrue([for a in aws_cloudwatch_metric_alarm.dev : length(a.alarm_actions) == 0])
    error_message = "Disk/process failures and missing metrics must alarm; notification delivery stays pending without an approved topic."
  }
  assert {
    condition     = alltrue([for l in aws_cloudwatch_log_group.task : l.retention_in_days == 7]) && aws_cloudwatch_log_group.database.retention_in_days == 7 && aws_cloudwatch_log_group.broker.retention_in_days == 7
    error_message = "All application, bootstrap, RDS and broker logs need bounded seven-day retention."
  }
}
run "staged_images_and_least_privilege" {
  command = apply
  variables {
    image_digests = { backend = "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", frontend = "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc" }
  }
  assert {
    condition     = length(aws_ecs_service.app) == 5 && alltrue([for s in aws_ecs_service.app : s.desired_count == 0 && !s.network_configuration[0].assign_public_ip && s.platform_version == "1.4.0"])
    error_message = "Five isolated Fargate capabilities are staged at zero count, without public IPv4."
  }
  assert {
    condition     = alltrue([for t in aws_ecs_task_definition.app : t.cpu == "256" && t.memory == "512" && t.network_mode == "awsvpc" && strcontains(jsondecode(t.container_definitions)[0].image, "@sha256:")])
    error_message = "Task sizing and immutable digest images must match the reviewed cost/security scope."
  }
  assert {
    condition     = alltrue([for k in keys(local.capabilities) : toset(local.execution_secrets[k]) == toset([aws_secretsmanager_secret.runtime[k].arn, aws_secretsmanager_secret.runtime["shared"].arn])]) && length(local.execution_secrets.frontend) == 0
    error_message = "Each API execution role reads only owned/shared secrets; frontend receives no secrets."
  }
  assert {
    condition     = alltrue([for k in keys(local.capabilities) : !contains(local.execution_secrets[k], aws_db_instance.dev.master_user_secret[0].secret_arn) && !contains(local.execution_secrets[k], aws_secretsmanager_secret.runtime["broker"].arn)])
    error_message = "Applications must never read master credentials or the broker private key."
  }
  assert {
    condition     = alltrue([for k in ["inquiries", "notifications"] : contains([for s in jsondecode(aws_ecs_task_definition.app[k].container_definitions)[0].secrets : s.valueFrom], "${aws_secretsmanager_secret.runtime[k].arn}:kafka_password::")])
    error_message = "Producer/consumer must receive separate owned Kafka credentials."
  }
  assert {
    condition     = jsondecode(aws_ecs_task_definition.bootstrap[0].container_definitions)[0].command == ["node", "dist/operations/database-bootstrap.js"] && length(local.execution_secrets.bootstrap) == 5
    error_message = "A separate one-off bootstrap task alone gets the RDS admin plus four owned passwords."
  }
  assert {
    condition     = alltrue([for k in keys(local.capabilities) : one([for e in jsondecode(aws_ecs_task_definition.app[k].container_definitions)[0].environment : e.value if e.name == "SEED_DEMO"]) == "false"])
    error_message = "Synthetic demo seeding must be explicitly disabled by default."
  }
  assert {
    condition     = alltrue([for k in keys(local.capabilities) : strcontains(jsonencode(jsondecode(aws_ecs_task_definition.app[k].container_definitions)[0].healthCheck), "/health/serve")])
    error_message = "Broker outage must not evict HTTP workers and prevent durable outbox writes."
  }
  assert {
    condition     = aws_vpc_security_group_ingress_rule.frontend.referenced_security_group_id == aws_security_group.alb.id && alltrue([for k, r in aws_vpc_security_group_ingress_rule.api : r.referenced_security_group_id == aws_security_group.service["frontend"].id])
    error_message = "Ingress must follow ALB SG to frontend SG to API SG trust."
  }
  assert {
    condition     = length(aws_vpc_security_group_ingress_rule.database) == 5 && alltrue([for r in aws_vpc_security_group_ingress_rule.database : r.cidr_ipv4 == null && r.from_port == 5432]) && length(aws_vpc_security_group_ingress_rule.broker) == 2 && alltrue([for r in aws_vpc_security_group_ingress_rule.broker : r.cidr_ipv4 == null && r.from_port == 9093])
    error_message = "Database/Kafka accept SG references only, never public CIDRs or plaintext Kafka."
  }
  assert {
    condition     = aws_lb_listener.https[0].port == 443 && aws_lb_listener.https[0].protocol == "HTTPS" && aws_lb_target_group.frontend.target_type == "ip" && contains(one(one(aws_lb_listener_rule.application[0].condition).host_header).values, var.application_hostname)
    error_message = "Only HTTPS with the approved hostname may reach IP-mode frontend targets."
  }
  assert {
    condition     = jsondecode(aws_iam_role.execution["identity"].assume_role_policy).Statement[0].Condition.StringEquals["aws:SourceAccount"] == "123456789012" && jsondecode(aws_iam_role.execution["identity"].assume_role_policy).Statement[0].Condition.ArnLike["aws:SourceArn"] == "arn:aws:ecs:us-east-2:123456789012:*"
    error_message = "ECS service roles require source-account and ECS source-ARN trust conditions."
  }
}
run "explicit_activation" {
  command = plan
  variables {
    deploy_application = true
    image_digests      = { backend = "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", frontend = "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc" }
  }
  assert {
    condition     = alltrue([for s in aws_ecs_service.app : s.desired_count == 1 && s.deployment_circuit_breaker[0].rollback])
    error_message = "Explicit activation starts one task/capability and enables deployment circuit-breaker rollback."
  }
}
run "reject_public_exposure" {
  command = plan
  variables { approved_client_cidrs = ["0.0.0.0/0"] }
  expect_failures = [var.approved_client_cidrs]
}
run "reject_activation_without_images" {
  command = plan
  variables { deploy_application = true }
  expect_failures = [var.image_digests]
}
run "reject_mutable_kafka_image" {
  command = plan
  variables { kafka_image = "apache/kafka:latest" }
  expect_failures = [var.kafka_image]
}

run "approved_existing_notification_topic" {
  command = plan
  variables { notification_topic_arn = "arn:aws:sns:us-east-2:123456789012:reviewed-operations" }
  assert {
    condition     = alltrue([for a in aws_cloudwatch_metric_alarm.dev : contains(a.alarm_actions, var.notification_topic_arn) && contains(a.ok_actions, var.notification_topic_arn)])
    error_message = "Only an explicitly supplied existing topic may receive alarm and recovery notifications."
  }
}

run "explicit_synthetic_demo_seeding" {
  command = plan
  variables {
    seed_demo     = true
    image_digests = { backend = "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", frontend = "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc" }
  }
  assert {
    condition     = alltrue([for k in keys(local.capabilities) : one([for e in jsondecode(aws_ecs_task_definition.app[k].container_definitions)[0].environment : e.value if e.name == "SEED_DEMO"]) == "true"])
    error_message = "Only explicit seed_demo=true may activate synthetic demonstration data."
  }
}

run "owner_has_no_hostname_safe_staging" {
  command = plan
  variables {
    application_hostname  = null
    certificate_arn       = null
    approved_client_cidrs = []
  }
  assert {
    condition     = length(aws_lb_listener.https) == 0 && length(aws_lb_listener_rule.application) == 0 && length(aws_vpc_security_group_ingress_rule.https) == 0 && length(aws_ecs_service.app) == 0 && output.access_mode == "no_listener_no_client_ingress_staging"
    error_message = "No hostname means no ALB listener, no client ingress and no running application. Never downgrade to HTTP or invent a domain."
  }
}
run "reject_activation_without_hostname_or_certificate" {
  command = plan
  variables {
    deploy_application    = true
    application_hostname  = null
    certificate_arn       = null
    approved_client_cidrs = []
    image_digests         = { backend = "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", frontend = "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc" }
  }
  expect_failures = [var.application_hostname, var.certificate_arn, var.approved_client_cidrs]
}
