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
    condition     = jsondecode(aws_iam_role.deploy[0].assume_role_policy).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:aud"] == "sts.amazonaws.com" && jsondecode(aws_iam_role.deploy[0].assume_role_policy).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == "repo:${var.github_repository}:environment:dev"
    error_message = "Deployment trust must bind the exact repository dev environment and STS audience."
  }
  assert {
    condition     = alltrue([for repository in aws_ecr_repository.app : repository.image_tag_mutability == "IMMUTABLE"])
    error_message = "Release tags must be immutable."
  }
}

run "free_plan_demo_instance" {
  command = plan
  assert {
    condition     = aws_instance.dev.instance_type == "m7i-flex.large"
    error_message = "The reviewed 24-hour demo defaults to m7i-flex.large."
  }
  assert {
    condition     = length(aws_instance.dev.credit_specification) == 0
    error_message = "Non-T instances must omit the unsupported CPU-credit specification."
  }
  assert {
    condition     = aws_instance.dev.root_block_device[0].volume_size == 40 && aws_instance.dev.root_block_device[0].delete_on_termination
    error_message = "The demo has a bounded 40 GiB disk removed on instance termination."
  }
}

run "burstable_without_surplus_charges" {
  command = plan
  variables { instance_type = "t3.medium" }
  assert {
    condition     = aws_instance.dev.credit_specification[0].cpu_credits == "standard"
    error_message = "An explicitly selected T instance must avoid unlimited CPU surplus charges."
  }
}

run "temporary_local_login_deployment" {
  command = plan
  variables {
    region                   = "us-east-2"
    enable_github_deployment  = false
    oidc_provider_arn         = null
  }
  assert {
    condition     = length(aws_iam_role.deploy) == 0 && length(aws_iam_role_policy.deploy) == 0 && output.deploy_role_arn == null
    error_message = "Local login deployment must omit the GitHub deploy role, policy, and output ARN."
  }
  assert {
    condition     = aws_iam_role.host.name == "${var.project}-dev-host" && aws_iam_instance_profile.host.role == aws_iam_role.host.name && aws_iam_role_policy_attachment.ssm.policy_arn == "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
    error_message = "Local deployment must retain the instance role, instance profile, and SSM access."
  }
  assert {
    condition     = length(aws_security_group.dev.ingress) == 0 && aws_instance.dev.metadata_options[0].http_tokens == "required"
    error_message = "Local deployment must retain no-ingress management and IMDSv2."
  }
}

run "github_mode_requires_oidc_provider" {
  command = plan
  variables {
    enable_github_deployment = true
    oidc_provider_arn        = null
  }
  expect_failures = [var.oidc_provider_arn]
}
