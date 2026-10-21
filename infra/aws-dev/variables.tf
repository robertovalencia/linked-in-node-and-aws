variable "region" { default = "us-east-1" }
variable "project" {
  default = "linked-in-node"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,24}$", var.project))
    error_message = "Use a short lowercase project slug."
  }
}
variable "github_repository" {
  type        = string
  description = "Exact owner/repository of the independent copy."
  validation {
    condition     = can(regex("^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", var.github_repository))
    error_message = "Specify owner/repository."
  }
}
variable "oidc_provider_arn" {
  type        = string
  description = "Existing account GitHub OIDC provider ARN; create once in account bootstrap."
}
variable "instance_type" { default = "t3.medium" }
