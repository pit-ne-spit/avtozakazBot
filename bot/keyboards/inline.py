"""Inline клавиатуры для бота."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_inline_keyboard() -> InlineKeyboardMarkup:
    """Получить основную inline клавиатуру бота."""
    keyboard = [
        [
            InlineKeyboardButton(text="🚗 Начать заново", callback_data="start"),
        ],
        [
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel"),
            InlineKeyboardButton(text="📞 Контакты", callback_data="contacts"),
            InlineKeyboardButton(text="ℹ️ Справка", callback_data="help"),
        ],
        [
            InlineKeyboardButton(text="🌐 Подобрать авто на сайте", url="https://avtozakaz74.ru/"),
        ],
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
