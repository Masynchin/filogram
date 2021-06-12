"""Функции для прямой работы с БД"""
from contextlib import contextmanager
import sqlite3

from . import exceptions
from .config import config
from .logger import logger


conn = None


@contextmanager
def get_cursor():
    try:
        cursor = conn.cursor()
        yield cursor
    except sqlite3.IntegrityError:
        conn.rollback()
        raise
    except sqlite3.Error:  # pragma: no cover
        conn.rollback()
        if config.LOG_DB_ERRORS:
            logger.exception("DB exception occured!")
    else:
        conn.commit()


def insert(column_values):
    columns = ",".join(column_values.keys())
    placeholders = ",".join("?" * len(column_values))
    values = tuple(column_values.values())

    with catch_integrity():
        with get_cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO files({columns})
                VALUES ({placeholders})
                """,
                values,
            )


@contextmanager
def catch_integrity():
    try:
        yield
    except sqlite3.IntegrityError as e:
        raise exceptions.IntegrityError from e


def fetchone(columns, distinct=False, **conditions):
    columns = ",".join(columns)
    distinct_query = "DISTINCT" if distinct else ""
    condition_query, condition_values = _create_condition(**conditions)

    with get_cursor() as cursor:
        cursor.execute(
            f"""
            SELECT {distinct_query} {columns}
            FROM files
            WHERE {condition_query}
            """,
            condition_values,
        )
        return cursor.fetchone()


def fetchall(columns, distinct=False, **conditions):
    columns = ",".join(columns)
    distinct_query = "DISTINCT" if distinct else ""
    condition_query, condition_values = _create_condition(**conditions)

    with get_cursor() as cursor:
        cursor.execute(
            f"""
            SELECT {distinct_query} {columns}
            FROM files
            WHERE {condition_query}
            ORDER BY category
            """,
            condition_values,
        )
        return cursor.fetchall()


def delete(**conditions):
    condition_query, condition_values = _create_condition(**conditions)

    with get_cursor() as cursor:
        cursor.execute(
            f"""
            DELETE FROM files
            WHERE {condition_query}
            """,
            condition_values,
        )


def _create_condition(**conditions):
    condition_query = " AND ".join(f"{key} = ?" for key in conditions)
    condition_values = tuple(conditions.values())
    return (condition_query, condition_values)


def reset_connection():
    close_connection()
    _set_connection()


def close_connection():
    conn.close()


def _set_connection():
    global conn

    conn = sqlite3.connect(config.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    _init_db()


def _init_db():
    with open(config.CREATE_DB_SCRIPT_PATH) as f, get_cursor() as cursor:
        script = f.read()
        cursor.executescript(script)


_set_connection()
