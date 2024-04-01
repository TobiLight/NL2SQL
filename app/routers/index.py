#!/usr/bin/env python3
# File: index.py
# Author: Oluwatobiloba Light
"""Index route"""

from fastapi import APIRouter, responses, status

index_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Index"]
)


@index_router.get("/", summary="Homepage")
def home():
    """Homepage/Index route"""
    return responses.JSONResponse(content="Welcome to NL2SQL! 🎉",
                                  status_code=status.HTTP_200_OK)


@index_router.get("/health-check", summary="Check Helth of server")
def health_check():
    """GET /health-check endpoint to check server health"""
    users = []
    return responses.JSONResponse(content={"status": "OK", "message": "Welcome to NL2SQL! 🎉", "users": users},
                                  status_code=status.HTTP_200_OK)
