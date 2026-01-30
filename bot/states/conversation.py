"""Состояния для диалога с пользователем."""

from aiogram.fsm.state import State, StatesGroup


class ConversationStates(StatesGroup):
    """Группа состояний для диалога."""
    
    # Начальное состояние
    STARTED = State()
    
    # Сбор информации
    ASKING_BUDGET = State()
    ASKING_PREFERENCES = State()
    ASKING_TIMELINE = State()
    ASKING_COMMENTS = State()
    
    # Завершение
    COMPLETED = State()
