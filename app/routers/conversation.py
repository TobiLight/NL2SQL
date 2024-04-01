#!/usr/bin/env python3
# File: conversation.py
# Author: Oluwatobiloba Light
"""Conversation route"""


from fastapi import APIRouter, responses, status


conversation_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Conversation"]
)


@conversation_router.get("/conversations", summary="Get list of conversations")
def get_conversations():
    """"""

    return responses.JSONResponse(status_code=status.HTTP_200_OK, content={})
