#!/bin/bash

# Script para migração de dados do JSON para PostgreSQL

set -e

echo "🔄 Iniciando migração de dados para PostgreSQL..."

# Verificar se estamos no diretório correto
if [ ! -f "database.py" ]; then
    echo "❌ Execute este script do diretório backend/"
    exit 1
fi

# Verificar se o PostgreSQL está rodando
echo "🔍 Verificando conexão com PostgreSQL..."
python3 -c "
import os
from sqlalchemy import create_engine
from database import DATABASE_URL

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    connection.close()
    print('✅ Conexão com PostgreSQL estabelecida com sucesso!')
except Exception as e:
    print(f'❌ Erro na conexão: {e}')
    exit(1)
" || exit 1

# Executar migração
echo "📦 Criando tabelas e migrando dados..."
python3 database.py

echo "✅ Migração concluída com sucesso!"
echo ""
echo "🔗 Próximos passos:"
echo "   1. Inicie a aplicação com: docker-compose up"
echo "   2. Acesse: http://localhost:5173"
echo "   3. Teste o login com usuário: testuser / senha: testpass"
