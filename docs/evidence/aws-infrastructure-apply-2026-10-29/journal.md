# Actual execution journal and repair — 29–30 October

Working directory for Terraform: `infra/aws-ecs-dev` in this repository. The named profile is `marketplace-dev`, region `us-east-2`, account `772641336063`, default workspace, protected S3 application state. Raw transcripts are private.

| Executed command or operation | Purpose | Actual outcome |
|---|---|---|
|Source/binary/JSON/provider-lock/backend/privacy guards; STS, Free-plan and empty-state reads|Bind the exact human-approved artifact and current account|Passed before initial apply|
|`terraform apply -input=false -json <exact approved application.tfplan>`|Apply only approved SHA256 `2fd776a529ab587759500bf71e43c5f461a528034db2942d5af2f664fe222b56`|Exit 1; 99 completed creates, 100 managed instances including tainted ALB|
|`terraform output -json`; `terraform state pull`|Preserve partial state and actual outputs|Captured privately; intended URL is not proof of a working endpoint|
|Scoped read-only ALB/RDS/ECS/EC2/SG/Cloud Map/log/secret-metadata checks by independent critic|Verify actual allocation and failures|ALB exists with no listeners and access logging disabled; RDS absent; broker DNS absent; no app tasks; seven alarms absent|
|`aws login --profile marketplace-login --region us-east-1` on 30 October|Human-approved renewal of temporary credentials|Succeeded; no provisioning|
|`aws sts get-caller-identity`; `aws freetier get-account-plan-state --region us-east-1`|Recheck account and credits|Free/ACTIVE; $98.59 reported credits at 14:40 UTC, not a hard cap or real-time invoice|
|`terraform workspace show`; `terraform state pull`|Check the real partial S3-backed baseline|Default workspace, serial 4, 100 managed instances, only ALB tainted; separate states unchanged|
|Scoped ALB/listener/RDS/ECS/Cloud Map/ACM reads on 30 October|Check whether the partial deployment changed|No RDS/listener/app services or running/pending tasks; existing certificate preserved|
|Source comparison guard before repair plan|Detect unexpected state changes|Stopped on check-result list ordering only; independently compared identical resources/outputs/serial/lineage; refusal preserved|
|`terraform fmt -check -recursive`; `terraform validate -json`|Check current repair configuration|Passed|
|First fresh `terraform plan -input=false -lock-timeout=60s -detailed-exitcode -json -var-file=<private inputs> -out=<private repair.tfplan>`|Reveal actual repair actions; no apply|Exit 2; 19 adds/81 updates/7 destroys. Rejected because latest-AMI drift would replace the broker. Five unused discovery service replacements also exposed ineffective empty custom-health blocks|

The repair pins the existing broker AMI instead of suppressing drift with lifecycle ignores, fixes the custom health configuration, uses Cloud Map registration for the broker, adopts the documented ALB log-delivery condition and proposes explicit one-day RDS backup retention. A new saved plan and independent review are required. One-day Free-plan acceptance is unproven; no account upgrade is authorized. No failed artifact is retried.

See [ALB logging requirements](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/enable-access-logging.html), [Cloud Map instance registration](https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html), [custom health configuration](https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html) and [RDS backup retention](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html). A shorter backup window is a recovery tradeoff, not a proven cost saving or account eligibility guarantee.
