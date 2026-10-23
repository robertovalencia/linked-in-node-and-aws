mock_provider "aws" {}
variables { state_bucket = "marketplace-test-state" }

# Apply resolves computed bucket ARNs using the mock provider only; no AWS calls.
run "private_encrypted_state" {
  command = apply
  assert {
    condition     = aws_s3_bucket_versioning.state.versioning_configuration[0].status == "Enabled"
    error_message = "State must retain object versions for recovery."
  }
  assert {
    condition     = one(aws_s3_bucket_server_side_encryption_configuration.state.rule).apply_server_side_encryption_by_default[0].sse_algorithm == "AES256"
    error_message = "State must be encrypted at rest."
  }
  assert {
    condition     = aws_s3_bucket_public_access_block.state.block_public_acls && aws_s3_bucket_public_access_block.state.block_public_policy && aws_s3_bucket_public_access_block.state.ignore_public_acls && aws_s3_bucket_public_access_block.state.restrict_public_buckets
    error_message = "State must block every S3 public-access mechanism."
  }
  assert {
    condition     = length(aws_iam_openid_connect_provider.github) == 0
    error_message = "Bootstrap must reuse an existing account OIDC provider unless creation is explicitly selected."
  }
  assert {
    condition     = jsondecode(aws_s3_bucket_policy.state_tls.policy).Statement[0].Condition.Bool["aws:SecureTransport"] == "false" && jsondecode(aws_s3_bucket_policy.state_tls.policy).Statement[0].Effect == "Deny"
    error_message = "State access over insecure transport must be denied."
  }
}

run "explicit_github_oidc" {
  command = plan
  variables { create_github_oidc = true }
  assert {
    condition     = length(aws_iam_openid_connect_provider.github) == 1 && aws_iam_openid_connect_provider.github[0].url == "https://token.actions.githubusercontent.com" && contains(aws_iam_openid_connect_provider.github[0].client_id_list, "sts.amazonaws.com")
    error_message = "Opt-in GitHub OIDC must use the correct issuer and STS audience."
  }
}
