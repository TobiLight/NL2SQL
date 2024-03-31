#!/usr/bin/env python3
# File: query.py
# Author: Oluwatobiloba Light
"""Query route"""

from MySQLdb import DatabaseError, OperationalError, ProgrammingError
from fastapi import APIRouter, Depends, HTTPException, responses, status
from fastapi.encoders import jsonable_encoder
from app.utils.auth import custom_auth
from app.utils.gquery import generate_sql, get_applicable_tables_sql, query_response_to_nl
from schema.query import QueryPrompt
from schema.user import User
from app.db import db
from app.gemini import model, chat
from uuid import uuid4


query_router = APIRouter(
    responses={404: {'description': "Not found!"}}, tags=["Query"],
    prefix="/query"
)


@query_router.post("/create", summary="Query NL2SQL")
async def create_prompt(query: QueryPrompt, user: User = Depends(custom_auth)):
    """"""
    conversation_id = query.conversation_id
    conversation = None

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

    # current_user = await db.user.find_first(where={"email": user.email})
    if not conversation_id or conversation_id is None:
        conversation = await db.conversation.create(data={
            "id": str(uuid4()),
            "user_id": str(user.id),
        }, include={"prompts": True})

        conversation_id = conversation.id
    else:
        conversation = await db.conversation.\
            find_unique(where={"id": conversation_id}, include={
                        "user": True, "prompts": True})

        if conversation:
            conversation_id = conversation.id
        else:
            print("creating a new one")
            conversation = await db.conversation.create(data={
                "id": str(uuid4()),
                "user_id": str(user.id),
            }, include={"prompts": True})

            conversation_id = conversation.id

    from sqlalchemy import create_engine, MetaData, text
    from sqlalchemy.orm import sessionmaker

    try:
        # connect to database
        engine = create_engine(existing_db.connection_uri)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        session = sessionmaker(bind=engine)()

        if "show tables" in query.query.lower():
            sql_result = session.execute(text(
                "SHOW TABLES;")).all()
            db_name = engine.url.database

            response = query_response_to_nl(
                "I want the list of table names of this database: {}".format(db_name), sql_result).text

            return responses.JSONResponse(content={"response": response})

        # get db_tables from database
        db_tables = list(metadata.tables.keys())

        # get applicable tables generated from gemini
        applicable_tables = get_applicable_tables_sql(
            query.query, db_tables).text

        # check database type
        if existing_db.type is not None:
            db_type = existing_db.type.lower()

            if db_type == 'postgresql':
                # get table name and the table from database tables
                for table_name, table in metadata.tables.items():
                    # Extract column names
                    column_names = [
                        column.name for column in table.columns]

                    # Store in the dictionary
                    data[table_name] = column_names

                sql_command: str = ""

                if conversation and conversation.prompts is not None:
                    prompts_data = []
                    prompts_data_obj = {}
                    for l in range(len(conversation.prompts)):
                        prompts_data_obj["query"] = conversation.prompts[l].query
                        prompts_data_obj["response"] = conversation.prompts[l].response
                        prompts_data.append(prompts_data_obj)

                    sql_command = generate_sql(
                        query.query, data, "'public'", "PostgreSQL", history=prompts_data).text
                    print("has history")
                else:
                    sql_command = generate_sql(
                        query.query, data, "'public'", "PostgreSQL").text

                # sanitize the query
                if ("```sql" in str(sql_command)[:6]):
                    print("yes, ```sql")
                    sql_command = str(sql_command)[6:]

                if "```" in str(sql_command)[:3]:
                    print("yes, ```")
                    sql_command = str(sql_command)[3:]

                if "```" in str(sql_command)[-3:]:
                    print("yes, ``` back")
                    sql_command = str(sql_command)[:-3]

                sql_query = text(sql_command)

                print("cleaned_sql", sql_query)

                try:
                    sql_result = session.execute(text(str(sql_query))).all()

                    response = query_response_to_nl(
                        query.query, sql_result).text
                    print(response, conversation)

                    # save the response to prompts
                    await db.prompt.create({
                        "id": str(uuid4()),
                        "conversation_id": conversation.id,
                        "query": query.query,
                        "response": response,
                    })

                    conversation = await db.conversation.find_first(where={"id": conversation_id}, include={"prompts": True})

                    # return conversation: includes user query and response
                    return responses.JSONResponse(content={"response": jsonable_encoder(conversation)})
                except () as e:
                    # print("error", e)
                    # print(session.execute(text(str(sql_query))).all())
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="An error has occured while querying the database! Please try again :)")
            else:
                # get table name and the table from database tables
                for table_name, table in metadata.tables.items():
                    # Extract column names
                    column_names = [
                        column.name for column in table.columns]

                    # Store in the dictionary
                    data[table_name] = column_names

                sql_command: str = ""

                if conversation and conversation.prompts is not None:
                    prompts_data = []
                    prompts_data_obj = {}
                    for l in range(len(conversation.prompts)):
                        prompts_data_obj["query"] = conversation.prompts[l].query
                        prompts_data_obj["response"] = conversation.prompts[l].response
                        prompts_data.append(prompts_data_obj)

                    sql_command = generate_sql(
                        query.query, data, "'public'", "MySQL", history=prompts_data).text
                    print("has history")
                else:
                    sql_command = generate_sql(
                        query.query, data, "'public'", "MySQL").text

                # sanitize the query
                if ("```sql" in str(sql_command)[:6]):
                    print("yes, ```sql")
                    sql_command = str(sql_command)[6:]

                if "```" in str(sql_command)[:3]:
                    print("yes, ```")
                    sql_command = str(sql_command)[3:]

                if "```" in str(sql_command)[-3:]:
                    print("yes, ``` back")
                    sql_command = str(sql_command)[:-3]

                sql_query = text(sql_command)

                print("cleaned_sql", sql_query)

                try:
                    sql_result = session.execute(
                        text(str(sql_query))).all()

                    response = query_response_to_nl(
                        query.query, sql_result).text

                    # save the response to prompts
                    await db.prompt.create({
                        "id": str(uuid4()),
                        "conversation_id": conversation.id,
                        "query": query.query,
                        "response": response,
                    })

                    conversation = await db.conversation.find_first(where={"id": conversation_id}, include={"prompts": True})

                    # return conversation: includes user query and response
                    return responses.JSONResponse(content={"response": jsonable_encoder(conversation)})
                except (ProgrammingError, ) as e:
                    # print("error", e)
                    # print(session.execute(text(str(sql_query))).all())
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="An error has occured while querying the database! Please try again :)")

    except (DatabaseError, OperationalError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error has occured while querying the database! Please try again :)")

    return responses.JSONResponse(content={}, status_code=status.HTTP_200_OK)
