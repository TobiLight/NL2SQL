#!/usr/bin/env python3
# File: utils.py
# Author: Oluwatobiloba Light
"""Utils module"""


import re
from typing import Union
from fastapi import HTTPException, Request, status


def get_token_from_header(request: Request) -> Union[str, None]:
    """"""
    token: str = ""
    header_token: Union[str, None] = request.headers.get("Authorization")

    if not header_token:
        return None

    if type(header_token) == str and len(header_token) < 2:
        return None

    token = header_token
    token = token.split()[1] if len(token.split()) > 1 else ""
    print("token", token)
    return token


def is_email(email):
    """"""
    email_regex = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"

    if not re.match(email_regex, email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid email!")
    return True
