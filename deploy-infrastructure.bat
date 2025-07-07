@echo off
setlocal enabledelayedexpansion

REM Script para deploy da infraestrutura AWS com RDS (Windows)

echo 🚀 Iniciando deploy da infraestrutura AWS...

REM Verificar se o Terraform está instalado
terraform --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Terraform não está instalado. Por favor, instale o Terraform primeiro.
    exit /b 1
)

REM Verificar se o AWS CLI está instalado
aws --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ AWS CLI não está instalado. Por favor, instale o AWS CLI primeiro.
    exit /b 1
)

REM Entrar no diretório do Terraform
cd terraform

REM Verificar se o arquivo terraform.tfvars existe
if not exist "terraform.tfvars" (
    echo 📝 Criando arquivo terraform.tfvars...
    copy terraform.tfvars.example terraform.tfvars
    echo ⚠️  Por favor, edite o arquivo terraform\terraform.tfvars com suas configurações antes de continuar.
    echo    Especialmente a senha do banco de dados (db_password).
    pause
)

REM Inicializar o Terraform
echo 📦 Inicializando Terraform...
terraform init

REM Planejar as mudanças
echo 📋 Planejando as mudanças...
terraform plan

REM Confirmar antes de aplicar
set /p confirm="🤔 Deseja aplicar essas mudanças? (y/N): "
if /i "!confirm!"=="y" (
    echo 🔧 Aplicando mudanças...
    terraform apply -auto-approve
    
    echo ✅ Infraestrutura criada com sucesso!
    echo.
    echo 📝 Informações do banco de dados:
    terraform output
    echo.
    echo 🔗 Para conectar sua aplicação ao RDS:
    echo    1. Copie o endpoint do RDS mostrado acima
    echo    2. Atualize a variável DATABASE_URL no seu .env
    echo    3. Formato: postgresql://username:password@endpoint:5432/database_name
    echo.
    echo ⚠️  Lembre-se de atualizar o security group se necessário para permitir conexões do seu IP.
) else (
    echo ❌ Deploy cancelado.
    exit /b 1
)

pause
