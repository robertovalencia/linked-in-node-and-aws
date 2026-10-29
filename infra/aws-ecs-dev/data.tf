resource "aws_secretsmanager_secret" "runtime" {
  for_each                = local.secret_names
  name                    = "${local.name}/${each.key}"
  recovery_window_in_days = var.teardown_discard_demo_data ? 0 : 7
}
# Secret values are populated out of band after provisioning. Never declare secret versions or passwords here.
resource "aws_db_subnet_group" "dev" {
  name       = local.name
  subnet_ids = aws_subnet.private[*].id
}
resource "aws_db_parameter_group" "dev" {
  name   = local.name
  family = "postgres17"
  parameter {
    name         = "rds.force_ssl"
    value        = "1"
    apply_method = "pending-reboot"
  }
  parameter {
    name  = "log_statement"
    value = "none"
  }
  # Bootstrap CREATE/ALTER ROLE statements contain passwords as SQL literals.
  # Do not export full failed statements to CloudWatch.
  parameter {
    name  = "log_min_error_statement"
    value = "panic"
  }
}
resource "aws_cloudwatch_log_group" "database" {
  name              = "/aws/rds/instance/${local.name}/postgresql"
  retention_in_days = 7
}
resource "aws_db_instance" "dev" {
  identifier                      = local.name
  engine                          = "postgres"
  engine_version                  = var.postgres_engine_version
  engine_lifecycle_support        = "open-source-rds-extended-support-disabled"
  instance_class                  = "db.t4g.small"
  allocated_storage               = 20
  max_allocated_storage           = 20
  storage_type                    = "gp3"
  storage_encrypted               = true
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
  backup_retention_period         = 7
  backup_window                   = "05:00-05:30"
  maintenance_window              = "sun:06:00-sun:07:00"
  auto_minor_version_upgrade      = true
  deletion_protection             = var.teardown_discard_demo_data ? false : var.protect_database
  skip_final_snapshot             = var.teardown_discard_demo_data
  final_snapshot_identifier       = var.teardown_discard_demo_data ? null : "${local.name}-final-${var.recovery_snapshot_suffix}"
  delete_automated_backups        = var.teardown_discard_demo_data
  copy_tags_to_snapshot           = true
  enabled_cloudwatch_logs_exports = ["postgresql"]
  monitoring_interval             = 0
  performance_insights_enabled    = false
  depends_on                      = [aws_cloudwatch_log_group.database]
}
resource "aws_ecr_repository" "app" {
  for_each             = toset(["backend", "frontend"])
  name                 = "${local.name}/${each.key}"
  image_tag_mutability = "IMMUTABLE"
  # Existing lab behavior: destroying a repository also removes its images.
  force_delete = true
  image_scanning_configuration { scan_on_push = true }
  encryption_configuration { encryption_type = "AES256" }
}
resource "aws_ecr_lifecycle_policy" "app" {
  for_each   = aws_ecr_repository.app
  repository = each.value.name
  policy     = jsonencode({ rules = [{ rulePriority = 1, description = "Expire untagged lab images after seven days", selection = { tagStatus = "untagged", countType = "sinceImagePushed", countUnit = "days", countNumber = 7 }, action = { type = "expire" } }] })
}
resource "aws_s3_bucket" "operations" {
  bucket_prefix = "${local.name}-ops-"
  # Provider requires a successful transition apply before destroy can empty it.
  # This is the operations bucket only; bootstrap Terraform state stays separate.
  force_destroy = var.teardown_discard_demo_data
}
resource "aws_s3_bucket_public_access_block" "operations" {
  bucket                  = aws_s3_bucket.operations.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_versioning" "operations" {
  bucket = aws_s3_bucket.operations.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "operations" {
  bucket = aws_s3_bucket.operations.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
resource "aws_s3_bucket_lifecycle_configuration" "operations" {
  bucket = aws_s3_bucket.operations.id
  rule {
    id     = "bounded-lab-records"
    status = "Enabled"
    filter { prefix = "" }
    expiration { days = 7 }
    noncurrent_version_expiration { noncurrent_days = 7 }
    abort_incomplete_multipart_upload { days_after_initiation = 1 }
  }
}
resource "aws_s3_bucket_policy" "operations" {
  bucket = aws_s3_bucket.operations.id
  policy = jsonencode({ Version = "2012-10-17", Statement = [
    { Sid = "DenyInsecureTransport", Effect = "Deny", Principal = "*", Action = "s3:*", Resource = [aws_s3_bucket.operations.arn, "${aws_s3_bucket.operations.arn}/*"], Condition = { Bool = { "aws:SecureTransport" = "false" } } },
    { Sid = "ALBAccessLogs", Effect = "Allow", Principal = { Service = "logdelivery.elasticloadbalancing.amazonaws.com" }, Action = "s3:PutObject", Resource = "${aws_s3_bucket.operations.arn}/alb/AWSLogs/${data.aws_caller_identity.current.account_id}/*", Condition = { ArnLike = { "aws:SourceArn" = "${local.arn_prefix}:elasticloadbalancing:${var.region}:${data.aws_caller_identity.current.account_id}:loadbalancer/app/${local.name}/*" } } }
  ] })
}
