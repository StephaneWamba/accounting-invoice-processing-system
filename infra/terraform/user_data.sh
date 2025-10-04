#!/bin/bash
yum update -y
yum install -y docker git python3 python3-pip postgresql

# Start Docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create app directory
mkdir -p /home/ec2-user/app
cd /home/ec2-user/app

# Clone repository
git clone https://github.com/StephaneWamba/accounting-invoice-processing-system.git .

# Create environment file
cat > .env << EOF
ENV=production
AWS_REGION=${aws_region}
S3_BUCKET=${s3_bucket}
DATABASE_URL=postgresql+psycopg2://${db_user}:${db_pass}@${db_host}:5432/${db_name}
REDIS_URL=redis://${redis_host}:6379/0
API_KEY=changeme-api-key
ADMIN_PASSWORD=changeme-admin
EOF

# Build and run with Docker Compose
docker-compose up -d --build

# Make sure port 8080 is accessible
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
