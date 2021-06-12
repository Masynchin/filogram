import pytest

from filogram import exceptions
from filogram import file_service


def test_correct_user_category_deletion(default_user, create_unique_file):
    user = default_user
    category = "photos"
    for _ in range(3):
        file = create_unique_file(user=user, category=category)
        file_service.save_file(file)

    file_service.delete_category_files(category=category, user_id=user.id)

    with pytest.raises(exceptions.NoUserFiles):
        file_service.get_owned_files(user_id=user.id)


def test_deletion_affects_only_to_exactly_category(
    default_user, create_unique_file
):
    user = default_user
    categories = ["books", "films"]
    for category in categories:
        file = create_unique_file(user=user, category=category)
        file_service.save_file(file)

    file_service.delete_category_files(category="books", user_id=user.id)

    owned_files = list(file_service.get_owned_files(user_id=user.id))
    assert len(owned_files) == 1
    assert owned_files[0].category == "films"


def test_deletion_not_affects_on_other_users(
    create_unique_user, create_unique_file
):
    category = "pictures"

    first_user = create_unique_user()
    first_file = create_unique_file(user=first_user, category=category)
    file_service.save_file(first_file)

    second_user = create_unique_user()
    second_file = create_unique_file(user=second_user, category=category)
    file_service.save_file(second_file)

    second_user_files_before = list(
        file_service.get_owned_files(user_id=second_user.id)
    )

    file_service.delete_category_files(
        category=category, user_id=first_user.id
    )

    second_user_files_after = list(
        file_service.get_owned_files(user_id=second_user.id)
    )
    assert second_user_files_before == second_user_files_after
