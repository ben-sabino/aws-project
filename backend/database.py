import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configurações do banco de dados
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:guilberth2305@database-1-instance-1.c010ka2ko3xe.us-east-1.rds.amazonaws.com:5432/awsproject"
)

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo do usuário
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    profile_image = Column(String(255), default="")
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "full_name": self.full_name,
            "email": self.email,
            "profile_image": self.profile_image,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

# Função para criar as tabelas
def create_tables():
    Base.metadata.create_all(bind=engine)

# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para migrar dados do JSON para o PostgreSQL
def migrate_json_to_postgres():
    """Migra dados do users.json para o PostgreSQL"""
    import json
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    if not os.path.exists("users.json"):
        print("Arquivo users.json não encontrado, criando usuário padrão...")
        # Criar usuário padrão
        db = SessionLocal()
        default_user = User(
            username="testuser",
            hashed_password=pwd_context.hash("testpass"),
            full_name="Test User",
            email="test@example.com",
            profile_image="",
            description="Usuario de teste",
            created_at=datetime.utcnow()
        )
        db.add(default_user)
        db.commit()
        db.close()
        return
    
    with open("users.json", "r") as f:
        users_data = json.load(f)
    
    db = SessionLocal()
    
    for username, user_data in users_data.items():
        # Verificar se o usuário já existe
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"Usuário {username} já existe no banco, pulando...")
            continue
        
        # Criar novo usuário
        new_user = User(
            username=user_data["username"],
            hashed_password=user_data["hashed_password"],
            full_name=user_data.get("full_name", ""),
            email=user_data.get("email", ""),
            profile_image=user_data.get("profile_image", ""),
            description=user_data.get("description", ""),
            created_at=datetime.fromisoformat(user_data.get("created_at", datetime.utcnow().isoformat()))
        )
        
        db.add(new_user)
        print(f"Usuário {username} migrado para o PostgreSQL")
    
    db.commit()
    db.close()
    print("Migração concluída!")

if __name__ == "__main__":
    create_tables()
    migrate_json_to_postgres()
