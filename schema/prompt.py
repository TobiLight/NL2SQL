#!/usr/bin/env python3
# File: prompt.py
# Author: Oluwatobiloba Light
"""Prompt schema"""

from dataclasses import dataclass
from typing import Union
from typing_extensions import Annotated
from fastapi import Form
from pydantic import BaseModel, Field
from datetime import datetime


class Prompt(BaseModel):
    id: str = Field(...)
    query: str
    response: str
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
