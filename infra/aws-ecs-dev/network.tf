data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_availability_zones" "available" {
  state = "available"
  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}
data "aws_ssm_parameter" "ami" { name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64" }
locals {
  https_configured = var.certificate_arn != null && var.application_hostname != null && length(var.approved_client_cidrs) > 0
  name             = "${var.project}-ecs-dev"
  namespace        = "${local.name}.internal"
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
  enable_dns_support   = true
}
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.dev.id
  availability_zone       = local.azs[count.index]
  cidr_block              = cidrsubnet(aws_vpc.dev.cidr_block, 8, count.index)
  map_public_ip_on_launch = false
  tags                    = { Name = "${local.name}-public-${count.index + 1}" }
}
resource "aws_subnet" "private" {
  count                   = 2
  vpc_id                  = aws_vpc.dev.id
  availability_zone       = local.azs[count.index]
  cidr_block              = cidrsubnet(aws_vpc.dev.cidr_block, 8, count.index + 10)
  map_public_ip_on_launch = false
  tags                    = { Name = "${local.name}-private-${count.index + 1}" }
}
resource "aws_internet_gateway" "dev" { vpc_id = aws_vpc.dev.id }
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.dev.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.dev.id
  }
}
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
resource "aws_eip" "nat" { domain = "vpc" }
resource "aws_nat_gateway" "dev" {
  availability_mode = "zonal"
  connectivity_type = "public"
  allocation_id     = aws_eip.nat.id
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
}
resource "aws_route_table_association" "private_active" {
  subnet_id      = aws_subnet.private[0].id
  route_table_id = aws_route_table.private_active.id
}
# The second subnet is for RDS subnet-group eligibility, not a second active application AZ.
resource "aws_route_table" "private_standby" { vpc_id = aws_vpc.dev.id }
resource "aws_route_table_association" "private_standby" {
  subnet_id      = aws_subnet.private[1].id
  route_table_id = aws_route_table.private_standby.id
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
resource "aws_security_group" "alb" {
  name        = "${local.name}-alb"
  description = "HTTPS from explicitly approved client networks only."
  vpc_id      = aws_vpc.dev.id
}
resource "aws_security_group" "service" {
  for_each    = local.services
  name        = "${local.name}-${each.key}"
  description = "Private ${each.key} task. Trust paths are explicit SG references."
  vpc_id      = aws_vpc.dev.id
}
resource "aws_security_group" "database" {
  name        = "${local.name}-database"
  description = "PostgreSQL TLS only from capability and bootstrap task security groups."
  vpc_id      = aws_vpc.dev.id
}
resource "aws_security_group" "bootstrap" {
  name        = "${local.name}-bootstrap"
  description = "Privileged one-off DB bootstrap task; no inbound rules."
  vpc_id      = aws_vpc.dev.id
}
resource "aws_security_group" "broker" {
  name        = "${local.name}-broker"
  description = "Private authenticated TLS Kafka; no SSH or public listener."
  vpc_id      = aws_vpc.dev.id
}
resource "aws_vpc_security_group_ingress_rule" "https" {
  for_each          = local.https_configured ? var.approved_client_cidrs : toset([])
  security_group_id = aws_security_group.alb.id
  cidr_ipv4         = each.value
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
}
resource "aws_vpc_security_group_egress_rule" "alb_frontend" {
  security_group_id            = aws_security_group.alb.id
  referenced_security_group_id = aws_security_group.service["frontend"].id
  ip_protocol                  = "tcp"
  from_port                    = 8180
  to_port                      = 8180
}
resource "aws_vpc_security_group_ingress_rule" "frontend" {
  security_group_id            = aws_security_group.service["frontend"].id
  referenced_security_group_id = aws_security_group.alb.id
  ip_protocol                  = "tcp"
  from_port                    = 8180
  to_port                      = 8180
}
resource "aws_vpc_security_group_ingress_rule" "api" {
  for_each                     = local.capabilities
  security_group_id            = aws_security_group.service[each.key].id
  referenced_security_group_id = aws_security_group.service["frontend"].id
  ip_protocol                  = "tcp"
  from_port                    = each.value
  to_port                      = each.value
}
resource "aws_vpc_security_group_egress_rule" "frontend_api" {
  for_each                     = local.capabilities
  security_group_id            = aws_security_group.service["frontend"].id
  referenced_security_group_id = aws_security_group.service[each.key].id
  ip_protocol                  = "tcp"
  from_port                    = each.value
  to_port                      = each.value
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
  referenced_security_group_id = aws_security_group.service["catalog"].id
  ip_protocol                  = "tcp"
  from_port                    = 8182
  to_port                      = 8182
}
resource "aws_vpc_security_group_ingress_rule" "database" {
  for_each                     = merge({ for k in keys(local.capabilities) : k => aws_security_group.service[k].id }, { bootstrap = aws_security_group.bootstrap.id })
  security_group_id            = aws_security_group.database.id
  referenced_security_group_id = each.value
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
}
resource "aws_vpc_security_group_egress_rule" "database" {
  for_each                     = merge({ for k in keys(local.capabilities) : k => aws_security_group.service[k].id }, { bootstrap = aws_security_group.bootstrap.id })
  security_group_id            = each.value
  referenced_security_group_id = aws_security_group.database.id
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
}
resource "aws_vpc_security_group_ingress_rule" "broker" {
  for_each                     = local.brokers_clients
  security_group_id            = aws_security_group.broker.id
  referenced_security_group_id = aws_security_group.service[each.key].id
  ip_protocol                  = "tcp"
  from_port                    = 9093
  to_port                      = 9093
}
resource "aws_vpc_security_group_egress_rule" "broker" {
  for_each                     = local.brokers_clients
  security_group_id            = aws_security_group.service[each.key].id
  referenced_security_group_id = aws_security_group.broker.id
  ip_protocol                  = "tcp"
  from_port                    = 9093
  to_port                      = 9093
}
resource "aws_vpc_security_group_egress_rule" "aws_https" {
  for_each          = merge({ for k, v in aws_security_group.service : k => v.id }, { bootstrap = aws_security_group.bootstrap.id, broker = aws_security_group.broker.id })
  security_group_id = each.value
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
}
# Broker bootstraps AL2023 repositories over HTTP as well as HTTPS; no other task gets port 80.
resource "aws_vpc_security_group_egress_rule" "broker_packages" {
  security_group_id = aws_security_group.broker.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80
}
