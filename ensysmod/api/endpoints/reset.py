from typing import List, Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import sqlite3

from ensysmod.database import init_db

router = APIRouter()


@router.get("/", response_class=JSONResponse)
def reset_database() -> Dict[str, str]:
    """
        Hard reset all of the contained data in the database
    """
    DB_PATH = r"/Users/felixarjuna/sciebo/HiWi Felix/Arbeit/EnSysMod/ensysmod/local.db"
    conn = create_connection_locally(DB_PATH)
    with conn:
        tables = print_all_tables(conn)
        for table in tables:
            delete_table(conn, table[0])

    # Recreate the template database
    init_db.check_connection()
    init_db.create_all()

    return {"reset": "successful"}


def create_connection_locally(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(e)

    return conn


def print_all_tables(conn):
    cur = conn.cursor()
    table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

    print(table_list, sep='\n')

    return table_list


def delete_table(conn, table):
    cur = conn.cursor()

    try:
        cur.execute("DROP TABLE %s" % table)
    except sqlite3.Error as e:
        print(e)

