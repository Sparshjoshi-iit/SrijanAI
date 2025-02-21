from fastapi import APIRouter, Depends, HTTPException
import schemas
from database import get_db
import firebase_admin.auth as auth
from datetime import datetime

router = APIRouter()

def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase Token")

@router.post("/users", response_model=schemas.UserResponseSchema)
def create_user(user: schemas.UserRegisterSchema, db=Depends(get_db)):
    decoded_token = verify_firebase_token(user.password)
    firebase_user_id = decoded_token.get("uid")
    email = decoded_token.get("email")

    users_ref = db.collection("users")
    user_doc = users_ref.document(firebase_user_id).get()

    if user_doc.exists:
        return user_doc.to_dict()
    new_user = {
        "uid": firebase_user_id,
        "email": email,
        "full_name": user.full_name,
        "created_at": datetime.utcnow()
    }
    users_ref.document(firebase_user_id).set(new_user)
    return new_user

@router.get("/users/{user_id}", response_model=schemas.UserResponseSchema)
def get_user(user_id: str, db=Depends(get_db)):
    users_ref = db.collection("users").document(user_id).get()
    
    if not users_ref.exists:
        raise HTTPException(status_code=404, detail="User not found")

    return users_ref.to_dict()

@router.post("/projects", response_model=schemas.ProjectResponseSchema)
def create_project(project: schemas.ProjectCreateSchema, db=Depends(get_db)):
    projects_ref = db.collection("projects")
    new_project = {
        "project_id": projects_ref.document().id,
        "user_id": project.user_id,
        "title": project.title,
        "description": project.description,
        "created_at": datetime.utcnow()
    }
    projects_ref.document(new_project["project_id"]).set(new_project)
    return new_project

@router.get("/projects/{user_id}", response_model=list[schemas.ProjectResponseSchema])
def get_user_projects(user_id: str, db=Depends(get_db)):
    projects_ref = db.collection("projects").where("user_id", "==", user_id).stream()
    projects = [doc.to_dict() for doc in projects_ref]
    return projects

@router.delete("/projects/{project_id}")
def delete_project(project_id: str, db=Depends(get_db)):
    project_ref = db.collection("projects").document(project_id)
    if not project_ref.get().exists:
        raise HTTPException(status_code=404, detail="Project not found")

    project_ref.delete()
    return {"message": "Project deleted successfully"}

@router.post("/generate", response_model=schemas.AppGenerationStatusSchema)
def generate_app(request: schemas.AppGenerationRequestSchema, db=Depends(get_db)):
    generation_ref = db.collection("generation_requests")
    task_id = generation_ref.document().id  

    new_request = {
        "task_id": task_id,
        "user_id": request.user_id,
        "prompt": request.prompt,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    generation_ref.document(task_id).set(new_request)
    return new_request

@router.get("/generate/{task_id}", response_model=schemas.AppGenerationStatusSchema)
def check_generation_status(task_id: str, db=Depends(get_db)):
    task_ref = db.collection("generation_requests").document(task_id).get()
    if not task_ref.exists:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_ref.to_dict()
