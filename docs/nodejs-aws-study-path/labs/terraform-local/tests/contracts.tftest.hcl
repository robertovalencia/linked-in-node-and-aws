run "default_contract" {
  command = apply
  assert {
    condition     = output.release_summary.name == "marketplace-local" && output.release_summary.release == "v1"
    error_message = "Default release output must have the expected name and release."
  }
}

run "custom_input" {
  command = apply
  variables {
    project = "catalog"
    release = "v2"
  }
  assert {
    condition     = output.release_summary.name == "catalog-local" && output.release_summary.release == "v2"
    error_message = "Inputs must flow through locals and resource output."
  }
}

run "invalid_project" {
  command = plan
  variables { project = "Invalid Project" }
  expect_failures = [var.project]
}
