"""routes/auth_routes.py"""
from fastapi import APIRouter, HTTPException, Response, Depends
from datetime import datetime, timezone

from database import users_collection
from auth import hash_password, verify_password, create_access_token, get_current_user
from models.user_model import UserRegister, UserLogin

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/register")
async def register(data: UserRegister, response: Response):
    users = users_collection()

    existing = users.select("*").eq("email", data.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "name":       data.name,
        "email":      data.email,
        "password":   hash_password(data.password),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    
    result = users.insert(user_doc).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create user")
        
    inserted_user = result.data[0]
    user_id = str(inserted_user["id"])

    token = create_access_token({
        "sub":   user_id,
        "email": data.email,
        "name":  data.name,
    })

    # Set cookie same as login so session works
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=86400,
        samesite="lax",
    )

    return {
        "message": "Registration successful",
        "token": token,
        "user": {
            "id":    user_id,
            "name":  data.name,
            "email": data.email,
        },
    }

@router.post("/login")
async def login(data: UserLogin, response: Response):
    users = users_collection()
    
    result = users.select("*").eq("email", data.email).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    user = result.data[0]

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({
        "sub":   str(user["id"]),
        "email": user["email"],
        "name":  user.get("name", "User"),
    })

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=86400,
        samesite="lax",
    )

    return {
        "message": "Login successful",
        "token":   token,
        "user": {
            "id":    str(user["id"]),
            "name":  user.get("name"),
            "email": user["email"],
        },
    }

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    users = users_collection()
    result = users.select("*").eq("id", current_user["sub"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
        
    user = result.data[0]
    return {
        "id":    str(user["id"]),
        "name":  user.get("name"),
        "email": user["email"],
    }
