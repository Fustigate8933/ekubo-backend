import os

import bcrypt
import jwt
from fastapi import APIRouter, HTTPException
from httpx import AsyncClient

from models.auth import LoginRequest, SignupRequest

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")


async def get_user_by_email(email: str):
    async with AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/users",
            params={"select": "*", "email": f"eq.{email}"},
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Accept": "application/json",
            },
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=500, detail="Error fetching user from database."
            )
        users = response.json()
        return users[0] if users and len(users) else None


async def create_user(email: str, username: str, hashed_password: str):
    async with AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/rest/v1/users",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            },
            json={"email": email, "username": username, "password": hashed_password},
        )
        if response.status_code not in [201, 200]:
            raise HTTPException(
                status_code=500, detail="Error creating user in database."
            )


@router.post("/signup")
async def signup(request: SignupRequest):
    existing_user = await get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")
    hashed_password = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt())
    await create_user(request.email, request.username, hashed_password.decode("utf-8"))
    return {"message": "User created successfully."}


@router.post("/login")
async def login(request: LoginRequest):
    user = await get_user_by_email(request.email)
    print('USER ---------------------------------->', user)
    if not user or not bcrypt.checkpw(request.password.encode("utf-8"), user["password"].encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid email or password.")
    token = jwt.encode({"email": user["email"], "username": user["username"], "id": user["id"]}, JWT_SECRET, algorithm="HS256")
    return {"token": token}

