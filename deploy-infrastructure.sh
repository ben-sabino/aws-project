#!/bin/bash

# Script para deploy da infraestrutura AWS com RDS

set -e

echo "🚀 Iniciando deploy da infraestrutura AWS..."

# Verificar se o Terraform está instalado
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform não está instalado. Por favor, instale o Terraform primeiro."
    exit 1
fi

# Verificar se o AWS CLI está instalado
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI não está instalado. Por favor, instale o AWS CLI primeiro."
    exit 1
fi

# Entrar no diretório do Terraform
cd terraform

# Verificar se o arquivo terraform.tfvars existe
if [ ! -f "terraform.tfvars" ]; then
    echo "📝 Criando arquivo terraform.tfvars..."
    cp terraform.tfvars.example terraform.tfvars
    echo "⚠️  Por favor, edite o arquivo terraform/terraform.tfvars com suas configurações antes de continuar."
    echo "   Especialmente a senha do banco de dados (db_password)."
    read -p "Pressione Enter para continuar após editar o arquivo..."
fi

# Inicializar o Terraform
echo "📦 Inicializando Terraform..."
terraform init

# Planejar as mudanças
echo "📋 Planejando as mudanças..."
terraform plan

# Confirmar antes de aplicar
read -p "🤔 Deseja aplicar essas mudanças? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 Aplicando mudanças..."
    terraform apply -auto-approve
    
    echo "✅ Infraestrutura criada com sucesso!"
    echo ""
    echo "📝 Informações do banco de dados:"
    terraform output
    echo ""
    echo "🔗 Para conectar sua aplicação ao RDS:"
    echo "   1. Copie o endpoint do RDS mostrado acima"
    echo "   2. Atualize a variável DATABASE_URL no seu .env"
    echo "   3. Formato: postgresql://username:password@endpoint:5432/database_name"
    echo ""
    echo "⚠️  Lembre-se de atualizar o security group se necessário para permitir conexões do seu IP."
else
    echo "❌ Deploy cancelado."
    exit 1
fi
