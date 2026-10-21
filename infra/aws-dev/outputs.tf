output "instance_id" { value = aws_instance.dev.id }
output "deploy_role_arn" { value = aws_iam_role.deploy.arn }
output "secret_arn" { value = aws_secretsmanager_secret.runtime.arn }
output "release_bucket" { value = aws_s3_bucket.releases.id }
output "backend_repository" { value = aws_ecr_repository.app["backend"].repository_url }
output "frontend_repository" { value = aws_ecr_repository.app["frontend"].repository_url }

output "deployment_account_id" { value = data.aws_caller_identity.current.account_id }
