import os

os.environ["STAGE"] = "dev"  # переменная окружения для dev конфига

from filogram import db  # noqa: E402


pytest_plugins = ["file_service_fixtures", "not_raises"]


def pytest_runtest_teardown(item):
    """Новая БД после каждого теста"""
    db.reset_connection()
