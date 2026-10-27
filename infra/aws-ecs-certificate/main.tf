terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 6.0" } }
}
# Certificate request only. Local state contains certificate/DNS metadata, not private keys.
# Do not create a public hosted zone or register a domain as a side effect.
provider "aws" {
  region = "us-east-2"
  default_tags { tags = { Project = "linked-in-node", Environment = "ecs-dev", ManagedBy = "Terraform", Owner = var.owner } }
}
variable "owner" { type = string }
variable "application_hostname" {
  type        = string
  description = "A hostname the operator controls; required before a real certificate request plan."
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]+\\.[a-z]{2,}$", var.application_hostname))
    error_message = "Provide an owned DNS hostname."
  }
}
resource "aws_acm_certificate" "application" {
  domain_name       = var.application_hostname
  validation_method = "DNS"
  key_algorithm     = "RSA_2048"
  options {
    certificate_transparency_logging_preference = "ENABLED"
    export                                      = "DISABLED"
  }
  lifecycle { create_before_destroy = true }
}
output "certificate_arn" { value = aws_acm_certificate.application.arn }
output "dns_validation_records" { value = aws_acm_certificate.application.domain_validation_options }
