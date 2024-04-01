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
from app.utils.utils import db_exists
from schema.database import CreateDatabase, Database, GetDatabase
from schema.user import User
from datetime import datetime


database_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Database"],
    prefix="/database"
)


@database_router.get("/all", summary="List of User's Databases")
async def all_db_conn(user: User = Depends(custom_auth)):
    """
    GET /database/all endpoint to retrieve a list of databases associated with
    the authenticated user.

    Args:
        - user (User, optional): The authenticated user. Defaults to the result
        of the custom authentication dependency.

    Returns:
        - responses.JSONResponse: A JSON response containing a list of
        dictionaries with information about each database associated with
        the user.

    Raises:
        - HTTPException: If there is an error retrieving the list of databases
        or if the user is not authenticated.

    Summary:
        This endpoint retrieves a list of databases that belong to the
        authenticated user.
    """
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
async def create_db_conn(database_data: CreateDatabase,
                         user: User = Depends(custom_auth)):
    """
    POST /database/create endpoint to create a new database associated with the
    authenticated user.

    Args:
        - database_data (CreateDatabase): The data required to create the
        new database.
        - user (User, optional): The authenticated user. Defaults to the result
        of the custom authentication dependency.

    Returns:
        - responses.JSONResponse: A JSON response containing information about
        the created database.

    Raises:
        - HTTPException: If there is an error creating the database or if the
        user is not authenticated.

    Summary:
        This endpoint creates a new database associated with the authenticated
        user.
    """
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


@database_router.get("", summary="Get a database connection")
async def get_db_conn(database: GetDatabase, user: User = Depends(custom_auth)):
    """
    Retrieve a database connection associated with the specified database ID.

    Args:
        - database (GetDatabase): The database object containing the ID of the
        database to retrieve.
        - user (User, optional): The authenticated user. Defaults to the result
        of the custom authentication dependency.

    Returns:
        - responses.JSONResponse: A JSON response containing information about
        the requested database connection.

    Raises:
        - HTTPException: If the specified database does not exist or if the
        user is not authenticated.

    Summary:
        This endpoint retrieves a database connection associated with the
        specified database ID.
    """
    db = await db_exists(database.id)

    return responses.JSONResponse(content=jsonable_encoder(db))
