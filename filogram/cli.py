"""Модуль для запуска бота с определённой конфигурацией через консоль"""
import argparse
import os

from aiogram import executor
from aiogram.utils.executor import start_webhook


parser = argparse.ArgumentParser()
parser.add_argument("--stage", choices=["dev", "prod"], default="dev")
parser.add_argument("--use", choices=["polling", "webhook"], default="polling")


def cli():
    """Запуск бота через командную строку.

    Аргументы:
    --stage: dev - запуск бота при разработке, prod - запуск бота в продакшене
    --use: polling (по умолчанию запускается поллинг)
    """
    args = parser.parse_args()
    os.environ["STAGE"] = args.stage

    if args.use == "polling":
        run_polling()
    elif args.use == "webhook":
        run_webhook()


def run_polling():
    """Запуск бота через поллинг"""
    from .bot import dp

    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_polling_startup,
        on_shutdown=on_polling_shutdown,
    )


async def on_polling_startup(dp):
    """Колбэк при включении бота через поллинг"""
    from .logger import logger

    logger.info("Запуск бота через поллинг")


async def on_polling_shutdown(dp):
    """Колбэк при выключении бота через поллинг"""
    from . import db
    from .logger import logger

    db.close_connection()

    logger.info("Работа бота завершена")


def run_webhook():
    """Функция запуска бота через вебхук"""
    from .bot import dp

    webhook_path = os.getenv("WEBHOOK_PATH")
    host = os.getenv("WEBAPP_HOST")
    port = os.getenv("WEBAPP_PORT")

    start_webhook(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_webhook_startup,
        on_shutdown=on_webhook_shutdown,
        webhook_path=webhook_path,
        host=host,
        port=port,
    )


async def on_webhook_startup(dp):
    """Колбэк при включении бота через вебхук"""
    from .bot import bot

    webhook_url = os.getenv("WEBHOOK_URL")
    await bot.set_webhook(webhook_url)


async def on_webhook_shutdown(dp):
    """Колбэк при выключении бота через вебхук"""
    from . import db
    from .bot import bot
    from .logger import logger

    await bot.delete_webhook()
    db.close_connection()

    logger.info("Работа бота завершена")
