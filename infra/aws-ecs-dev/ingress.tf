resource "aws_lb" "dev" {
  name                       = local.name
  internal                   = false
  load_balancer_type         = "application"
  ip_address_type            = "ipv4"
  subnets                    = aws_subnet.public[*].id
  security_groups            = [aws_security_group.alb.id]
  drop_invalid_header_fields = true
  enable_deletion_protection = false
  access_logs {
    bucket  = aws_s3_bucket.operations.id
    prefix  = "alb"
    enabled = true
  }
  depends_on = [aws_s3_bucket_policy.operations, aws_route_table_association.public]
}
resource "aws_lb_target_group" "frontend" {
  name                 = "${local.name}-web"
  port                 = 8180
  protocol             = "HTTP"
  target_type          = "ip"
  vpc_id               = aws_vpc.dev.id
  deregistration_delay = 30
  health_check {
    enabled             = true
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}
resource "aws_lb_listener" "https" {
  count             = local.https_configured ? 1 : 0
  load_balancer_arn = aws_lb.dev.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn
  lifecycle {
    precondition {
      condition     = startswith(var.certificate_arn, "${local.arn_prefix}:acm:${var.region}:${data.aws_caller_identity.current.account_id}:certificate/")
      error_message = "The ALB certificate must belong to this deployment account and Ohio region."
    }
  }
  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Use the approved application hostname"
      status_code  = "403"
    }
  }
}
resource "aws_lb_listener_rule" "application" {
  count        = local.https_configured ? 1 : 0
  listener_arn = aws_lb_listener.https[0].arn
  priority     = 10
  condition {
    host_header {
      values = [var.application_hostname]
    }
  }
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}
