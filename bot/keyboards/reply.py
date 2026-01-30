"""Reply клавиатуры для бота."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Получить основную клавиатуру бота."""
    keyboard = [
        [
            KeyboardButton(text="🚗 Начать заново"),
            KeyboardButton(text="▶️ Старт"),
        ],
        [
            KeyboardButton(text="❌ Отменить"),
            KeyboardButton(text="📞 Контакты"),
            KeyboardButton(text="ℹ️ Справка"),
        ],
        [
            KeyboardButton(text="🌐 Подобрать авто на сайте"),
        ],
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие или напишите текст"
    )
