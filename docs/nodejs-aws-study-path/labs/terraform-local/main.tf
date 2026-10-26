terraform {
  required_version = ">= 1.10, < 2.0"
}

variable "project" {
  type    = string
  default = "marketplace"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,24}$", var.project))
    error_message = "Use a short lowercase project slug."
  }
}

variable "release" {
  type    = string
  default = "v1"
}

variable "generation" {
  type    = number
  default = 1
}

locals {
  name = "${var.project}-local"
}

resource "terraform_data" "release" {
  input = {
    name    = local.name
    release = var.release
  }
  triggers_replace = var.generation
}

output "release_summary" {
  value = terraform_data.release.output
}
