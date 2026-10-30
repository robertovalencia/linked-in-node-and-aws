output "deployment_account_id" { value = data.aws_caller_identity.current.account_id }
output "deployment_region" { value = var.region }
output "alb_dns_name" { value = aws_lb.dev.dns_name }
output "application_url" { value = local.https_configured ? "https://${var.application_hostname}" : null }
output "access_mode" { value = local.https_configured ? "https_configured" : "no_listener_no_client_ingress_staging" }
output "cluster_name" { value = aws_ecs_cluster.dev.name }
output "active_private_subnet_id" { value = aws_subnet.private[0].id }
output "service_security_group_ids" { value = { for k, v in aws_security_group.service : k => v.id } }
output "bootstrap_security_group_id" { value = aws_security_group.bootstrap.id }
output "bootstrap_task_definition_arn" { value = try(aws_ecs_task_definition.bootstrap[0].arn, null) }
output "broker_instance_id" { value = aws_instance.broker.id }
output "broker_dns" { value = "kafka.${local.namespace}" }
output "database_endpoint" { value = aws_db_instance.dev.address }
output "database_admin_secret_arn" { value = aws_db_instance.dev.master_user_secret[0].secret_arn }
output "runtime_secret_arns" { value = { for k, v in aws_secretsmanager_secret.runtime : k => v.arn } }
output "repository_urls" { value = { for k, v in aws_ecr_repository.app : k => v.repository_url } }
output "operations_bucket" { value = aws_s3_bucket.operations.id }
output "cost_quantities" {
  value = {
    alb                      = 1, alb_public_subnet_azs = 2, zonal_nat = 1, nat_elastic_ipv4 = 1, private_app_azs = 1,
    fargate_tasks            = var.deploy_application ? 5 : 0, fargate_cpu_per_task = 0.25, fargate_memory_gib_per_task = 0.5,
    rds_instances            = 1, rds_multi_az = false, rds_storage_gib = 20, rds_backup_days = var.rds_backup_retention_days,
    broker_instances         = 1, broker_gp3_gib = 40, broker_public_ipv4 = 0,
    runtime_secret_resources = 6, rds_managed_master_secrets = 1, standard_alarms = 7, custom_host_metrics = 3, log_retention_days = 7,
    interface_endpoints      = 0, s3_gateway_endpoints = 1, cloud_map_namespaces = 1, broker_registered_resources = 1
  }
}

output "alarm_notification_configured" { value = var.notification_topic_arn != null }
