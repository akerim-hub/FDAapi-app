from flask import Flask,request, jsonify
import requests

from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Models
class User(BaseModel):
    id: int
    name: str

class CreateUserRequest(BaseModel):
    user_id: int
    name: str

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    new_user_id: Optional[int] = None

class CreateNoteRequest(BaseModel):
    text: str

# Global in-memory stores (per process)
users_by_id: Dict[int, User] = {}
# Dictionary to map user_id to a list of their notes
notes_by_user_id: Dict[int, List[str]] = {} 


# User Endpoints

@app.post("/create_user", status_code=201)
def create_user(payload: CreateUserRequest):
    # Check if ID already exists
    if payload.user_id in users_by_id:
        raise HTTPException(status_code=409, detail=f"User with id={payload.user_id} already exists.")

    # Check if Username already exists, if it does return 409
    for existing_user in users_by_id.values():
        if existing_user.name == payload.name:
            raise HTTPException(status_code=409, detail=f"Username '{payload.name}' already exists.")

    # Create user and initialize their notes list
    user = User(id=payload.user_id, name=payload.name)
    users_by_id[user.id] = user
    notes_by_user_id[user.id] = [] 
    
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


# Notes Endpoints

@app.post("/users/{user_id}/notes", status_code=201)
def add_note(user_id: int, payload: CreateNoteRequest):
    # Ensure the user exists before adding a note
    if user_id not in users_by_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    notes_by_user_id[user_id].append(payload.text)
    return {"message": "Note added successfully"}

@app.get("/users/{user_id}/notes")
def get_notes(user_id: int):
    # Ensure the user exists before retrieving notes
    if user_id not in users_by_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"user_id": user_id, "notes": notes_by_user_id[user_id]}
