output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "ec2_public_ip" {
  value = aws_instance.app.public_ip
}

output "github_actions_role_arn" {
  value = aws_iam_role.gha_oidc_role.arn
}
