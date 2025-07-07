from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from pydantic import BaseModel, EmailStr
import json
import os
from typing import Optional
import io

# Importar o gerenciador de armazenamento AWS
from aws_storage import storage_manager

# Security configurations
SECRET_KEY = "your-secret-key-keep-it-secret"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
USERS_FILE = "users.json"

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

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def load_users() -> Dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {
        "testuser": {
            "username": "testuser",
            "hashed_password": pwd_context.hash("testpass"),
            "full_name": "Test User",
            "email": "test@example.com",
            "profile_image": "",
            "description": "Usuario de teste",
            "created_at": datetime.utcnow().isoformat(),
        }
    }

def save_users(users: Dict):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Load users from file
fake_users_db = load_users()

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    email: str  # Keep as EmailStr for validation during creation
    description: Optional[str] = ""

class UserProfile(BaseModel):
    username: str
    full_name: str
    email: str  # Changed from EmailStr to str to handle legacy data
    profile_image: Optional[str] = ""
    description: Optional[str] = ""
    created_at: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None  # Changed from EmailStr to str
    profile_image: Optional[str] = None
    description: Optional[str] = None

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

# Modelos para gerenciamento de arquivos
class FileInfo(BaseModel):
    key: str
    name: str
    size: int
    last_modified: str
    etag: str
    content_type: Optional[str] = None

class StorageUsage(BaseModel):
    total_size: int
    file_count: int
    total_size_mb: float

class FileUploadResponse(BaseModel):
    file: FileInfo
    message: str

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
async def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = pwd_context.hash(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_password,
        "full_name": user.full_name,
        "email": user.email,
        "profile_image": "",
        "description": user.description,
        "created_at": datetime.utcnow().isoformat(),
    }
    
    # Save users to file
    save_users(fake_users_db)
    
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
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=UserProfile)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Handle legacy users who might not have all fields
    return UserProfile(
        username=user["username"],
        full_name=user.get("full_name", ""),
        email=user.get("email", ""),
        profile_image=user.get("profile_image", ""),
        description=user.get("description", ""),
        created_at=user.get("created_at", datetime.utcnow().isoformat())
    )

@app.put("/api/users/me", response_model=UserProfile)
async def update_user_profile(user_update: UserUpdate, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    if user_update.full_name is not None:
        user["full_name"] = user_update.full_name
    if user_update.email is not None:
        user["email"] = user_update.email
    if user_update.profile_image is not None:
        user["profile_image"] = user_update.profile_image
    if user_update.description is not None:
        user["description"] = user_update.description
      # Save changes
    save_users(fake_users_db)
    
    return UserProfile(
        username=user["username"],
        full_name=user.get("full_name", ""),
        email=user.get("email", ""),
        profile_image=user.get("profile_image", ""),
        description=user.get("description", ""),
        created_at=user.get("created_at", datetime.utcnow().isoformat())
    )

@app.put("/api/users/me/password")
async def update_user_password(password_update: PasswordUpdate, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not pwd_context.verify(password_update.current_password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    user["hashed_password"] = pwd_context.hash(password_update.new_password)
    
    # Save changes
    save_users(fake_users_db)
    
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

@app.put("/api/files/rename")
async def rename_file(
    old_name: str = Body(...),
    new_name: str = Body(...),
    token: str = Depends(oauth2_scheme)
):
    """Renomeia um arquivo do S3 (copia e deleta o antigo)"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    try:
        ok = storage_manager.rename_file(username, old_name, new_name)
        if not ok:
            raise HTTPException(status_code=404, detail="Arquivo original não encontrado")
        return {"message": "Arquivo renomeado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao renomear arquivo: {str(e)}")

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