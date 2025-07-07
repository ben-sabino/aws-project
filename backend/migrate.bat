@echo off
setlocal enabledelayedexpansion

REM Script para migração de dados do JSON para PostgreSQL (Windows)

echo 🔄 Iniciando migração de dados para PostgreSQL...

REM Verificar se estamos no diretório correto
if not exist "database.py" (
    echo ❌ Execute este script do diretório backend/
    exit /b 1
)

REM Verificar se o PostgreSQL está rodando
echo 🔍 Verificando conexão com PostgreSQL...
python -c "import os; from sqlalchemy import create_engine; from database import DATABASE_URL; engine = create_engine(DATABASE_URL); connection = engine.connect(); connection.close(); print('✅ Conexão com PostgreSQL estabelecida com sucesso!')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Erro na conexão com PostgreSQL. Verifique se o banco está rodando.
    exit /b 1
)

REM Executar migração
echo 📦 Criando tabelas e migrando dados...
python database.py

echo ✅ Migração concluída com sucesso!
echo.
echo 🔗 Próximos passos:
echo    1. Inicie a aplicação com: docker-compose up
echo    2. Acesse: http://localhost:5173
echo    3. Teste o login com usuário: testuser / senha: testpass

pause
