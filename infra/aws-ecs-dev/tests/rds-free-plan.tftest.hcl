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
run "micro_candidate_preserves_private_backups_and_no_app_scope" {
  command = plan
  variables { rds_backup_retention_days = 1 }
  assert {
    condition     = aws_db_instance.dev.instance_class == "db.t4g.micro" && aws_db_instance.dev.backup_retention_period == 1 && !aws_db_instance.dev.publicly_accessible && aws_db_instance.dev.storage_encrypted && aws_db_instance.dev.deletion_protection && !aws_db_instance.dev.skip_final_snapshot && !aws_db_instance.dev.delete_automated_backups && output.cost_quantities.fargate_tasks == 0
    error_message = "The Free-plan micro candidate must preserve backups, private encrypted storage and recovery controls, with no app tasks. Mock success is not AWS acceptance."
  }
}
