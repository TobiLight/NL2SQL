#!/usr/bin/env python3
# File: gquery.py
# Author: Oluwatobiloba Light
"""Google Gemini AI Query module"""

from typing import Any, Dict, List, Union
from app.gemini import chat


def get_applicable_tables_sql(query_text: str, tables: List[str]):
    """"""
    response = chat.send_message(
        """
            You are a helpful assistant that knows a lot about SQL language and manages a database.
            
            The database tables are: {0}.
            
            Answer only with a comma separated list of tables, without any explanation. Example response: '\"users\", \"products\"'
            
            If you think there is a table name that can be used but you aren't sure, please include it anyways.
            
            Tell me which tables from the list of tables {0} you would use to make this query: {1}
        """.format(query_text, tables)
    )

    return response


def generate_sql(query_text: str, table_meta: Dict[str, str], schema: str, db_type: str, history: Union[List[Dict[str, str]], None] = None):
    """"""
    from datetime import datetime
    counter = 0

    if history and history is not None:
        history_str = ""
        for hist in range(len(history)):
            history_str += "Query:\n{}".format(history[hist]["query"])
            history_str += "\n\nResponse:\n{}\n\n".format(
                history[hist]["response"])
            counter += 1

        print(history_str)
        if counter >= 2:
            response = chat.send_message(
                """
                Conversation History:
                ============================================================
                {0}
            
            
                What would be the SQL query command to this question based on the history provided above: {1}.
                
                The database schema is {2} and the database tables are: {3}. 
                
                Do not wrap the SQL command in ```sql ...``` or code blocks or quotes.
                
                In the SQL Query for {4} is "MySQL", DO NOT wrap the table name(s) in quotes. For example: "users" should be users, otherwise do so for if {4} is "PostgreSQL"                      
            """.format(history_str, query_text, schema, table_meta, db_type))
            return response

        response = chat.send_message(
            """
            I have a history of conversations I have had with you. It is a list of dictionary items with "query" and "response" as the keys.
            You will use this history as a reference to respond accurately to user prompts if there is a need for it. I have provided it below:
            
            Conversation History:
            ============================================================
            {0}
            
            The database schema is {2} and the database tables are: {3}. 
            
            What would be the SQL query command to this question based on the history provided above: {1} 
            
            Do not wrap the SQL command in ```sql ...``` or code blocks or quotes.
            
            In the SQL Query for {4} is "MySQL", DO NOT wrap the table name(s) in quotes. For example: "users" should be users, otherwise do so for if {4} is "PostgreSQL"                 
            """.format(history_str, query_text, schema, table_meta, db_type)
        )

        return response

    response = chat.send_message(
        """
        You are a helpful assistant that knows a lot about SQL language and manages a database.
        
        You are using {3} as the database and SQLAlchemy (a python package) as the ORM for operations on the database.
        
        You MUST answer only with a 100% correct {3} query command to execute. Don't include any explanation.
        
        The database schema is {2} and the database tables are: {1}. 
        
        The table is a hashmap of table name as keys and the schemas as values.
                
        What would be the SQL query command to this question: {4}
        
        In the SQL Query for {3}, wrap the key from database tables {1} with '"'. For example: User -> "User". If {3} is "MySQL", DO NOT wrap the table name(s) in quotes. For example: "users" should be users.
        
        DO NOT wrap the SQL command in ```sql ...``` or code blocks or quotes.
        """.format(
            datetime.now().date(), table_meta, schema, db_type, query_text)
    )

    return response


def query_response_to_nl(query_text: str, query_answer: Any):
    """"""
    response = chat.send_message("""
    You will be given a query and the result of executing the query on a database. Try to give a detailed summary of the result in such a way that a non tech-savvy user or even a 10yo would understand easily. 
    
    Your answer must be in natural language and MUST not include any programming verbs (for example: tuple, dict, list, etc) or anything that a non tech-savvy user won't understand.
    
    -----------------------------------------
    Query: {0}
    
    -----------------------------------------
    Result: {1}
    """.format(query_text, query_answer)
    )

    return response
