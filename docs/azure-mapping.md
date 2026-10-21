# Explaining the Azure equivalents

AWS is the implemented deployment target. This is an interview comparison, not an Azure deployment or tested portability claim. The mappings follow [Microsoft's AWS/Azure comparison](https://learn.microsoft.com/en-us/azure/architecture/aws-professional/services), reviewed October 21, 2026.

| Responsibility here | AWS implementation | Azure equivalent and difference |
|---|---|---|
| Dev host | EC2 with Docker Compose | Azure Linux VM; a VM scale set adds lifecycle/scaling, not database HA automatically |
| Network restrictions | VPC/subnet/security group, no ingress | VNet/subnet/NSG; management access design must be reassessed |
| Management access | SSM session/port forwarding | Azure Bastion/VM Run Command; pricing and tunnel prerequisites differ, so this is no drop-in SSM replacement |
| Host workload identity | EC2 instance profile | Managed identity with scoped Azure RBAC |
| Runtime secrets | Secrets Manager JSON | Key Vault secrets; application retrieval and rotation code changes |
| Private images | ECR | Azure Container Registry; use workload identity and immutable digest deployments |
| Terraform state | Encrypted, versioned S3 with lock file | Azure Blob backend with blob lease locking; separate backend configuration/state |
| GitHub authentication | GitHub OIDC to AWS role | GitHub OIDC to Entra federated credential; audience/subject and roles differ |
| Future managed SQL | RDS PostgreSQL | Azure Database for PostgreSQL Flexible Server |
| Future managed containers | ECS/Fargate | Azure Container Apps, or AKS when Kubernetes requirements justify its overhead |
| Future event broker | MSK Kafka | Event Hubs Kafka endpoint; test protocol/features and semantics rather than assuming full Kafka equivalence |
| Future operations | CloudWatch/CloudTrail | Azure Monitor/Activity Log; verify retention, ingestion cost, and privacy |

The React bundle, Node images, PostgreSQL schema, HTTP contracts, and domain rules can move without rewriting the product. Terraform resources, secret acquisition, IAM, registry authentication, network defaults, and deployment runbooks are cloud-specific. Introduce a separate `infra/azure-dev` root and separate remote state if Azure becomes an actual requirement; never share the AWS dev state or secrets.

For a production discussion, start with availability, RPO/RTO, compliance, workload traffic, team skills, and budget. Managed PostgreSQL removes some patching/backup work but needs restore drills. Managed containers improve rollout/scale behavior but do not fix cross-service transaction design. The transactional outbox and idempotent notification consumer remain necessary on either cloud. Microsoft's [VM baseline](https://learn.microsoft.com/en-us/azure/architecture/virtual-machines/baseline) provides a concrete production comparison; its redundancy and governance are intentionally beyond this one-host dev target.
