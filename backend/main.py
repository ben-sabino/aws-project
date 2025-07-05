from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
import os
import io

# Importar módulos do banco de dados
from database import get_db, create_tables
from models import UserCreate, UserProfile, UserUpdate, PasswordUpdate, FileInfo, StorageUsage, FileUploadResponse
from crud import (
    get_user_by_username, 
    create_user, 
    update_user, 
    update_user_password,
    verify_password
)

# Importar o gerenciador de armazenamento AWS
from aws_storage import storage_manager

# Security configurations
SECRET_KEY = "your-secret-key-keep-it-secret"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://107.20.88.199:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Criar tabelas na inicialização
@app.on_event("startup")
async def startup_event():
    create_tables()

# Função para criar token de acesso

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/register")
async def register(user: UserCreate, db = Depends(get_db)):
    # Verificar se usuário já existe
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Verificar se email já existe
    existing_email = get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Criar usuário no banco
    db_user = create_user(db, user)
    
    # Create access token for the new user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }

@app.post("/api/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=UserProfile)
async def read_users_me(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@app.put("/api/users/me", response_model=UserProfile)
async def update_user_profile(user_update: UserUpdate, token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Atualizar usuário no banco
    updated_user = update_user(db, username, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user

@app.put("/api/users/me/password")
async def update_user_password(password_update: PasswordUpdate, token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not verify_password(password_update.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    new_hashed_password = get_password_hash(password_update.new_password)
    update_user_password(db, username, new_hashed_password)
    
    return {"message": "Password updated successfully"}

# Rotas de gerenciamento de arquivos AWS

@app.get("/api/files", response_model=List[FileInfo])
async def list_user_files(token: str = Depends(oauth2_scheme)):
    """Lista todos os arquivos do usuário"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        files = storage_manager.list_files(username)
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar arquivos: {str(e)}")

@app.post("/api/files/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme)
):
    """Faz upload de um arquivo para o S3"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Validar tamanho do arquivo (máximo 100MB)
    if file.size and file.size > 100 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Arquivo muito grande. Máximo 100MB")
    
    try:
        # Ler conteúdo do arquivo
        file_content = await file.read()
        
        # Fazer upload para o S3
        file_info = storage_manager.upload_file(
            username=username,
            file_content=file_content,
            file_name=file.filename,
            content_type=file.content_type
        )
        
        return FileUploadResponse(
            file=FileInfo(**file_info),
            message="Arquivo enviado com sucesso"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")

@app.get("/api/files/download/{file_name}")
async def download_file(
    file_name: str,
    token: str = Depends(oauth2_scheme)
):
    """Download de um arquivo do S3"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        file_data = storage_manager.download_file(username, file_name)
        if not file_data:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        
        # Criar resposta de streaming
        return StreamingResponse(
            io.BytesIO(file_data['content']),
            media_type=file_data['content_type'],
            headers={
                "Content-Disposition": f"attachment; filename={file_name}",
                "Content-Length": str(file_data['size'])
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer download: {str(e)}")

@app.delete("/api/files/{file_name}")
async def delete_file(
    file_name: str,
    token: str = Depends(oauth2_scheme)
):
    """Deleta um arquivo do S3"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        storage_manager.delete_file(username, file_name)
        return {"message": "Arquivo deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar arquivo: {str(e)}")

@app.get("/api/files/{file_name}/url")
async def get_file_url(
    file_name: str,
    token: str = Depends(oauth2_scheme)
):
    """Gera uma URL pré-assinada para download do arquivo"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        url = storage_manager.get_file_url(username, file_name)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar URL: {str(e)}")

@app.get("/api/storage/usage", response_model=StorageUsage)
async def get_storage_usage(token: str = Depends(oauth2_scheme)):
    """Obtém informações de uso de armazenamento do usuário"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        usage = storage_manager.get_storage_usage(username)
        return StorageUsage(**usage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter uso de armazenamento: {str(e)}")