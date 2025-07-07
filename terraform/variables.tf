# Variáveis para configuração do projeto
variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "aws-project"
}

variable "aws_region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-1"
}

# Variáveis do RDS
variable "db_instance_class" {
  description = "Classe da instância RDS"
  type        = string
  default     = "db.t3.micro" # Free tier eligible
}

variable "db_allocated_storage" {
  description = "Storage inicial em GB"
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "Storage máximo em GB"
  type        = number
  default     = 100
}

variable "db_name" {
  description = "Nome do banco de dados"
  type        = string
  default     = "awsproject"
}

variable "db_username" {
  description = "Usuário do banco de dados"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Senha do banco de dados"
  type        = string
  sensitive   = true
  default     = "your-secure-password-here"
}
