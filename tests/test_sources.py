#!/usr/bin/env python
"""Несты для проверки корректной обработки источников лидов."""

import sys
from pathlib import Path

# Добавляем родительскую папку в path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.models import Lead


def format_source_message(lead: Lead) -> str:
    """
    Имитирует функцию send_lead_to_admins для формирования текста источника.
    
    Args:
        lead: Объект Lead с информацией о лиде
        
    Returns:
        Отформатированная строка с источником
    """
    if lead.source == "site":
        source_text = f"🌐 Сайт: {lead.source_detail}"
    elif lead.source == "channel":
        source_text = f"📢 Канал: {lead.source_detail}"
    elif lead.source == "group":
        source_text = "👥 Группа Telegram"
    else:
        source_text = "🔗 Прямой переход"
    return source_text


def test_group_source():
    """Тест: Лид из группы должен показывать '👥 Группа Telegram'."""
    print("\n=== Тест 1: Источник - ГРУППА ===")
    
    lead = Lead(
        user_id=123456789,
        username="testuser",
        source="group",
        source_detail="group",
        budget="2-3 млн",
        preferences="Toyota",
        timeline="месяц",
        comments=None
    )
    
    source_text = format_source_message(lead)
    expected = "👥 Группа Telegram"
    
    print(f"  Lead.source: {lead.source}")
    print(f"  Lead.source_detail: {lead.source_detail}")
    print(f"  Результат: {source_text}")
    print(f"  Ожидается: {expected}")
    
    assert source_text == expected, f"❌ Ошибка! Ожидалось '{expected}', получено '{source_text}'"
    print("  ✅ ТЕСТ ПРОЙДЕН!")


def test_site_source():
    """Тест: Лид с сайта должен показывать '🌐 Сайт: avtozakaz74'."""
    print("\n=== Тест 2: Источник - САЙТ ===")
    
    lead = Lead(
        user_id=987654321,
        username="testuser2",
        source="site",
        source_detail="avtozakaz74",
        budget="3-4 млн",
        preferences="Honda",
        timeline="2-3 месяца",
        comments="Срочно нужно"
    )
    
    source_text = format_source_message(lead)
    expected = "🌐 Сайт: avtozakaz74"
    
    print(f"  Lead.source: {lead.source}")
    print(f"  Lead.source_detail: {lead.source_detail}")
    print(f"  Результат: {source_text}")
    print(f"  Ожидается: {expected}")
    
    assert source_text == expected, f"❌ Ошибка! Ожидалось '{expected}', получено '{source_text}'"
    print("  ✅ ТЕСТ ПРОЙДЕН!")


def test_channel_source():
    """Тест: Лид из канала должен показывать '📢 Канал: channel_post123'."""
    print("\n=== Тест 3: Источник - КАНАЛ (с номером поста) ===")
    
    lead = Lead(
        user_id=111111111,
        username="testuser3",
        source="channel",
        source_detail="channel_post123",
        budget="1-2 млн",
        preferences="BMW",
        timeline="не срочно",
        comments=None
    )
    
    source_text = format_source_message(lead)
    expected = "📢 Канал: channel_post123"
    
    print(f"  Lead.source: {lead.source}")
    print(f"  Lead.source_detail: {lead.source_detail}")
    print(f"  Результат: {source_text}")
    print(f"  Ожидается: {expected}")
    
    assert source_text == expected, f"❌ Ошибка! Ожидалось '{expected}', получено '{source_text}'"
    print("  ✅ ТЕСТ ПРОЙДЕН!")


def test_channel_source_general():
    """Тест: Лид из канала (общая ссылка) должен показывать '📢 Канал: channel'."""
    print("\n=== Тест 4: Источник - КАНАЛ (общая ссылка) ===")
    
    lead = Lead(
        user_id=222222222,
        username="testuser4",
        source="channel",
        source_detail="channel",
        budget="2-3 млн",
        preferences="Mercedes",
        timeline="месяц",
        comments=None
    )
    
    source_text = format_source_message(lead)
    expected = "📢 Канал: channel"
    
    print(f"  Lead.source: {lead.source}")
    print(f"  Lead.source_detail: {lead.source_detail}")
    print(f"  Результат: {source_text}")
    print(f"  Ожидается: {expected}")
    
    assert source_text == expected, f"❌ Ошибка! Ожидалось '{expected}', получено '{source_text}'"
    print("  ✅ ТЕСТ ПРОЙДЕН!")


def test_direct_source():
    """Тест: Прямой переход должен показывать '🔗 Прямой переход'."""
    print("\n=== Тест 5: Источник - ПРЯМОЙ ПЕРЕХОД ===")
    
    lead = Lead(
        user_id=333333333,
        username="testuser5",
        source="direct",
        source_detail=None,
        budget="4-5 млн",
        preferences="Audi",
        timeline="2 месяца",
        comments=None
    )
    
    source_text = format_source_message(lead)
    expected = "🔗 Прямой переход"
    
    print(f"  Lead.source: {lead.source}")
    print(f"  Lead.source_detail: {lead.source_detail}")
    print(f"  Результат: {source_text}")
    print(f"  Ожидается: {expected}")
    
    assert source_text == expected, f"❌ Ошибка! Ожидалось '{expected}', получено '{source_text}'"
    print("  ✅ ТЕСТ ПРОЙДЕН!")


def test_unknown_source():
    """Тест: Неизвестный источник должен показывать '🔗 Прямой переход'."""
    print("\n=== Тест 6: Неизвестный источник ===")
    
    lead = Lead(
        user_id=444444444,
        username="testuser6",
        source="unknown",
        source_detail=None,
        budget="2 млн",
        preferences="Tesla",
        timeline="неделя",
        comments=None
    )
    
    source_text = format_source_message(lead)
    expected = "🔗 Прямой переход"
    
    print(f"  Lead.source: {lead.source}")
    print(f"  Lead.source_detail: {lead.source_detail}")
    print(f"  Результат: {source_text}")
    print(f"  Ожидается: {expected}")
    
    assert source_text == expected, f"❌ Ошибка! Ожидалось '{expected}', получено '{source_text}'"
    print("  ✅ ТЕСТ ПРОЙДЕН!")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 ТЕСТИРОВАНИЕ ОБРАБОТКИ ИСТОЧНИКОВ ЛИДОВ")
    print("=" * 60)
    
    try:
        test_group_source()
        test_site_source()
        test_channel_source()
        test_channel_source_general()
        test_direct_source()
        test_unknown_source()
        
        print("\n" + "=" * 60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ ТЕСТ НЕ ПРОЙДЕН: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
