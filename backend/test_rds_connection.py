#!/usr/bin/env python3
"""
Script para testar a conexão com o RDS AWS
"""
import os
import sys
from sqlalchemy import text
from database import engine, create_tables, test_rds_connection, SessionLocal
from models import UserCreate
from crud import create_user, get_user_by_username

def main():
    """Função principal para testar RDS"""
    print("🔍 Testando conexão com RDS AWS...")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Variável DATABASE_URL não configurada!")
        print("Configure a variável de ambiente DATABASE_URL")
        print("Exemplo: DATABASE_URL=postgresql://postgres:senha@endpoint:5432/aws_project_db")
        sys.exit(1)
    
    # Mascarar senha na URL para exibição
    safe_url = database_url.replace(database_url.split('@')[0].split(':')[-1], '***')
    print(f"📡 Conectando ao banco: {safe_url}")
    
    # Testar conexão
    if not test_rds_connection():
        print("\n❌ Falha na conexão com RDS!")
        print("Verifique:")
        print("1. Se o RDS está criado e rodando")
        print("2. Se as credenciais estão corretas")
        print("3. Se o Security Group permite conexões")
        print("4. Se o endpoint está correto")
        sys.exit(1)
    
    # Criar tabelas
    try:
        create_tables()
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        sys.exit(1)
    
    # Testar operações CRUD
    try:
        db = SessionLocal()
        
        # Verificar se já existe um usuário de teste
        test_user = get_user_by_username(db, "test_user")
        if test_user:
            print("✅ Usuário de teste já existe!")
        else:
            # Criar usuário de teste
            test_user_data = UserCreate(
                username="test_user",
                password="test123",
                full_name="Usuário de Teste",
                email="test@example.com",
                description="Usuário criado para testar RDS"
            )
            create_user(db, test_user_data)
            print("✅ Usuário de teste criado com sucesso!")
        
        # Verificar informações do banco
        with engine.connect() as connection:
            # Verificar versão do PostgreSQL
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"📊 Versão do PostgreSQL: {version.split(',')[0]}")
            
            # Verificar tabelas
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"📋 Tabelas criadas: {', '.join(tables)}")
            
            # Verificar usuários
            result = connection.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"👥 Total de usuários: {user_count}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Erro ao testar operações CRUD: {e}")
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 Teste de conexão com RDS concluído com sucesso!")
    print("✅ O banco de dados está funcionando corretamente!")
    print("🚀 Você pode agora executar o backend com: uvicorn main:app --reload")

if __name__ == "__main__":
    main() 