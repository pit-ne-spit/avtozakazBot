"""Валидация параметров и deep links."""

import re
from typing import Tuple, Optional


# Регулярные выражения для валидации источников
CHANNEL_POST_PATTERN = r"^channel(?:_post\d+)?$"
GROUP_PATTERN = r"^group$"
SITE_PATTERN = r"^site_[\w\-]{1,50}$"

# Максимальная длина source_detail
MAX_SOURCE_DETAIL_LENGTH = 100


def validate_deep_link(param: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Валидация параметра deep link и возврат (source, source_detail).
    
    Поддерживаемые форматы:
    - channel, channel_post123 -> ('channel', 'channel' или 'channel_post123')
    - site_name -> ('site', 'name')
    - group -> ('group', 'telegram_group')
    - Любое другое -> ('direct', param)
    
    Если валидация не пройдена, возвращает (None, None).
    
    Args:
        param: параметр из deep link
        
    Returns:
        Кортеж (source, source_detail) или (None, None) при ошибке
    """
    if not param or len(param) > MAX_SOURCE_DETAIL_LENGTH:
        return None, None
    
    # Проверяем канал
    if re.match(CHANNEL_POST_PATTERN, param):
        return "channel", param
    
    # Проверяем группу
    if re.match(GROUP_PATTERN, param):
        return "group", "telegram_group"
    
    # Проверяем сайт
    if re.match(SITE_PATTERN, param):
        site_name = param.replace("site_", "")
        return "site", site_name
    
    # Проверяем что в direct не передана опасная информация
    if is_safe_string(param):
        return "direct", param
    
    # Небезопасный параметр
    return None, None


def is_safe_string(s: str) -> bool:
    """
    Проверить что строка безопасна (нет специальных символов, SQL-injection и т.д.).
    
    Args:
        s: строка для проверки
        
    Returns:
        True если строка безопасна, иначе False
    """
    if not s or len(s) > MAX_SOURCE_DETAIL_LENGTH:
        return False
    
    # Разрешаем только буквы, цифры, дефис, подчеркивание, точку
    if re.match(r"^[\w\-\.]+$", s):
        return True
    
    return False


def format_source_for_display(source: Optional[str], source_detail: Optional[str]) -> str:
    """
    Форматировать источник для отображения в сообщениях админам.
    
    Args:
        source: тип источника
        source_detail: детали источника
        
    Returns:
        Отформатированная строка с эмодзи и описанием
    """
    if source == "channel":
        return f"📢 Канал: {source_detail}"
    elif source == "group":
        return "👥 Группа Telegram"
    elif source == "site":
        return f"🌐 Сайт: {source_detail}"
    else:
        return "🔗 Прямой переход"
