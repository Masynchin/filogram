from filogram import file_service


def test_correct_files_grouping_by_category(create_unique_file):
    files = []
    for category in ["books", "audio", "texts", "audio"]:
        file = create_unique_file(category=category)
        files.append(file)

    (book_file, audio_file, text_file, another_audio_file) = files
    files = sort_files_by_category(files)

    grouped_files = file_service.group_files_by_category(files)

    assert grouped_files == {
        "books": (book_file,),
        "texts": (text_file,),
        "audio": (audio_file, another_audio_file),
    }


def sort_files_by_category(files):
    """Сортировка файлов по категории и уникальному ID.

    В основном коде сортировка файлов происходит при запросе к БД.
    Там они сортируются по категории, и если они совпадают, то по
    полю `unique_id`.

    Присвоить файлу во время создания поле `unique_id` нельзя, так как
    `FileModel` является дочерним классом NamedTuple. В данной функции
    `enumerate` используется в качестве замены поля `unique_id`
    """
    files_sorted_by_category = sorted(
        enumerate(files), key=lambda pair: (pair[1].category, pair[0])
    )
    files_sorted_by_category = [file for (_, file) in files_sorted_by_category]
    return files_sorted_by_category


def test_correct_owned_files_grouping_by_category(
    default_user, create_unique_file
):
    files = []
    for category in ["books", "audio", "texts", "audio"]:
        file = create_unique_file(user=default_user, category=category)
        file_service.save_file(file)
        files.append(file)

    (book_file, audio_file, text_file, another_audio_file) = files

    owned_files = file_service.get_owned_files(default_user.id)
    grouped_files = file_service.group_files_by_category(owned_files)

    assert grouped_files == {
        "books": (book_file,),
        "texts": (text_file,),
        "audio": (audio_file, another_audio_file),
    }
