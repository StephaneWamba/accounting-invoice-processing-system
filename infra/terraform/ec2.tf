data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "ec2_sg" {
  name        = "${var.app_name}-ec2-sg"
  description = "EC2 security group"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app" {
  ami                    = "ami-0c02fb55956c7d316" # Amazon Linux 2
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  subnet_id              = data.aws_subnets.default.ids[0]

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    app_name   = var.app_name
    db_host    = aws_db_instance.postgres.address
    db_name    = "invoice_db"
    db_user    = "postgres"
    db_pass    = var.db_password
    redis_host = aws_elasticache_cluster.redis.cache_nodes[0].address
    s3_bucket  = aws_s3_bucket.files.bucket
    aws_region = var.aws_region
  }))

  tags = {
    Name = var.app_name
  }
}
