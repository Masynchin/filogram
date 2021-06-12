"""Конфиги для запуска бота с определёнными настройками"""
import os
from pathlib import Path
from typing import Union


class Config:
    """Родительский класс для конфигов.

    Переопределяемые параметры обозначены аннотациями типов.
    Непереопределяемые параметры имеют значение, и не должны переопределятся
    """

    DATABASE_URL: Union[Path, str]
    LOG_DB_ERRORS: bool

    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CREATE_DB_SCRIPT_PATH = Path(".").joinpath("filogram/createdb.sql")
    LOGS_PATH = Path(".").joinpath("logs/log.log")


class ProdConfig(Config):
    """Конфиг для запуска в продакшене"""

    DATABASE_URL = Path(".").joinpath("db.sqlite3")
    LOG_DB_ERRORS = False


class DevConfig(Config):
    """Конфиг для запуска при разработке"""

    DATABASE_URL = ":memory:"
    LOG_DB_ERRORS = True


stage = os.getenv("STAGE")
if stage == "prod":
    config = ProdConfig()
elif stage == "dev":
    config = DevConfig()
