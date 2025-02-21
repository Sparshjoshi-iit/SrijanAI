from fastapi import APIRouter, Depends, HTTPException
import schemas
from database import get_db
import firebase_admin.auth as auth

auth_router = APIRouter()

def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase Token")

@auth_router.post("/users", response_model=schemas.UserResponseSchema)
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
        "full_name": user.full_name
    }
    users_ref.document(firebase_user_id).set(new_user)

    return new_user

@auth_router.get("/users/{user_id}", response_model=schemas.UserResponseSchema)
def get_user(user_id: str, db=Depends(get_db)):
    users_ref = db.collection("users").document(user_id).get()
    
    if not users_ref.exists:
        raise HTTPException(status_code=404, detail="User not found")

    return users_ref.to_dict()
