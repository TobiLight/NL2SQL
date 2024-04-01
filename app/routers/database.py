#!/usr/bin/env python3
# File: database.py
# Author: Oluwatobiloba Light
"""Database route"""

from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, responses, status
from fastapi.encoders import jsonable_encoder
from app.db import db
from prisma import errors
from app.utils.auth import custom_auth
from schema.database import CreateDatabase, Database
from schema.user import User
from datetime import datetime


database_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Database"],
    prefix="/database"
)


@database_router.get("/all", summary="List of User's Databases")
async def all_db(user: User = Depends(custom_auth)):
    """"""
    try:
        list_db = await db.databaseconnection.find_many(where={"user_id":
                                                               str(user.id)})

        return responses.JSONResponse(
            content={"databases": jsonable_encoder(list_db)},
            status_code=status.HTTP_200_OK)
    except errors.PrismaError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="An error has occured!")


@database_router.post("/create", summary="Create Database")
async def create_db(database_data: CreateDatabase,
                    user: User = Depends(custom_auth)):
    """"""
    existing_db = await db.databaseconnection.\
        find_first(where={"connection_uri": database_data.connection_uri})

    print(user)

    if existing_db is not None:
        return responses.\
            JSONResponse(content={"status":
                                  "Database connection exists already!"},
                         status_code=status.HTTP_200_OK)

    new_db = await db.databaseconnection.create({
        "id": str(uuid4()),
        "type": database_data.database_type.lower(),
        "connection_uri": database_data.connection_uri,
        'user_id': str(user.id),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })

    db_json = jsonable_encoder(Database(id=new_db.id,
                                        connection_uri=new_db.connection_uri,
                                        database_name=new_db.database_name,
                                        user_id=str(user.id),
                                        created_at=new_db.created_at,
                                        updated_at=new_db.updated_at))

    return responses.JSONResponse(content={"database": db_json},
                                  status_code=status.HTTP_200_OK)
