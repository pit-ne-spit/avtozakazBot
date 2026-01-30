"""Конфигурация логирования для production и development."""

import os
import logging
from logging.handlers import RotatingFileHandler
from config import LOG_LEVEL, LOG_DIR, LOG_FILE, ENVIRONMENT


def setup_logging():
    """Настройка логирования с ротацией файлов."""
    
    # Создаем директорию для логов если ее нет
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # Формат логирования
    if ENVIRONMENT == "production":
        log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # Получаем root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    
    # Удаляем существующие handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # File handler с ротацией (максимум 5 файлов по 10MB каждый)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(LOG_LEVEL)
    root_logger.addHandler(file_handler)
    
    # Console handler для development
    if ENVIRONMENT != "production":
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        console_handler.setLevel(LOG_LEVEL)
        root_logger.addHandler(console_handler)
    
    # Логируем инициализацию
    logger = logging.getLogger(__name__)
    logger.info(f"Логирование инициализировано. Режим: {ENVIRONMENT}")
    logger.info(f"Уровень логирования: {logging.getLevelName(LOG_LEVEL)}")
    logger.info(f"Логи сохраняются в: {LOG_FILE}")
    
    return root_logger
