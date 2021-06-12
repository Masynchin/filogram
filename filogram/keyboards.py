"""Клавиатуры для бота"""
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


EXTRA_CATEGORY = "Добавить категорию"
CANCEL_GETTING = CANCEL_DELETION = "Отмена"


def create_categories_keboard(categories):
    """Создание клавиатуры для выбора категории файла"""
    keyboard = InlineKeyboardMarkup()
    buttons = (*categories, EXTRA_CATEGORY)
    _add_inline_buttons(keyboard, buttons)
    return keyboard


def create_categories_get_keyboard(categories):
    """Создание клавиатуры для выбора категории для получения файлов"""
    keyboard = InlineKeyboardMarkup()
    buttons = (*categories, CANCEL_GETTING)
    _add_inline_buttons(keyboard, buttons)
    return keyboard


def create_categories_delete_keyboard(categories):
    """Создание клавиатуры для выбора категории для удаления файлов"""
    keyboard = InlineKeyboardMarkup()
    buttons = (*categories, CANCEL_DELETION)
    _add_inline_buttons(keyboard, buttons)
    return keyboard


def _add_inline_buttons(keyboard, button_texts):
    """Добавление кнопок на inline-клавиатуру"""
    for text in button_texts:
        keyboard.add(InlineKeyboardButton(text, callback_data=text))


MY_FILES = "Мои файлы"
GET_CATEGORY_FILES = "Получить категорию"
DELETE_CATEGORY_FILES = "Удалить категорию"


main_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton(MY_FILES)],
        [KeyboardButton(GET_CATEGORY_FILES)],
        [KeyboardButton(DELETE_CATEGORY_FILES)],
    ],
    resize_keyboard=True,
)
