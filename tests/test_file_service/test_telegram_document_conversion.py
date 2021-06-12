from filogram import file_service


def test_convert_teleram_document_to_file_model(
    default_document, default_user, default_category
):
    file = file_service.FileModel.from_telegram_document(
        default_document, owner_id=default_user.id, category=default_category
    )

    assert file.file_id == default_document.file_id
    assert file.file_name == default_document.file_name
    assert file.owner_id == default_user.id
    assert file.category == default_category


def test_save_telegram_document(
    default_document,
    default_user,
    default_category,
    get_file_unique_id,
):
    file_service.save_telegram_document(
        default_document, user_id=default_user.id, category=default_category
    )

    unique_id = get_file_unique_id()
    file = file_service.get_file(
        unique_id=unique_id,
        user_id=default_user.id,
    )

    assert file.file_id == default_document.file_id
    assert file.file_name == default_document.file_name
    assert file.owner_id == default_user.id
    assert file.category == default_category
