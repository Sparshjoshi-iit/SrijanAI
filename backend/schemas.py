from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    uid: str
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        orm_mode = True
class ProjectCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectResponseSchema(ProjectCreateSchema):
    project_id: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class AppGenerationRequestSchema(BaseModel):
    user_id: str
    prompt: str

class AppGenerationStatusSchema(BaseModel):
    task_id: str
    status: str 
    created_at: datetime

    class Config:
        orm_mode = True
