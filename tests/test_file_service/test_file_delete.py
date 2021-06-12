import pytest

from filogram import exceptions
from filogram import file_service


def test_correct_file_deletion(
    create_unique_user,
    create_unique_file,
    get_file_unique_id,
    not_raises,
):
    user = create_unique_user()
    file = create_unique_file(user=user)
    file_service.save_file(file)

    unique_id = get_file_unique_id(file)
    with not_raises(exceptions.IncorrectFileID):
        file_service.delete_file(unique_id=unique_id, user_id=user.id)

    with pytest.raises(exceptions.IncorrectFileID):
        file_service.get_file(unique_id=unique_id, user_id=user.id)


def test_cannot_delete_someone_elses_file(
    create_unique_user,
    create_unique_file,
    get_file_unique_id,
):
    user = create_unique_user()

    another_user = create_unique_user()
    someone_elses_file = create_unique_file(user=another_user)
    file_service.save_file(someone_elses_file)

    unique_id = get_file_unique_id(someone_elses_file)
    with pytest.raises(exceptions.IncorrectFileID):
        file_service.delete_file(unique_id=unique_id, user_id=user.id)
