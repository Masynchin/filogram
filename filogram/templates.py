"""Шаблоны и готовые ответы для бота"""
from . import keyboards


def generate_grouped_files_text(files_with_categories):
    """Создание текста о файлах пользователя по шаблону"""
    return "\n\n".join(
        FILES_WITH_CATEGORIES.format(
            category=category,
            files="\n\n".join(SINGLE_FILE.format(file=file) for file in files),
        )
        for category, files in files_with_categories.items()
    )


START_MESSAGE = (
    "Привет! Я - Filogram, бот, позволяющий удобно хранить файлы.\n"
    "Чтобы загрузить файл, отправьте его и выберите для него категорию\n\n"
    "Предназначения кнопок на главной клавиатуре:\n"
    f"*{keyboards.MY_FILES}*"
    " - получить список ваших файлов\n"
    f"*{keyboards.GET_CATEGORY_FILES}*"
    " - получить все файлы определённой категории\n"
    f"*{keyboards.DELETE_CATEGORY_FILES}*"
    " - удалить все файлы определённой категории"
)

INCORRECT_CATEGORY_NAME = "Недопустимое название категории. Введите новое"

FILES_WITH_CATEGORIES = "*{category}*\n\n{files}"
SINGLE_FILE = (
    "`{file.file_name}`\n"
    "_Получить файл:_ /f{file.unique_id:04}\n"
    "_Удалить файл:_ /d{file.unique_id:04}"
)

NO_FILES_UPLOADED_YET = (
    "Похоже, что у вас ещё нет ни одного файла.\n"
    "Вы можете загрузить их, отправив в виде файла"
)

FILE_ALREADY_EXISTS = "Данный файл уже сохранён"
