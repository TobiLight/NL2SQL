#!/usr/bin/env python3
# File: query.py
# Author: Oluwatobiloba Light
"""Query route"""

from MySQLdb import DatabaseError, OperationalError
from fastapi import APIRouter, Depends, HTTPException, responses, status
from app.utils.auth import custom_auth
from app.utils.gquery import query_response_to_nl
from app.utils.utils import conversation_exists_or_create, db_exists, run_query
from schema.query import QueryPrompt
from schema.user import User


query_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Query"],
    prefix="/query"
)


@query_router.post("/create", summary="Query NL2SQL")
async def create_prompt(query: QueryPrompt, user: User = Depends(custom_auth)):
    """
    POST /query/create endpoint to create a new prompt for NL2SQL query.

    Args:
        query (QueryPrompt): The NL2SQL query prompt to be created.
        user (User, optional): The authenticated user. Defaults to the result
        of the custom authentication dependency.

    Returns:
        - responses.JSONResponse: A dict as JSON response containing
        information about the created prompt.

    Raises:
        HTTPException: If there is an error creating the prompt or if the user
        is not authenticated.

    Summary:
        This endpoint creates a new NL2SQL query prompt. The user must be
        authenticated to create a prompt.
    """
    if query.query is None or not query.query:
        return responses.JSONResponse(content="Query cannot be empty!",
                                      status_code=status.HTTP_400_BAD_REQUEST)

    existing_db = await db_exists(str(query.database_id))

    [_, conversation] = await conversation_exists_or_create(
        query.conversation_id, str(user.id))

    from sqlalchemy import text
    from app.utils.db import connect_db

    try:
        # connect to database
        db_info = connect_db(existing_db.connection_uri)
        [session, _, db_name] = db_info

        if "show tables" in query.query.lower():
            if existing_db.type is not None and\
                    existing_db.type == 'postgresql':
                sql_result = session.execute(text(
                    "SELECT table_name FROM information_schema.tables\
                        WHERE table_schema = 'public' AND table_type\
                            = 'BASE TABLE';")).all()

                response = query_response_to_nl(
                    "I want the list of table names of this database: {}"
                    .format(db_name), sql_result).text

                return responses.JSONResponse(content={"response": response})

            sql_result = session.execute(text(
                "SHOW TABLES;")).all()

            response = query_response_to_nl(
                "I want the list of table names of this database: {}"
                .format(db_name), sql_result).text

            return responses.JSONResponse(content={"response": response})

        # check database type
        if existing_db.type is not None:
            db_type = existing_db.type.lower()

            return await run_query(db_type, conversation, query.query,
                                   existing_db.connection_uri)

    except (DatabaseError, OperationalError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error has occured while connecting the database!\
                Please try again :)")
