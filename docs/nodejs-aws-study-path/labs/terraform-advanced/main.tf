terraform {
  required_version = ">= 1.10, < 2.0"
}

variable "services" {
  description = "Stable service keys; synthetic metadata only, never secrets."
  type = map(object({
    owner   = string
    enabled = optional(bool, true)
    tier    = optional(string, "standard")
  }))
  default = {
    catalog  = { owner = "team-catalog" }
    identity = { owner = "team-identity", tier = "critical" }
    preview  = { owner = "team-preview", enabled = false }
  }
  validation {
    condition = alltrue([
      for key, service in var.services :
      can(regex("^[a-z][a-z0-9-]*$", key)) && contains(["standard", "critical"], service.tier)
    ])
    error_message = "Keys must be lowercase identifiers and tier must be standard or critical."
  }
}

locals {
  enabled_services = { for key, service in var.services : key => service if service.enabled }
}

module "service" {
  source   = "./modules/service"
  for_each = local.enabled_services
  name     = each.key
  owner    = each.value.owner
  tier     = each.value.tier
}

output "contracts" {
  description = "Explicit child-module output interface, keyed by stable identity."
  value       = { for key, service in module.service : key => service.contract }
}

output "identities" {
  value = { for key, service in module.service : key => service.id }
}

check "at_least_one_service" {
  assert {
    condition     = length(local.enabled_services) > 0
    error_message = "The study inventory should include an enabled service."
  }
}
