#!/usr/bin/env python3
# File: database.py
# Author: Oluwatobiloba Light
"""Database schema"""


from typing import Union
from pydantic import BaseModel, Field
from datetime import datetime


class Database(BaseModel):
    """Database Schema"""
    id: str = Field(...)
    connection_uri: str
    database_name: Union[str, None]
    user_id: str
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class CreateDatabase(BaseModel):
    """Create Database Schema"""
    connection_uri: str = Field(...)
    database_name: str
    database_type: str


class GetDatabase(BaseModel):
    """Get Database Schema"""
    id: str
