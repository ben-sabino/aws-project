from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os
from datetime import datetime

# Configurações do banco de dados
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://username:password@localhost:5432/aws_project_db'
)

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

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