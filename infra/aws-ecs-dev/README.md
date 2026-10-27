# ECS/RDS dev — preparation only

Read [architecture, cost, phased deployment and recovery](../../docs/aws-ecs-dev.md).

No AWS resources were created. `staging.tfvars.example` prepares no listener, no client ingress and no application services when the owner has no hostname. Paid infrastructure would still bill if applied. Do not apply a local-backend preview or start paid staging just to wait for a domain.

`dev.tfvars.example` is the later HTTPS/image configuration. Its documentation CIDR, .invalid hostname and dummy ARN/digests are placeholders only. Application activation requires real owner inputs, successful bootstrap, exact-source verified images and a separately approved plan.

Use a distinct S3 state key `linked-in-node/ecs-dev/terraform.tfstate`. Runtime credentials never belong in Terraform values/state.
