resource "aws_ecs_cluster" "dev" {
  name = local.name
  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}
resource "aws_cloudwatch_log_group" "task" {
  for_each          = toset(concat(keys(local.services), ["bootstrap"]))
  name              = "/ecs/${local.name}/${each.key}"
  retention_in_days = 7
}
resource "aws_cloudwatch_log_group" "broker" {
  name              = "/ec2/${local.name}/broker"
  retention_in_days = 7
}
resource "aws_service_discovery_private_dns_namespace" "dev" {
  name        = local.namespace
  description = "Private capability discovery, not a public DNS zone."
  vpc         = aws_vpc.dev.id
}
resource "aws_service_discovery_service" "app" {
  for_each = local.services
  name     = each.key
  dns_config {
    namespace_id   = aws_service_discovery_private_dns_namespace.dev.id
    routing_policy = "MULTIVALUE"
    dns_records {
      type = "A"
      ttl  = 10
    }
  }
  health_check_custom_config {}
}
resource "aws_instance" "broker" {
  ami                         = data.aws_ssm_parameter.ami.value
  instance_type               = "m7i-flex.large"
  subnet_id                   = aws_subnet.private[0].id
  associate_public_ip_address = false
  vpc_security_group_ids      = [aws_security_group.broker.id]
  iam_instance_profile        = aws_iam_instance_profile.broker.name
  metadata_options {
    http_tokens                 = "required"
    http_protocol_ipv6          = "disabled"
    http_put_response_hop_limit = 1
  }
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 40
    encrypted             = true
    delete_on_termination = true
  }
  user_data = templatefile("${path.module}/kafka-user-data.sh.tftpl", {
    aws_region        = var.region
    broker_secret_arn = aws_secretsmanager_secret.runtime["broker"].arn
    broker_dns        = "kafka.${local.namespace}"
    kafka_image       = var.kafka_image
    log_group         = aws_cloudwatch_log_group.broker.name
  })
  # A template update must be reviewed separately; replacing the host deletes Kafka's data volume.
  user_data_replace_on_change = false
  depends_on                  = [aws_route_table_association.private_active, aws_iam_role_policy.broker, aws_iam_role_policy_attachment.ssm]
  tags                        = { Name = "${local.name}-broker" }
}
resource "aws_route53_record" "broker" {
  zone_id = aws_service_discovery_private_dns_namespace.dev.hosted_zone
  name    = "kafka.${local.namespace}"
  type    = "A"
  ttl     = 10
  records = [aws_instance.broker.private_ip]
}
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
    portMappings           = [{ containerPort = port, protocol = "tcp" }]
    environment = service == "frontend" ? [
      { name = "DNS_RESOLVER", value = cidrhost(aws_vpc.dev.cidr_block, 2) },
      { name = "IDENTITY_UPSTREAM", value = "identity.${local.namespace}" },
      { name = "CATALOG_UPSTREAM", value = "catalog.${local.namespace}" },
      { name = "INQUIRIES_UPSTREAM", value = "inquiries.${local.namespace}" },
      { name = "NOTIFICATIONS_UPSTREAM", value = "notifications.${local.namespace}" }
      ] : concat([
        { name = "DEPLOYMENT_MODE", value = "aws-ecs" }, { name = "SEED_DEMO", value = tostring(var.seed_demo) }, { name = "NODE_ENV", value = "production" }, { name = "SERVICE", value = service }, { name = "PORT", value = tostring(port) },
        { name = "DB_HOST", value = aws_db_instance.dev.address }, { name = "DB_PORT", value = "5432" },
        { name = "DB_NAME", value = service }, { name = "DB_USER", value = service },
        { name = "DB_SSL", value = "true" }, { name = "DB_SSL_CA_FILE", value = "/app/certs/rds-us-east-2-bundle.pem" },
        { name = "CATALOG_URL", value = "http://catalog.${local.namespace}:8182" }
        ], contains(local.brokers_clients, service) ? [
        { name = "KAFKA_BROKERS", value = "kafka.${local.namespace}:9093" },
        { name = "KAFKA_SSL", value = "true" }, { name = "KAFKA_SASL_MECHANISM", value = "scram-sha-512" }, { name = "KAFKA_USERNAME", value = service }
    ] : [])
    secrets = service == "frontend" ? [] : concat([
      { name = "DB_PASSWORD", valueFrom = "${aws_secretsmanager_secret.runtime[service].arn}:password::" },
      { name = "JWT_SECRET", valueFrom = "${aws_secretsmanager_secret.runtime["shared"].arn}:JWT_SECRET::" },
      { name = "INTERNAL_API_KEY", valueFrom = "${aws_secretsmanager_secret.runtime["shared"].arn}:INTERNAL_API_KEY::" }
      ], contains(local.brokers_clients, service) ? [
      { name = "KAFKA_SSL_CA", valueFrom = "${aws_secretsmanager_secret.runtime["shared"].arn}:KAFKA_SSL_CA::" },
      { name = "KAFKA_PASSWORD", valueFrom = "${aws_secretsmanager_secret.runtime[service].arn}:kafka_password::" }
    ] : [])
    healthCheck = {
      command     = service == "frontend" ? ["CMD-SHELL", "wget -q -O /dev/null http://127.0.0.1:8180/health || exit 1"] : ["CMD", "node", "-e", "fetch('http://127.0.0.1:${port}/health/serve').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]
      interval    = 30
      timeout     = 5
      retries     = 3
      startPeriod = 60
    }
    logConfiguration = { logDriver = "awslogs", options = { awslogs-group = aws_cloudwatch_log_group.task[service].name, awslogs-region = var.region, awslogs-stream-prefix = "ecs", mode = "non-blocking", max-buffer-size = "1m" } }
  } }
}
resource "aws_ecs_task_definition" "app" {
  for_each                 = local.active_services
  family                   = "${local.name}-${each.key}"
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
  container_definitions = jsonencode([local.app_containers[each.key]])
  depends_on            = [aws_iam_role_policy.execution]
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
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200
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
  service_registries { registry_arn = aws_service_discovery_service.app[each.key].arn }
  dynamic "load_balancer" {
    for_each = each.key == "frontend" ? [1] : []
    content {
      target_group_arn = aws_lb_target_group.frontend.arn
      container_name   = "frontend"
      container_port   = 8180
    }
  }
  depends_on = [aws_lb_listener.https, aws_route_table_association.private_active, aws_vpc_endpoint.s3, aws_route53_record.broker]
}
resource "aws_ecs_task_definition" "bootstrap" {
  count                    = var.image_digests == null ? 0 : 1
  family                   = "${local.name}-bootstrap"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.execution["bootstrap"].arn
  task_role_arn            = aws_iam_role.task["bootstrap"].arn
  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }
  container_definitions = jsonencode([{
    name        = "bootstrap", image = "${aws_ecr_repository.app["backend"].repository_url}@${var.image_digests.backend}", essential = true, user = "1000", readonlyRootFilesystem = true,
    command     = ["node", "dist/operations/database-bootstrap.js"],
    environment = [{ name = "DEPLOYMENT_MODE", value = "aws-ecs" }, { name = "DB_HOST", value = aws_db_instance.dev.address }, { name = "DB_PORT", value = "5432" }, { name = "DB_NAME", value = "postgres" }, { name = "DB_SSL", value = "true" }, { name = "DB_SSL_CA_FILE", value = "/app/certs/rds-us-east-2-bundle.pem" }],
    secrets = concat([
      { name = "DB_USER", valueFrom = "${aws_db_instance.dev.master_user_secret[0].secret_arn}:username::" },
      { name = "DB_PASSWORD", valueFrom = "${aws_db_instance.dev.master_user_secret[0].secret_arn}:password::" }
    ], [for k in keys(local.capabilities) : { name = "${upper(k)}_DB_PASSWORD", valueFrom = "${aws_secretsmanager_secret.runtime[k].arn}:password::" }]),
    linuxParameters  = { initProcessEnabled = true, capabilities = { drop = ["ALL"] } },
    logConfiguration = { logDriver = "awslogs", options = { awslogs-group = aws_cloudwatch_log_group.task["bootstrap"].name, awslogs-region = var.region, awslogs-stream-prefix = "bootstrap" } }
  }])
  depends_on = [aws_iam_role_policy.execution]
}
