run "default_contract" {
  command = apply
  variables {
    services = {
      catalog  = { owner = "team-catalog" }
      identity = { owner = "team-identity", tier = "critical" }
      preview  = { owner = "team-preview", enabled = false }
    }
  }
  assert {
    condition     = toset(keys(output.contracts)) == toset(["catalog", "identity"])
    error_message = "Only enabled stable keys must be instantiated."
  }
  assert {
    condition     = output.contracts.catalog.tier == "standard"
    error_message = "An omitted optional tier must use its default."
  }
}

run "explicit_null_default" {
  command = apply
  variables {
    services = { payments = { owner = "team-payments", tier = null } }
  }
  assert {
    condition     = output.contracts.payments.tier == "standard"
    error_message = "An explicit null must use the non-null optional default."
  }
}

run "child_normalizes_owner" {
  command = apply
  variables {
    services = { payments = { owner = "  team-payments  ", tier = "critical" } }
  }
  assert {
    condition     = output.contracts.payments.owner == "team-payments"
    error_message = "The child contract must trim padding."
  }
}

run "reject_invalid_tier" {
  command = plan
  variables {
    services = { payments = { owner = "team-payments", tier = "gold" } }
  }
  expect_failures = [var.services]
}

run "check_warning_is_observable" {
  command = plan
  variables {
    services = {}
  }
  expect_failures = [check.at_least_one_service]
}
