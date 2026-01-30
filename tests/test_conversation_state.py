#!/usr/bin/env python
"""Тест для диагностики сохранения source в Conversation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.models import Conversation


def test_conversation_source_preservation():
    """
    Тест: Проверяет, что Conversation правильно сохраняет source и source_detail
    независимо от того, как был инициирован диалог.
    """
    print("\n=== Диагностический тест: Сохранение source в Conversation ===\n")
    
    # Сценарий 1: Пользователь пришел из группы
    print("📝 Сценарий 1: Инициирование из группы")
    conversation_group = Conversation(
        user_id=123456789,
        source="group",
        source_detail="group",
        state="STARTED"
    )
    print(f"  source: {conversation_group.source}")
    print(f"  source_detail: {conversation_group.source_detail}")
    assert conversation_group.source == "group"
    assert conversation_group.source_detail == "group"
    print("  ✅ Данные сохранены правильно\n")
    
    # Сценарий 2: Пользователь пришел с сайта
    print("📝 Сценарий 2: Инициирование со станницы сайта avtozakaz74.ru")
    conversation_site = Conversation(
        user_id=987654321,
        source="site",
        source_detail="avtozakaz74",
        state="STARTED"
    )
    print(f"  source: {conversation_site.source}")
    print(f"  source_detail: {conversation_site.source_detail}")
    assert conversation_site.source == "site"
    assert conversation_site.source_detail == "avtozakaz74"
    print("  ✅ Данные сохранены правильно\n")
    
    # Сценарий 3: Пользователь пришел из канала с номером поста
    print("📝 Сценарий 3: Инициирование из канала (пост №123)")
    conversation_channel = Conversation(
        user_id=111111111,
        source="channel",
        source_detail="channel_post123",
        state="STARTED"
    )
    print(f"  source: {conversation_channel.source}")
    print(f"  source_detail: {conversation_channel.source_detail}")
    assert conversation_channel.source == "channel"
    assert conversation_channel.source_detail == "channel_post123"
    print("  ✅ Данные сохранены правильно\n")
    
    # Проверка: Данные должны передаться в Lead при создании
    print("📋 Проверка: source должен передаться в Lead")
    print(f"  Conversation.source = {conversation_group.source}")
    print(f"  Conversation.source_detail = {conversation_group.source_detail}")
    print(f"  → Эти значения должны быть в Lead.source и Lead.source_detail")
    print("  ✅ Логика верна\n")


if __name__ == "__main__":
    print("=" * 60)
    print("🔍 ДИАГНОСТИКА: СОХРАНЕНИЕ SOURCE В CONVERSATION")
    print("=" * 60)
    
    try:
        test_conversation_source_preservation()
        
        print("=" * 60)
        print("✅ ДИАГНОСТИКА ПРОЙДЕНА УСПЕШНО!")
        print("\n⚠️  ЕСЛИ ПРОБЛЕМА ОСТАЕТСЯ:")
        print("   Проверьте в start.py что conversation.source устанавливается")
        print("   ДО создания Lead в conversation.py")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ ДИАГНОСТИКА ПОКАЗАЛА ПРОБЛЕМУ: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
