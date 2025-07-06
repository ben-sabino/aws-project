from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os
from datetime import datetime

# Configurações do banco de dados RDS
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:password@localhost:5432/aws_project_db'
)

# Configurações otimizadas para RDS AWS
DB_CONFIG = {
    'pool_size': 5,  # Reduzido para Free Tier
    'max_overflow': 10,
    'pool_pre_ping': True,
    'pool_recycle': 3600,
    'echo': os.getenv('DB_ECHO', 'false').lower() == 'true',
    'connect_args': {
        'connect_timeout': 10,
        'application_name': 'aws-file-storage'
    }
}

# Criar engine do SQLAlchemy com configurações otimizadas para RDS
engine = create_engine(DATABASE_URL, **DB_CONFIG)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Modelo de usuário
class User(Base):
    __tablename__ = "users"

    username = Column(String(50), primary_key=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    profile_image = Column(Text, default="")
    description = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Função para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criar tabelas
def create_tables():
    Base.metadata.create_all(bind=engine)

# Função para testar conexão com RDS
def test_rds_connection():
    """Testa a conexão com o RDS"""
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("✅ Conexão com RDS estabelecida com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro ao conectar com RDS: {e}")
        return False 