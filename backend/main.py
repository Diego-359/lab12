import firebase_admin
from firebase_admin import credentials, auth, firestore
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.user_service import UserService
from pydantic import BaseModel
from routers import user_router
from auth_utils import get_current_user, require_role

class RoleUpdateBody(BaseModel):
    new_role: str

#cred = credentials.Certificate("hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json")
import os
base_path = os.path.dirname(__file__)
json_path = os.path.join(base_path, "hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json")
cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred)

user_service = UserService()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", 
                   "https://hogar-limpio-frontend.onrender.com"
    ],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router.router)

security = HTTPBearer()

@app.get("/users/me")
async def read_user_me(user: dict = Depends(get_current_user)):
    return {"uid": user["uid"], "email": user.get("email"), "role": user.get("role")}

@app.get("/cleaners/dashboard")
async def cleaners_dashboard(user: dict = Depends(require_role("personal_limpieza"))):
    return {"message": "Welcome, cleaning staff!"}

@app.get("/cliente/profile")
async def client_profile(user: dict = Depends(require_role("cliente"))):
    return {"message": "Your client profile"}

@app.get("/")
def home():
    return {"message": "Public Hello World"}

@app.get("/admin/users", dependencies=[Depends(require_role("admin"))])
async def list_users():
    db = firestore.client()
    users_ref = db.collection("users")
    users = users_ref.stream()
    result = []
    for user in users:
        user_data = user.to_dict()
        user_data["uid"] = user.id
        user_data.pop("created_at", None)
        result.append(user_data)
    return result

@app.post("/users/signup-sync")
async def sync_user(request: Request, token_data=Depends(get_current_user)):
    body = await request.json() if await request.body() else {}
    return user_service.register_new_user(token_data, body)

@app.post("/admin/users/{uid}/role")
async def update_user_role(uid: str, body: RoleUpdateBody, admin: dict = Depends(require_role("admin"))):
    user_service.update_user_role(uid, body.new_role)
    return {"message": f"User role updated to {body.new_role}"}