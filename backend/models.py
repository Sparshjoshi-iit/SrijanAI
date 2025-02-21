from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    uid:str
    email:str
    full_name:Optional[str]=None
    created_at:datetime=datetime.utcnow()
    
class Project(BaseModel):
    project_id:str
    user_id:str
    title:str
    description:Optional[str]=None
    created_at:datetime=datetime.utcnow()
    
class createProjectRequest(BaseModel):
    prompt:str
    user_id:str
    status:Optional[str]=None
    created_at:datetime=datetime.utcnow()
    