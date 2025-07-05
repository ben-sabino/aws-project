#!/usr/bin/env python3
"""
Script opcional para criar um usuário padrão no banco de dados.
Execute apenas se quiser um usuário de teste pré-configurado.
"""

from database import SessionLocal, create_tables
from crud import create_user
from models import UserCreate

def create_default_user():
    """Cria um usuário padrão para testes"""
    
    # Criar tabelas se não existirem
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Verificar se o usuário já existe
        from crud import get_user_by_username
        existing_user = get_user_by_username(db, "admin")
        
        if existing_user:
            print("Usuário 'admin' já existe!")
            return
        
        # Criar usuário padrão
        default_user = UserCreate(
            username="admin",
            password="admin123",
            full_name="Administrador",
            email="admin@example.com",
            description="Usuário administrador padrão"
        )
        
        create_user(db, default_user)
        print("Usuário padrão criado com sucesso!")
        print("Username: admin")
        print("Password: admin123")
        
    except Exception as e:
        print(f"Erro ao criar usuário padrão: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_user() 