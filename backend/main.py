from fastapi import FastAPI
from router import auth  # Import authentication routes

app = FastAPI()

# Include Routers
app.include_router(auth.auth_router)

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to SrijanAI!"}
