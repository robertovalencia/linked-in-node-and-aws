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
variable "enable_github_deployment" {
  type        = bool
  default     = true
  description = "Create the GitHub OIDC deploy role. Set false to deploy with a temporary local AWS login."
}
variable "oidc_provider_arn" {
  type        = string
  default     = null
  nullable    = true
  description = "Existing account GitHub OIDC provider ARN; required only for GitHub deployment."
  validation {
    condition     = !var.enable_github_deployment || can(regex("^arn:aws[a-z-]*:iam::[0-9]{12}:oidc-provider/token\\.actions\\.githubusercontent\\.com$", var.oidc_provider_arn))
    error_message = "GitHub deployment requires an existing GitHub OIDC provider ARN. For temporary local login deployment, set enable_github_deployment = false."
  }
}
variable "instance_type" {
  type        = string
  default     = "m7i-flex.large"
  description = "x86_64 EC2 type for the single-host demo. Verify regional Free plan eligibility before applying."
}
