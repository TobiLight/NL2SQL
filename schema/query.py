#!/usr/bin/env python3
# File: query.py
# Author: Oluwatobiloba Light
"""Query Schema"""

from enum import Enum
from typing import Union
from uuid import UUID
from fastapi import Form
from pydantic import BaseModel, Field


class QueryPrompt(BaseModel):
    query: str
    database_id: Union[str, UUID]
    conversation_id: Union[str, None] = Field(default=None)


class QueryResponse(BaseModel):
    query: str
    response: str


# class DatabaseConnection(BaseModel):
#     database_type: DatabaseType
#     uri: Union[str, None]
#     database_name: Union[str, None]

#     @classmethod
#     def as_form(cls, database_type: DatabaseType = Form(...), uri: str = Form(...)):
#         return cls(database_type=database_type,
#                    uri=uri)

#     class Config:
#         orm_mode = True
