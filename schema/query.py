#!/usr/bin/env python3
# File: query.py
# Author: Oluwatobiloba Light
"""Query Schema"""


from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field


class QueryPrompt(BaseModel):
    """Query Prompt Schema"""
    query: str
    database_id: Union[str, UUID]
    conversation_id: Union[str, None] = Field(default=None)


class QueryResponse(BaseModel):
    """Query Response Schema"""
    query: str
    response: str
