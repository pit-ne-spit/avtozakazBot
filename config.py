"""Конфигурация бота из переменных окружения."""

import os
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

# Валидация обязательных параметров
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

if not ADMIN_IDS:
    print("⚠️  ADMIN_IDS не настроены. Уведомления менеджерам работать не будут.")
