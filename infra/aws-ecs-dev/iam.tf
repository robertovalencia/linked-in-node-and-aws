locals {
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
}
resource "aws_iam_role" "execution" {
  for_each           = local.execution_names
  name               = "${local.name}-${each.key}-execution"
  assume_role_policy = local.ecs_trust
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
# Applications call PostgreSQL/Kafka/HTTP, not AWS APIs. Empty task roles cannot fetch master/broker credentials.
resource "aws_iam_role" "task" {
  for_each           = local.execution_names
  name               = "${local.name}-${each.key}-task"
  assume_role_policy = local.ecs_trust
}
resource "aws_iam_role" "broker" {
  name               = "${local.name}-broker"
  assume_role_policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Service = "ec2.amazonaws.com" }, Action = "sts:AssumeRole" }] })
}
resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.broker.name
  policy_arn = "${local.arn_prefix}:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
resource "aws_iam_role_policy" "broker" {
  role = aws_iam_role.broker.id
  policy = jsonencode({ Version = "2012-10-17", Statement = [
    { Sid = "ReadBrokerOnlySecret", Effect = "Allow", Action = ["secretsmanager:GetSecretValue"], Resource = aws_secretsmanager_secret.runtime["broker"].arn },
    { Sid = "WriteBrokerLogs", Effect = "Allow", Action = ["logs:CreateLogStream", "logs:PutLogEvents", "logs:DescribeLogStreams"], Resource = "${aws_cloudwatch_log_group.broker.arn}:*" },
    { Sid = "EmitBoundedHostMetrics", Effect = "Allow", Action = ["cloudwatch:PutMetricData"], Resource = "*", Condition = { StringEquals = { "cloudwatch:namespace" = "Marketplace/ECSDev" } } }
  ] })
}
resource "aws_iam_instance_profile" "broker" { role = aws_iam_role.broker.name }
