from typing import NamedTuple

import pytest

from filogram import file_service


class TelegramDocumentModel(NamedTuple):
    """Модель телеграм-документа для тестов.

    Представляет документ, передаваемый в сообщении пользователя.
    Поля `file_id` и `file_name` имеют значение по умолчанию так как
    присутствуют в телеграм-документе, но не имеют значения при
    сравнении файлов
    """

    file_unique_id: str
    file_id = "file_id"
    file_name = "file_name"


class TelegramUserModel(NamedTuple):
    """Модель телеграм-пользователя для тестов.

    Представялет объект пользователя, отправившего сообщение
    """

    id: int


@pytest.fixture(scope="function")
def get_file_unique_id():
    unique_id = 0

    def _get_file_unique_id(file=None):
        nonlocal unique_id
        unique_id += 1
        return unique_id

    return _get_file_unique_id


@pytest.fixture
def create_document():
    def _create_document(file_unique_id="0"):
        document = TelegramDocumentModel(file_unique_id=file_unique_id)
        return document

    return _create_document


@pytest.fixture
def create_unique_document(create_document):
    file_unique_id = 0

    def _create_unique_document():
        nonlocal file_unique_id

        file_unique_id += 1

        document = create_document(file_unique_id=str(file_unique_id))
        return document

    return _create_unique_document


@pytest.fixture
def default_document(create_document):
    document = create_document()
    return document


@pytest.fixture
def create_user():
    def _create_user(user_id=0):
        user = TelegramUserModel(id=user_id)
        return user

    return _create_user


@pytest.fixture
def create_unique_user(create_user):
    user_id = 0

    def _create_unique_user():
        nonlocal user_id
        user_id += 1

        return create_user(user_id=user_id)

    return _create_unique_user


@pytest.fixture
def default_user(create_user):
    user = create_user()
    return user


@pytest.fixture
def create_unique_category():
    category = "category"

    def _create_unique_category():
        nonlocal category
        category += "category"

        return category

    return _create_unique_category


@pytest.fixture
def default_category(create_unique_category):
    return create_unique_category()


@pytest.fixture
def create_file(default_document, default_user, default_category):
    def _create_file(
        document=default_document,
        user=default_user,
        category=default_category,
    ):
        file = file_service.FileModel.from_telegram_document(
            document, owner_id=user.id, category=category
        )
        return file

    return _create_file


@pytest.fixture
def create_unique_file(
    create_file,
    create_unique_document,
    create_unique_user,
    create_unique_category,
):
    def _create_unique_file(document=None, user=None, category=None):
        document = document or create_unique_document()
        user = user or create_unique_user()
        category = category or create_unique_category()

        file = create_file(document, user, category)
        return file

    return _create_unique_file


@pytest.fixture
def default_file(create_file):
    file = create_file()
    return file
