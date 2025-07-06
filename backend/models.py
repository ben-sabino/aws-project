from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    description: Optional[str] = ""

class UserProfile(BaseModel):
    username: str
    full_name: str
    email: str
    profile_image: Optional[str] = ""
    description: Optional[str] = ""
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    profile_image: Optional[str] = None
    description: Optional[str] = None

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

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