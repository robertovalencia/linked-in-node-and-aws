terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 6.0" } }
}
provider "aws" { region = var.region }
variable "region" { default = "us-east-1" }
variable "state_bucket" { type = string }
resource "aws_s3_bucket" "state" {
  bucket = var.state_bucket
  lifecycle { prevent_destroy = true }
}
resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
resource "aws_s3_bucket_public_access_block" "state" {
  bucket                  = aws_s3_bucket.state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
output "state_bucket" { value = aws_s3_bucket.state.id }
resource "aws_s3_bucket_policy" "state_tls" {
  bucket = aws_s3_bucket.state.id
  policy = jsonencode({ Version = "2012-10-17", Statement = [{ Sid = "DenyInsecureTransport", Effect = "Deny", Principal = "*", Action = "s3:*", Resource = [aws_s3_bucket.state.arn, "${aws_s3_bucket.state.arn}/*"], Condition = { Bool = { "aws:SecureTransport" = "false" } } }] })
}
variable "create_github_oidc" {
  type        = bool
  default     = false
  description = "Set true only if the account does not already have GitHub's OIDC provider."
}
resource "aws_iam_openid_connect_provider" "github" {
  count          = var.create_github_oidc ? 1 : 0
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}
output "created_oidc_provider_arn" { value = try(aws_iam_openid_connect_provider.github[0].arn, null) }
