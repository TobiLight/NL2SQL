#!/usr/bin/env python3
# File: auth.py
# Author: Oluwatobiloba Light
"""Authentication schema"""


from typing import Union
from pydantic import BaseModel


class AuthForm(BaseModel):
    """Auth Schema"""
    name: Union[str, None] = None
    email: str
    password: str
