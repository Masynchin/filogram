"""Логгер"""
from loguru import logger

from .config import config


logger.add(
    encoding="u8",
    sink=config.LOGS_PATH,
    format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
    rotation="1 week",
    compression="zip",
    backtrace=False,
)
