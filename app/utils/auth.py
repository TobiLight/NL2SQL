#!/usr/bin/env python3
# File: auth.py
# Author: Oluwatobiloba Light

from typing import Any, Dict, Union
from uuid import UUID
from fastapi import Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from schema.user import User
from app.db import db
from os import getenv
from jose import jwt
from prisma import errors


# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
# REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
# JWT_REFRESH_SECRET_KEY = "kjhgfghjk"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using a secure hashing algorithm.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The hashed representation of the input password.
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """
    Verify whether a given plain-text password matches a hashed password.

    Args:
        password (str): The plain-text password to be verified.
        hashed_pass (str): The hashed password for comparison.

    Returns:
        bool: True if the plain-text password matches the hashed password,
        False otherwise.
    """
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict, expires_delta:
                        Union[timedelta, None] = None) -> str:
    """"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=2)

    to_encode.update({"exp": expire})

    encoded_jwt = None

    SECRET_KEY = getenv("JWT_SECRET_KEY")

    if SECRET_KEY is None:
        raise Exception("🚨 JWT SECRET KEY NOT SET")
    else:
        encoded_jwt = jwt.encode(
            to_encode, key=SECRET_KEY, algorithm=getenv("JWT_ALGORITHM") or "HS256")

    return encoded_jwt


def verify_access_token(request: Request) -> Union[dict, None]:
    """"""
    SECRET_KEY = getenv("JWT_SECRET_KEY")

    token: str

    authorization = request.headers.get("Authorization")

    if authorization is None:
        return None

    authorization = authorization.split()

    if len(authorization) < 2:
        return None

    token = authorization[1]

    if SECRET_KEY is None:
        raise Exception("🚨 JWT SECRET KEY NOT SET")

    try:
        payload = jwt.decode(token, key=SECRET_KEY,
                             algorithms=getenv("JWT_ALGORITHM") or "HS256")
        return payload
    except JWTError as e:
        print("🚨 Token Error:", e)

    return None


async def custom_auth(payload: Dict[str, Any] = Depends(verify_access_token)) -> User:
    """"""
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized!",
                            headers={"Authorization": "Bearer"})

    user = await db.user.find_unique(where={"email": payload["sub"]})

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized!",
                            headers={"Authorization": "Bearer"})

    return User(id=user.id, email=user.email,
                name=user.name,
                created_at=user.created_at,
                updated_at=user.updated_at)
