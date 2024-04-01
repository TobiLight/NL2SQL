#!/usr/bin/env python3
# File: db.py
# Author: Oluwatobiloba Light
"""DB Utils"""


from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


def connect_db(conn_uri: str):
    """"""
    engine = create_engine(conn_uri)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    session = sessionmaker(bind=engine)()
    db_name = engine.url.database

    return (session, metadata, db_name)
