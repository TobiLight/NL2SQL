#!/usr/bin/env python3
# File: auth.py
# Author: Oluwatobiloba Light
"""Auth module"""


from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request, responses, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from app.utils.auth import create_access_token, hash_password, \
    verify_access_token, verify_password
from app.utils.utils import is_email
from schema.auth import AuthForm
from app.db import db
from uuid import uuid4
from schema.user import User
from datetime import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(
    responses={404: {'description': "URL not found!"}},
    tags=["User authentication & authorization"],
    prefix="/auth"
)


@auth_router.post("/login", summary="User login",
                  response_model_exclude_none=True)
async def login(form_data: AuthForm):
    """POST /auth/login endpoint to sign in a user"""
    email = form_data.email
    password = form_data.password

    is_email(email)

    user = await db.user.find_unique(where={"email": email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login!",
            headers={"WWW-Authenticate": "Bearer"})

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login!",
            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=60*12)

    token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)

    user = jsonable_encoder(User(id=user.id, email=user.email))

    return responses.JSONResponse(content={"user": user,
                                           "access_token": token})


@auth_router.post("/create", summary="Create a new user",
                  response_model_exclude_none=True)
async def create_user(form_data: AuthForm):
    """
    POST /auth/create endpoint to create a new user
    """
    name = form_data.name
    email = form_data.email
    password = form_data.password

    is_email(email)

    if len(password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password must 6 or more characters!")

    existing = await db.user.find_unique(where={"email": email})

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already exists")

    hashed_password = hash_password(password)

    new_user = jsonable_encoder({
        "id": str(uuid4()),
        "name": name,
        "email": email,
        "password": hashed_password,
        # "created_at": datetime.now(),
        # "updated_at": datetime.now()
    })

    await db.user.create(data=new_user)

    del new_user['password']

    return responses.JSONResponse(content={"message": "User created!",
                                           "user": new_user},
                                  status_code=status.HTTP_201_CREATED)


@auth_router.get("/user/me", summary="Get a user")
async def get_user(request: Request):
    """GET /user/me endpoint to get a user's info"""
    valid_token = verify_access_token(request)

    if valid_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    user = await db.user.find_unique(where={"email": valid_token["sub"]})

    if user is None or not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    user_json = jsonable_encoder(
        User(id=user.id, email=user.email, created_at=user.created_at,
             updated_at=user.updated_at))

    return responses.JSONResponse(content={**user_json})
