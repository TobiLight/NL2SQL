#!/usr/bin/env python3
# File: database.py
# Author: Oluwatobiloba Light
"""Database schema"""

from dataclasses import dataclass
from typing import Union
from typing_extensions import Annotated
from fastapi import Form
from pydantic import BaseModel, Field
from datetime import datetime


class Database(BaseModel):
    id: str = Field(...)
    connection_uri: str
    database_name: Union[str, None]
    user_id: str
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class CreateDatabase(BaseModel):
    connection_uri: str = Field(...)
    database_name: str
    # user_id: str
    database_type: str
