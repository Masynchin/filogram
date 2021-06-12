import pytest

from filogram import exceptions
from filogram import file_service


def test_correct_get_category_files(default_user, create_unique_file):
    user = default_user
    category = "books"
    file = create_unique_file(user=user, category=category)
    file_service.save_file(file)

    files = list(
        file_service.get_category_files(category=category, user_id=user.id)
    )

    assert len(files) == 1
    assert files[0].category == "books"


def test_affects_only_to_exact_category(default_user, create_unique_file):
    user = default_user
    categories = ["photos", "videos"]
    for category in categories:
        file = create_unique_file(user=user, category=category)
        file_service.save_file(file)

    files = list(
        file_service.get_category_files(category="photos", user_id=user.id)
    )

    assert len(files) == 1
    assert files[0].category == "photos"


def test_cannot_get_other_files_with_same_category(
    create_unique_user, create_unique_file
):
    category = "audio"

    first_user = create_unique_user()
    first_file = create_unique_file(user=first_user, category=category)
    file_service.save_file(first_file)

    second_user = create_unique_user()
    second_file = create_unique_file(user=second_user, category=category)
    file_service.save_file(second_file)

    files = list(
        file_service.get_category_files(
            category=category, user_id=first_user.id
        )
    )

    assert first_file in files
    assert second_file not in files


def test_cannot_get_non_existing_category(default_user):
    user = default_user

    with pytest.raises(exceptions.NoCategoryFiles):
        file_service.get_category_files(category="documents", user_id=user.id)
