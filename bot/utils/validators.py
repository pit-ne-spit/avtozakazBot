"""Валидаторы для глубоких ссылок и параметров бота."""

import re
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# Допустимые источники
VALID_SOURCES = {"channel", "group", "site", "direct"}

# Максимальная длина параметров
MAX_SOURCE_DETAIL_LENGTH = 100

# Регулярные выражения для валидации
CHANNEL_POST_PATTERN = r"^channel(?:_post\d+)?$"
GROUP_PATTERN = r"^group$"
SITE_PATTERN = r"^site_[\w\-]{1,50}$"


def validate_deep_link(param: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Валидирует параметры deep link.
    
    Args:
        param: Строка параметра из deep link (например: 'channel_post123' или 'site_avtozakaz74')
    
    Returns:
        Кортеж (source, source_detail) или (None, None) если параметр невалиден
    """
    if not param:
        return "direct", None
    
    # Проверяем длину
    if len(param) > MAX_SOURCE_DETAIL_LENGTH:
        logger.warning(f"❌ Deep link параметр слишком длинный: {len(param)} символов")
        return None, None
    
    # Парсим параметр
    if param.startswith("channel"):
        # Валидируем формат: channel или channel_post123
        if re.match(CHANNEL_POST_PATTERN, param):
            return "channel", param
        else:
            logger.warning(f"Невалидный формат канала: {param}")
            return None, None
    
    elif param.startswith("group"):
        # Валидируем формат: group
        if re.match(GROUP_PATTERN, param):
            return "group", param
        else:
            logger.warning(f"Невалидный формат группы: {param}")
            return None, None
    
    elif param.startswith("site"):
        # Валидируем формат: site_avtozakaz74
        if re.match(SITE_PATTERN, param):
            # Извлекаем название сайта
            site_name = param.replace("site_", "")
            return "site", site_name
        else:
            logger.warning(f"Невалидный формат сайта: {param}")
            return None, None
    
    else:
        # Неизвестный источник
        logger.warning(f"Неизвестный источник в deep link: {param}")
        return None, None


def get_source_info(source: Optional[str], source_detail: Optional[str]) -> str:
    """
    Формирует читаемое описание источника для логирования.
    
    Args:
        source: Источник (channel, group, site, direct)
        source_detail: Детали источника
    
    Returns:
        Строка описания
    """
    if not source:
        return "неизвестный источник"
    
    if source == "channel":
        return f"📢 Канал: {source_detail or 'без деталей'}"
    elif source == "group":
        return f"👥 Группа"
    elif source == "site":
        return f"🌐 Сайт: {source_detail or 'без деталей'}"
    else:
        return "🔗 Прямой переход"
