#!/usr/bin/env python3
# File: conversation.py
# Author: Oluwatobiloba Light
"""Conversation schema"""


from typing import List, Union
from fastapi import Form
from pydantic import BaseModel, Field
from datetime import datetime


class Conversation(BaseModel):
    id: str = Field(...)
    prompts: Union[List['Prompt'], None] = None
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())



from schema.prompt import Prompt
