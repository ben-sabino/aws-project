# Configuração do provedor AWS
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Dados da VPC padrão
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Security Group para o RDS
resource "aws_security_group" "rds_sg" {
  name        = "${var.project_name}-rds-sg"
  description = "Security group for RDS database"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Em produção, restringir para IPs específicos
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-rds-sg"
  }
}

# Subnet Group para o RDS
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

# Instância RDS PostgreSQL
resource "aws_db_instance" "postgresql" {
  identifier = "${var.project_name}-postgres"

  # Configurações do banco
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class
  
  # Storage
  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage
  storage_type          = "gp2"
  storage_encrypted     = true

  # Database
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  port     = 5432

  # Subnet e Security Group
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  publicly_accessible    = true  # Permite acesso público ao RDS

  # Backup e Manutenção
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  # Skip final snapshot para desenvolvimento
  skip_final_snapshot = true
  deletion_protection = false

  # Performance Insights
  performance_insights_enabled = true

  tags = {
    Name = "${var.project_name}-postgres"
  }
}

# Outputs
output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.postgresql.endpoint
}

output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.postgresql.port
}

output "database_name" {
  description = "Database name"
  value       = aws_db_instance.postgresql.db_name
}

output "database_username" {
  description = "Database username"
  value       = aws_db_instance.postgresql.username
  sensitive   = true
}
