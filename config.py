"""Конфигурация бота из переменных окружения."""

import os
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID администраторов (менеджеров)
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip()]

# База данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot.db")

# Конфигурация источников (для deep links)
# Это наименования для генерации deep links
SOURCES = {
    # Канал Telegram
    "CHANNEL": "channel",
    # Группа Telegram
    "GROUP": "group",
    # Получите deep link для вашого сайта
    "SITE": "site_avtozakaz74",
    # Прямой переход в бот
    "DIRECT": "direct",
}

# Наименования сайтов для отображения
SITE_NAMES = {
    "avtozakaz74": "🌐 avtozakaz74.ru",
}

# Валидация обязательных параметров
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

if not ADMIN_IDS:
    print("⚠️  ADMIN_IDS не настроены. Уведомления менеджерам работать не будут.")

# Режим
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Конфигурация логирования
LOG_LEVEL = logging.INFO if ENVIRONMENT == "production" else logging.DEBUG
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "bot.log")
