import pytest

from filogram import exceptions
from filogram import file_service


def test_correct_get_file(
    default_file,
    default_user,
    get_file_unique_id,
):
    file_service.save_file(default_file)
    unique_id = get_file_unique_id(default_file)

    same_file = file_service.get_file(
        unique_id=unique_id,
        user_id=default_user.id,
    )

    assert default_file == same_file


def test_cannot_get_someone_elses_files(
    create_unique_user,
    create_unique_file,
    get_file_unique_id,
):
    user = create_unique_user()

    other_user = create_unique_user()
    someone_elses_file = create_unique_file(user=other_user)
    file_service.save_file(someone_elses_file)

    unique_id = get_file_unique_id(someone_elses_file)
    with pytest.raises(exceptions.IncorrectFileID):
        file_service.get_file(unique_id=unique_id, user_id=user.id)
