# Free public certificate request — separate review stage

An owned hostname is required. This root prepares one nonexportable public ACM certificate in Ohio with DNS validation. It does not buy a domain, create a hosted zone, start paid application infrastructure or validate ownership automatically.

`terraform plan -var='owner=YOUR_OWNER' -var='application_hostname=YOUR_OWNED_NAME' -out=certificate.tfplan` prepares a request for review. Do not apply without explicit approval. After an approved request, add the exact CNAME from `terraform output -json dns_validation_records` at your DNS provider and verify ACM ISSUED before the ECS infrastructure plan. Keep the validation record for renewal.

Local state contains certificate/DNS metadata only and is ignored. Keep state/plans out of Git. See [the full runbook](../../docs/aws-ecs-dev.md).
