#!/usr/bin/env python3
# File: conversation.py
# Author: Oluwatobiloba Light
"""Conversation route"""


from fastapi import APIRouter, Depends, responses, status
from fastapi.encoders import jsonable_encoder

from app.utils.auth import custom_auth
from schema.conversation import Conversation
from schema.user import User
from app.db import db


conversation_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Conversation"],
    prefix="/conversation"
)


@conversation_router.get("/all", summary="Get list of conversations")
async def get_conversations(user: User = Depends(custom_auth)):
    """"""
    conversation_list = await db.conversation.find_many(
        where={"user_id": str(user.id)}, include={
            "prompts": True
        })

    return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
        "conversations": jsonable_encoder(conversation_list)})


@conversation_router.get("/{conversation_id}", summary="Get a conversation")
async def get_conversation(conversation_id: str,
                           user: User = Depends(custom_auth)):
    """"""
    conversation = await db.conversation.find_first(
        where={
            "id": conversation_id,
            "user_id": str(user.id)},
        include={"prompts": True})

    if not conversation or conversation is None:
        return responses.JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Conversation does not exist!")

    return responses.JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"conversation": jsonable_encoder(conversation)})
