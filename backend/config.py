import os
from typing import Optional

class Settings:
    # Configurações do banco de dados
    DATABASE_URL: str = os.getenv(
        'DATABASE_URL',
        'postgresql://username:password@localhost:5432/aws_project_db'
    )
    
    # Configurações de segurança
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-keep-it-secret')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configurações AWS
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION: str = os.getenv('AWS_REGION', 'us-east-1')
    AWS_S3_BUCKET: str = os.getenv('AWS_S3_BUCKET', 'my-file-storage-bucket')

settings = Settings() 