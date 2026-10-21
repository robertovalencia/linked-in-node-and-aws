mock_provider "aws" {
  mock_data "aws_partition" {
    defaults = { partition = "aws" }
  }
  mock_data "aws_caller_identity" {
    defaults = { account_id = "123456789012" }
  }
  mock_data "aws_ssm_parameter" {
    defaults = { value = "ami-0123456789abcdef0" }
  }
}
variables {
  github_repository = "example/marketplace"
  oidc_provider_arn = "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
}
run "private_management" {
  command = plan
  assert {
    condition     = length(aws_security_group.dev.ingress) == 0
    error_message = "Dev must have no inbound access, including SSH and HTTP."
  }
  assert {
    condition     = aws_instance.dev.metadata_options[0].http_tokens == "required" && aws_instance.dev.root_block_device[0].encrypted
    error_message = "Require IMDSv2 and encrypted disk."
  }
  assert {
    condition     = alltrue([for repository in aws_ecr_repository.app : repository.image_tag_mutability == "IMMUTABLE"])
    error_message = "Release tags must be immutable."
  }
}
