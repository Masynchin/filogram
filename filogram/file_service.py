"""Работа с файлами - сохранение, получение, удаление"""
from itertools import groupby
from typing import NamedTuple, Optional

from . import db
from . import exceptions
from . import templates


class FileModel(NamedTuple):
    """Модель файла.

    Модель представляет как входной файл (созданный из ввода пользователя),
    так и файл полученный из БД.

    Модель имеет 6 полей:
    `file_unique_id` - уникальный ID файла в Telegram
    `file_id`        - ID телеграм-документа для отправления в сообщении
    `owner_id`       - ID пользователя, которому принадлежит данный файл
    `category`       - пользовательская категория файла
    `file_name`      - название файла
    `unique_id`      - ID данного файла в нашей БД (имеется только у файлов,
                       которые мы достали из БД)
    """

    file_unique_id: str
    file_id: str
    owner_id: int
    category: str
    file_name: str
    unique_id: Optional[int] = None

    def __eq__(self, other):
        """Проверка на равенство файлов.

        Сравниваюся поле `file_unique_id`. Так мы можем сравнивать
        файлы ещё не попавшие в БД с теми, которые мы оттуда достали
        (удобно при тестах)
        """
        return self.file_unique_id == other.file_unique_id

    @classmethod
    def from_telegram_document(cls, document, **kwargs):
        """Создание модели из телеграм-документа.

        Создаём модель файла из телеграм-документа и дополнительно
        переданных параметров (тех, которых нет в документе,
        это `owner_id` и `category`).

        !! При создании через документ, у модели нет поля `unique_id`
        """
        file_unique_id = document.file_unique_id
        file_id = document.file_id
        file_name = document.file_name
        return cls(
            file_unique_id=file_unique_id,
            file_id=file_id,
            file_name=file_name,
            **kwargs
        )

    @classmethod
    def from_db_values(cls, row):
        """Создание модели из данных БД.

        Создаём модель файла из данных БД. В этих данных присутствуют
        все поля модели, включая `unique_id`
        """
        named_values = dict(zip(row.keys(), row))
        return cls(**named_values)

    @classmethod
    def db_columns(cls):
        """Название полей для таблицы в БД"""
        return (
            "file_unique_id",
            "file_id",
            "owner_id",
            "category",
            "file_name",
            "unique_id",
        )

    def column_values(self):
        """Значения файла сцеплённые с названием колонок.

        Данные передаются для сохранения в БД, поэтому у модели
        на текущий момент нет поля `unique_id`
        """
        return {
            "file_unique_id": self.file_unique_id,
            "file_id": self.file_id,
            "owner_id": self.owner_id,
            "category": self.category,
            "file_name": self.file_name,
        }


def save_telegram_document(document, user_id, category):
    """Сохранение телеграм-документа.

    Создание файла из переданого Telegram документа - `document`,
    ID пользователя - `user_id` и категории - `category`.
    Далее полученый файл сохраняется в БД
    """
    file = FileModel.from_telegram_document(
        document, owner_id=user_id, category=category
    )
    save_file(file)


def save_file(file):
    """Сохранение файла в БД"""
    column_values = file.column_values()
    try:
        db.insert(column_values)
    except exceptions.IntegrityError:
        raise exceptions.FileAlreadyExists(templates.FILE_ALREADY_EXISTS)


def get_file(unique_id, user_id):
    """Получение конкретного файла.

    Получение файла с ID - `unique_id` у пользователя с ID - `user_id`.
    Если файл не найден, то выбрасывается исключение `IncorrentFileID`
    """
    columns = FileModel.db_columns()
    values = db.fetchone(columns, unique_id=unique_id, owner_id=user_id)
    if not values:
        raise exceptions.IncorrectFileID("Не могу найти файл с таким ID")

    file = FileModel.from_db_values(values)
    return file


def delete_file(unique_id, user_id):
    """Удаление конкретного файла.

    Удаление файла с ID - `unique_id` у пользователя с ID `user_id`.
    Перед удалением файла нужно удостоверится, что пользователь имеет доступ
    к этому файлу, иначе выбрасывается исключение `IncorrectFileID`
    """
    try:
        get_file(unique_id, user_id)
    except exceptions.IncorrectFileID:
        raise
    else:
        db.delete(unique_id=unique_id, owner_id=user_id)


def get_owned_files(user_id):
    """Получение всех файлов пользователя.

    Получение всех файлов пользователя с ID - `user_id`
    """
    columns = FileModel.db_columns()
    values = db.fetchall(columns, owner_id=user_id)
    if not values:
        raise exceptions.NoUserFiles(templates.NO_FILES_UPLOADED_YET)

    files = map(FileModel.from_db_values, values)
    return files


def get_user_categories(user_id):
    """Получение всех категорий файлов пользователя.

    Получение всех категорий файлов пользователя с ID - `user_id`
    """
    categories = db.fetchall(["category"], distinct=True, owner_id=user_id)
    categories = list(map(lambda c: c[0], categories))
    return categories


def group_files_by_category(files):
    """Группировка файлов по их категориям.

    !! Чтобы функция groupby работала корректно, файлы должны
       быть изначально отсортированы. Файлы выбираются из БД
       с сортировкой по полю `category`, поэтому sorted
       делать не надо
    """
    files_grouped_by_category = {
        category: tuple(_files)
        for category, _files in groupby(files, key=lambda f: f.category)
    }
    return files_grouped_by_category


def get_category_files(category, user_id):
    """Получение всех файлов пользователя в данной категории"""
    columns = FileModel.db_columns()
    values = db.fetchall(columns, category=category, owner_id=user_id)
    if not values:
        raise exceptions.NoCategoryFiles(templates.NO_FILES_UPLOADED_YET)

    files = map(FileModel.from_db_values, values)
    return files


def delete_category_files(category, user_id):
    """Удаление всех файлов данной категории у данного пользователя"""
    db.delete(category=category, owner_id=user_id)
