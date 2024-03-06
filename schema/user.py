#!/usr/bin/env python3
# File: user.py
# Author: Oluwatobiloba Light
"""User Schema"""


from typing import Union
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserAuthentication(BaseModel):
    """User login/signup schema"""
    email: EmailStr = Field(title="Email", description="User email")
    password: str = Field(
        title="Password", description="User password", min_length=6)


class User(BaseModel):
    """User schema"""
    id: UUID = Field(...)
    email: EmailStr = Field(title="Email", description="User email")
    name: Union[str, None] = Field(default=None, title="Name",
                                   description="User name")
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
