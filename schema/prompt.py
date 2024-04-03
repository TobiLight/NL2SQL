#!/usr/bin/env python3
# File: prompt.py
# Author: Oluwatobiloba Light
"""Prompt schema"""


from pydantic import BaseModel, Field
from datetime import datetime


class Prompt(BaseModel):
    """Prompt Schema"""
    id: str = Field(...)
    query: str
    response: str
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
