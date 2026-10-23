data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_ssm_parameter" "ami" { name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64" }
locals {
  name       = "${var.project}-dev"
  arn_prefix = "arn:${data.aws_partition.current.partition}"
}
resource "aws_vpc" "dev" {
  cidr_block           = "10.84.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}
resource "aws_subnet" "dev" {
  vpc_id                  = aws_vpc.dev.id
  cidr_block              = "10.84.1.0/24"
  map_public_ip_on_launch = true
}
resource "aws_internet_gateway" "dev" { vpc_id = aws_vpc.dev.id }
resource "aws_route_table" "dev" {
  vpc_id = aws_vpc.dev.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.dev.id
  }
}
resource "aws_route_table_association" "dev" {
  subnet_id      = aws_subnet.dev.id
  route_table_id = aws_route_table.dev.id
}
resource "aws_security_group" "dev" {
  name        = local.name
  description = "No ingress. SSM manages host and tunnels browser traffic."
  ingress     = []
  vpc_id      = aws_vpc.dev.id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_secretsmanager_secret" "runtime" {
  name                    = "${local.name}/runtime"
  recovery_window_in_days = 7
}
resource "aws_ecr_repository" "app" {
  for_each             = toset(["backend", "frontend"])
  name                 = "${local.name}/${each.key}"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = true
  image_scanning_configuration { scan_on_push = true }
  encryption_configuration { encryption_type = "AES256" }
}
resource "aws_ecr_lifecycle_policy" "app" {
  for_each   = aws_ecr_repository.app
  repository = each.value.name
  policy     = jsonencode({ rules = [{ rulePriority = 1, description = "Expire untagged images after seven days", selection = { tagStatus = "untagged", countType = "sinceImagePushed", countUnit = "days", countNumber = 7 }, action = { type = "expire" } }] })
}
resource "aws_s3_bucket" "releases" {
  bucket_prefix = "${local.name}-releases-"
  force_destroy = true
}
resource "aws_s3_bucket_public_access_block" "releases" {
  bucket                  = aws_s3_bucket.releases.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_versioning" "releases" {
  bucket = aws_s3_bucket.releases.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "releases" {
  bucket = aws_s3_bucket.releases.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
resource "aws_iam_role" "host" {
  name               = "${local.name}-host"
  assume_role_policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Service = "ec2.amazonaws.com" }, Action = "sts:AssumeRole" }] })
}
resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.host.name
  policy_arn = "${local.arn_prefix}:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
resource "aws_iam_role_policy" "host" {
  role = aws_iam_role.host.id
  policy = jsonencode({ Version = "2012-10-17", Statement = [
    { Effect = "Allow", Action = ["secretsmanager:GetSecretValue"], Resource = aws_secretsmanager_secret.runtime.arn },
    { Effect = "Allow", Action = ["ecr:GetAuthorizationToken"], Resource = "*" },
    { Effect = "Allow", Action = ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer", "ecr:BatchCheckLayerAvailability"], Resource = [for r in aws_ecr_repository.app : r.arn] },
    { Effect = "Allow", Action = ["s3:GetObject"], Resource = "${aws_s3_bucket.releases.arn}/releases/*" }
  ] })
}
resource "aws_iam_instance_profile" "host" { role = aws_iam_role.host.name }
resource "aws_instance" "dev" {
  depends_on             = [aws_route_table_association.dev, aws_iam_role_policy.host, aws_iam_role_policy_attachment.ssm]
  ami                    = data.aws_ssm_parameter.ami.value
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.dev.id
  vpc_security_group_ids = [aws_security_group.dev.id]
  iam_instance_profile   = aws_iam_instance_profile.host.name
  metadata_options {
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 40
    encrypted             = true
    delete_on_termination = true
  }
  # CPU-credit options apply only to burstable T instances. Non-T families
  # such as m7i-flex must omit the API field entirely.
  dynamic "credit_specification" {
    for_each = can(regex("^t[0-9]", var.instance_type)) ? [1] : []
    content { cpu_credits = "standard" }
  }
  user_data                   = file("${path.module}/user-data.sh")
  user_data_replace_on_change = true
  tags                        = { Name = local.name }
}
resource "aws_iam_role" "deploy" {
  count              = var.enable_github_deployment ? 1 : 0
  name               = "${local.name}-github-deploy"
  assume_role_policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Federated = var.oidc_provider_arn }, Action = "sts:AssumeRoleWithWebIdentity", Condition = { StringEquals = { "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com", "token.actions.githubusercontent.com:sub" = "repo:${var.github_repository}:environment:dev" } } }] })
}
resource "aws_iam_role_policy" "deploy" {
  count = var.enable_github_deployment ? 1 : 0
  role  = aws_iam_role.deploy[0].id
  policy = jsonencode({ Version = "2012-10-17", Statement = [
    { Effect = "Allow", Action = ["ecr:GetAuthorizationToken"], Resource = "*" },
    { Effect = "Allow", Action = ["ecr:BatchCheckLayerAvailability", "ecr:InitiateLayerUpload", "ecr:UploadLayerPart", "ecr:CompleteLayerUpload", "ecr:PutImage", "ecr:BatchGetImage", "ecr:DescribeImageScanFindings"], Resource = [for r in aws_ecr_repository.app : r.arn] },
    { Effect = "Allow", Action = ["s3:PutObject"], Resource = "${aws_s3_bucket.releases.arn}/releases/*" },
    { Effect = "Allow", Action = ["ssm:SendCommand"], Resource = [aws_instance.dev.arn, "${local.arn_prefix}:ssm:${var.region}::document/AWS-RunShellScript"] },
    { Effect = "Allow", Action = ["ssm:GetCommandInvocation"], Resource = "*" }
  ] })
}
resource "aws_s3_bucket_policy" "releases_tls" {
  bucket = aws_s3_bucket.releases.id
  policy = jsonencode({ Version = "2012-10-17", Statement = [{ Sid = "DenyInsecureTransport", Effect = "Deny", Principal = "*", Action = "s3:*", Resource = [aws_s3_bucket.releases.arn, "${aws_s3_bucket.releases.arn}/*"], Condition = { Bool = { "aws:SecureTransport" = "false" } } }] })
}
