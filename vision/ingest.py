import os
from pathlib import Path
from click import echo
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
)
from sqlalchemy.pool import NullPool

DB_CONFIG_DICT = {
        'user': 'postgres',
        'password': '1234',
        'host': 'localhost',
        'port': 5432,
}

DB_CONN_FORMAT = "postgresql://{user}:{password}@{host}:{port}/{database}"

DB_CONN_URL_DEFAULT = (DB_CONN_FORMAT.format(
    database='postgres',
    **DB_CONFIG_DICT))

engine_default = create_engine(DB_CONN_URL_DEFAULT, echo=True)

NEW_DB_NAME = 'testvision'

DB_CONN_URL_NEW = (DB_CONN_FORMAT.format(
    database=NEW_DB_NAME,
    **DB_CONFIG_DICT))

metadata = MetaData()

proj = Table('test', metadata, Column('id', Integer))

def setup_module():
    conn = engine_default.connect()
    conn.execute("COMMIT")
    # Do not substitute user-supplied database names here.
    conn.execute("CREATE DATABASE %s" % NEW_DB_NAME)
    conn.close()

def test_create_table():
    # Get a new engine for the just-created database and create a table.
    engine_new = create_engine(DB_CONN_URL_NEW, poolclass=NullPool)
    conn = engine_new.connect()
    metadata.create_all(conn)
    conn.close()

setup_module()
test_create_table()