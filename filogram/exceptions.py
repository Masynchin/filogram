"""Собственные исключения"""


class IncorrectFileID(Exception):
    """Передан неверный ID файла"""


class IntegrityError(Exception):
    """Алиас для sqlite3.IntegrityError"""


class FileAlreadyExists(IntegrityError):
    """Передаваемый файл уже находится в БД"""


class NoUserFiles(Exception):
    """У пользователя нет файлов"""


class NoCategoryFiles(Exception):
    """У пользователя нет файлов данной категории"""
