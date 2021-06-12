import pytest

from filogram import exceptions
from filogram import file_service


def test_correct_no_owned_files(create_unique_user, create_unique_file):
    user = create_unique_user()

    with pytest.raises(exceptions.NoUserFiles):
        file_service.get_owned_files(user_id=user.id)

    another_user = create_unique_user()
    another_file = create_unique_file(user=another_user)
    file_service.save_file(another_file)

    with pytest.raises(exceptions.NoUserFiles):
        file_service.get_owned_files(user_id=user.id)


def test_correct_owned_files(create_unique_user, create_unique_file):
    first_user = create_unique_user()
    second_user = create_unique_user()

    our_file = create_unique_file(user=first_user)
    other_file = create_unique_file(user=second_user)

    file_service.save_file(our_file)
    file_service.save_file(other_file)

    owned_files = list(file_service.get_owned_files(first_user.id))

    assert our_file in owned_files
    assert other_file not in owned_files
