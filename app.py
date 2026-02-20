from flask import Flask,request, jsonify
import requests

from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ---- Models ----
class User(BaseModel):
    id: int
    name: str

class CreateUserRequest(BaseModel):
    user_id: int
    name: str

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    new_user_id: Optional[int] = None  # optional (usually not recommended)

# ---- Global in-memory store (per process) ----
users_by_id: Dict[int, User] = {}


@app.post("/create_user", status_code=201)
def create_user(payload: CreateUserRequest):
    if payload.user_id in users_by_id:
        raise HTTPException(status_code=409, detail=f"User with id={payload.user_id} already exists.")

    user = User(id=payload.user_id, name=payload.name)
    users_by_id[user.id] = user
    return {"created": user, "total_users": len(users_by_id)}

@app.get("/users")
def list_users():
    return list(users_by_id.values())



@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = users_by_id.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



    