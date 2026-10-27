mock_provider "aws" {}
variables {
  owner                = "mock-reviewer"
  application_hostname = "marketplace.example.com"
}
run "request_only_nonexportable_public_dns_certificate" {
  command = plan
  assert {
    condition     = aws_acm_certificate.application.validation_method == "DNS" && aws_acm_certificate.application.domain_name == var.application_hostname && one(aws_acm_certificate.application.options).export == "DISABLED"
    error_message = "Prepare only a nonexportable public DNS certificate; no domain purchase or hosted zone."
  }
}
run "reject_non_dns_hostname" {
  command = plan
  variables { application_hostname = "https://not-a-hostname/path" }
  expect_failures = [var.application_hostname]
}
