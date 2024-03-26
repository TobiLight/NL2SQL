#!/usr/bin/env python3
# File: auth.py
# Author: Oluwatobiloba Light
"""Authentication schema"""

from dataclasses import dataclass
from typing import Union
from typing_extensions import Annotated
from fastapi import Form
from pydantic import BaseModel


class AuthForm(BaseModel):
    name: Union[str, None] = None
    email: str
    password: str
