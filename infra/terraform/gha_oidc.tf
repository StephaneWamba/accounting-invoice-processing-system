data "aws_caller_identity" "current" {}

data "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
}

locals {
  github_owner = "StephaneWamba"
  github_repo  = "accounting-invoice-processing-system"
}

data "aws_iam_policy_document" "gha_oidc_assume" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"
    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${local.github_owner}/${local.github_repo}:ref:refs/heads/main"]
    }
  }
}

resource "aws_iam_role" "gha_oidc_role" {
  name               = "${var.app_name}-gha-oidc-role"
  assume_role_policy = data.aws_iam_policy_document.gha_oidc_assume.json
}

data "aws_iam_policy_document" "gha_ecr_push" {
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken"
    ]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:BatchGetImage",
      "ecr:DescribeRepositories",
      "ecr:GetDownloadUrlForLayer"
    ]
    resources = [aws_ecr_repository.app.arn]
  }
}

resource "aws_iam_policy" "gha_ecr_push" {
  name   = "${var.app_name}-gha-ecr-push"
  policy = data.aws_iam_policy_document.gha_ecr_push.json
}

resource "aws_iam_role_policy_attachment" "gha_attach" {
  role       = aws_iam_role.gha_oidc_role.name
  policy_arn = aws_iam_policy.gha_ecr_push.arn
}

output "github_actions_role_arn" {
  value = aws_iam_role.gha_oidc_role.arn
}
