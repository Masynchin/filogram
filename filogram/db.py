"""Функции для прямой работы с БД"""
from contextlib import contextmanager
import sqlite3

from . import exceptions
from .config import config
from .logger import logger


conn = None


@contextmanager
def get_cursor():
    """Получение курсора для выполнения запроса к БД.

    Если во время запроса произошла ошибка sqlite3.IntegrityError,
    то прокидываем исключение наверх. Если возникла другая ошибка, то логируем
    """
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
    """Добавляем данные в БД"""
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
    """
    Декоратор для перехвата ошибки `sqlite3.IntegrityError`
    с заменой на нашу `exceptions.IntegrityError`
    """
    try:
        yield
    except sqlite3.IntegrityError as e:
        raise exceptions.IntegrityError from e


def fetchone(columns, distinct=False, **conditions):
    """Получаем одну запись из БД"""
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
    """Получаем все записи из БД"""
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
    """Удаляем запись из БД"""
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
    """Создаён из именованых аргументов WHERE условие для sqlite3"""
    condition_query = " AND ".join(f"{key} = ?" for key in conditions)
    condition_values = tuple(conditions.values())
    return (condition_query, condition_values)


def reset_connection():
    """Закрываем текущее соединение и устаналиваем новое.

    Функция используется только при тестах для получения корректный ID записей
    """
    close_connection()
    _set_connection()


def close_connection():
    """Закрываем соединение к БД"""
    conn.close()


def _set_connection():
    """Устанавливаем соединение к БД"""
    global conn

    conn = sqlite3.connect(config.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    _init_db()


def _init_db():
    """Инициализация БД из скрипта"""
    with open(config.CREATE_DB_SCRIPT_PATH) as f, get_cursor() as cursor:
        script = f.read()
        cursor.executescript(script)


_set_connection()
