variable "name" {
  type = string
}

variable "owner" {
  type = string
  validation {
    condition     = length(trimspace(var.owner)) >= 3
    error_message = "Owner must contain at least three non-padding characters."
  }
}

variable "tier" {
  type = string
}

resource "terraform_data" "record" {
  input = {
    name  = var.name
    owner = trimspace(var.owner)
    tier  = var.tier
  }
  lifecycle {
    precondition {
      condition     = can(regex("^[a-z][a-z0-9-]*$", var.name))
      error_message = "Service name must be a lowercase identifier."
    }
    postcondition {
      condition     = self.output.owner != ""
      error_message = "Stored contract must identify its owner."
    }
  }
}

output "contract" {
  value = terraform_data.record.output
}

output "id" {
  value = terraform_data.record.id
}
