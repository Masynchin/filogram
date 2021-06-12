from filogram import file_service


def test_correct_user_categories(default_user, create_unique_file):
    categories = ["photos", "videos"]
    for category in categories:
        file = create_unique_file(user=default_user, category=category)
        file_service.save_file(file)

    user_categories = file_service.get_user_categories(user_id=default_user.id)

    assert all(c in user_categories for c in categories)


def test_all_categories_unique(default_user, create_unique_file):
    categories = ["audio", "audio", "audio"]
    for category in categories:
        file = create_unique_file(user=default_user, category=category)
        file_service.save_file(file)

    user_categories = file_service.get_user_categories(user_id=default_user.id)

    assert user_categories == ["audio"]


def test_no_someone_elses_categories(create_unique_user, create_unique_file):
    first_user = create_unique_user()
    second_user = create_unique_user()

    first_user_categories = ["photos", "videos"]
    second_user_categories = ["games", "programs"]

    for category in first_user_categories:
        file = create_unique_file(user=first_user, category=category)
        file_service.save_file(file)

    for category in second_user_categories:
        file = create_unique_file(user=second_user, category=category)
        file_service.save_file(file)

    user_categories = file_service.get_user_categories(first_user.id)

    assert all(c in user_categories for c in first_user_categories)
    assert all(c not in user_categories for c in second_user_categories)
