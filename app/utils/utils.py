#!/usr/bin/env python3
# File: utils.py
# Author: Oluwatobiloba Light
"""Utils module"""


import re
from typing import Tuple, Union
from uuid import uuid4
from MySQLdb import ProgrammingError
from fastapi import HTTPException, Request, responses, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import MetaData
from app.db import db
from app.utils.db import connect_db
from app.utils.gquery import generate_sql, query_response_to_nl
from schema.conversation import Conversation
from sqlalchemy import text


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


def sanitize_sql_query(sql_cmd: str):
    """"""
    if ("```sql" in str(sql_cmd)[:6]):
        print("yes, ```sql")
        sql_cmd = str(sql_cmd)[6:]

    if "```" in str(sql_cmd)[:3]:
        print("yes, ```")
        sql_cmd = str(sql_cmd)[3:]

    if "```" in str(sql_cmd)[-3:]:
        print("yes, ``` back")
        sql_cmd = str(sql_cmd)[:-3]

    sql_query = text(sql_cmd)

    return sql_query


def is_email(email):
    """"""
    email_regex = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"

    if not re.match(email_regex, email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid email!")
    return True


async def db_exists(db_id: str, user_id: str):
    """"""
    existing_db = await db.databaseconnection\
        .find_first(where={"id": db_id, "user_id": user_id})

    if existing_db is None or not existing_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="""Database does not exist for this user!
            Consider adding a new database!""",
            headers={"Authorization": "Bearer"})

    return existing_db


async def conversation_exists_or_create(convo_id: Union[str, None],
                                        user_id: str) -> Tuple[str,
                                                               Conversation]:
    """"""
    if not convo_id or convo_id is None:
        conversation = await db.conversation.create(data={
            "id": str(uuid4()),
            "user_id": user_id,
        }, include={"prompts": True})

        convo_id = conversation.id
    else:
        conversation = await db.conversation.\
            find_unique(where={"id": convo_id}, include={
                        "user": True, "prompts": True})

        if conversation:
            convo_id = conversation.id
        else:
            conversation = await db.conversation.create(data={
                "id": str(uuid4()),
                "user_id": user_id,
            }, include={"prompts": True})

            convo_id = conversation.id

    convo = jsonable_encoder(conversation)

    return (convo_id, Conversation(id=conversation.id, prompts=convo['prompts']))


async def run_query(db_type: str, conversation: Conversation, query: str,
                    conn_uri: str):
    """"""
    [session, metadata, _] = connect_db(conn_uri)

    data = {}

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

        for prompt in range(len(conversation.prompts)):
            prompts_data_obj["query"] =\
                conversation.prompts[prompt].query

            prompts_data_obj["response"] =\
                conversation.prompts[prompt].response

            prompts_data.append(prompts_data_obj)

        sql_command = generate_sql(
            query, data, "'public'", "PostgreSQL"
            if db_type.lower() == 'PostgreSQL'.lower() else "MySQL",
            history=prompts_data).text
    else:
        sql_command = generate_sql(
            query, data, "'public'", "PostgreSQL"
            if db_type.lower() == 'PostgreSQL'.lower() else "MySQL").text

    # print("unsanitized sql", sql_command)
    sanitize_sql_query(str(sql_command))

    sql_query = text(sql_command)

    # print("cleaned_sql", sql_query)

    try:
        sql_result = session.execute(text(str(sql_query))).all()

        response = query_response_to_nl(
            query, sql_result).text

        # save the response to prompts
        await db.prompt.create({
            "id": str(uuid4()),
            "conversation_id": conversation.id,
            "query": query,
            "response": response,
        })

        convo = await db.conversation.find_first(where={"id": conversation.id}, include={"prompts": True})

        # return conversation: includes user query and response
        return responses.JSONResponse(content={"response": jsonable_encoder(convo)})
    except (ProgrammingError) as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error has occured while querying the database! Please try again :)")
