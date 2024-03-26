#!/usr/bin/env python3
# File: query.py
# Author: Oluwatobiloba Light
"""Query route"""

from MySQLdb import DatabaseError, OperationalError
from fastapi import APIRouter, Depends, HTTPException, responses, status

from app.utils.auth import custom_auth
from schema.query import QueryPrompt
from schema.user import User
from app.db import db


query_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Query"],
    prefix="/query"
)


@query_router.post("/create", summary="Query NL2SQL")
async def create_prompt(query: QueryPrompt, user: User = Depends(custom_auth)):
    """"""
    def add_quotes_around_table(query):
        # Ensure query is a string
        import re
        if not isinstance(query, str):
            raise ValueError("Input must be a string")

        # Define a regular expression pattern to match schema.table
        pattern = r'(\bpublic\b)\.(\w+)'

        # Use re.sub to replace matches
        modified_query = re.sub(
            pattern, lambda match: f'{match.group(1)}."{match.group(2)}"',
            query)
        return modified_query
    data = {}

    if query.query is None or not query.query:
        return responses.JSONResponse(content="Query cannot be empty!",
                                      status_code=status.HTTP_400_BAD_REQUEST)

    existing_db = await db.databaseconnection.\
        find_unique(where={"id": str(query.database_id)})

    if existing_db is None or not existing_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database does not exist! Consider adding a new database!",
            headers={"Authorization": "Bearer"})

    from sqlalchemy import create_engine, MetaData, text
    from sqlalchemy.orm import sessionmaker

    try:
        engine = create_engine(existing_db.connection_uri)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        session = sessionmaker(bind=engine)()

        table_names = list(metadata.tables.keys())

        print(add_quotes_around_table(str(table_names)))

    except (DatabaseError, OperationalError) as e:
        print("choi", e)

    return responses.JSONResponse(content={}, status_code=status.HTTP_200_OK)
