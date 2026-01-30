"""Обработчик команды /start и deep links."""

import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import User, Conversation, async_session
from bot.states.conversation import ConversationStates
from bot.keyboards.inline import get_main_inline_keyboard
from bot.utils.validators import validate_deep_link, get_source_info

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Обработка команды /start с deep link."""
    try:
        # Парсинг deep link параметров
        args = message.text.split(maxsplit=1)
        source = "direct"
        source_detail = None
        
        if len(args) > 1:
            # Есть параметры deep link: /start channel_post123
            param = args[1]
            validated_source, validated_detail = validate_deep_link(param)
            
            if validated_source is None:
                # Невалидный параметр, логируем и используем direct
                logger.warning(f"Невалидный deep link от {message.from_user.id}: {param}")
                source = "direct"
                source_detail = None
            else:
                source = validated_source
                source_detail = validated_detail
        
        # Сохранение пользователя в БД
        async with async_session() as session:
            # Проверяем, есть ли пользователь
            result = await session.execute(
                select(User).where(User.telegram_id == message.from_user.id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                # Создаем нового пользователя
                user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name
                )
                session.add(user)
            
            # Проверяем активный диалог (RACE CONDITION FIX)
            result = await session.execute(
                select(Conversation).where(Conversation.user_id == message.from_user.id)
            )
            conversation = result.scalar_one_or_none()
            
            if not conversation:
                # Создаем новый диалог только если его нет
                conversation = Conversation(
                    user_id=message.from_user.id,
                    source=source,
                    source_detail=source_detail,
                    state="STARTED"
                )
                session.add(conversation)
                logger.info(f"Создан новый диалог для {message.from_user.id} из {get_source_info(source, source_detail)}")
            else:
                # Диалог уже активен, пересоздаем состояние
                logger.info(f"Переиспользуется активный диалог для {message.from_user.id}")
                await state.clear()
            
            await session.commit()
    
    except Exception as e:
        logger.error(f"Ошибка при обработке /start: {e}", exc_info=True)
        await message.answer(
            "❌ Произошла ошибка. Пожалуйста, попробуйте снова позже.",
            reply_markup=get_main_inline_keyboard()
        )
        return
    
    # Формируем приветственное сообщение в зависимости от источника
    if source == "channel":
        greeting = "👋 Привет! Вы пришли из нашего канала."
    elif source == "group":
        greeting = "👋 Привет! Вы пришли из нашей группы."
    elif source == "site":
        greeting = f"👋 Привет! Вы пришли с сайта {source_detail}."
    else:
        greeting = "👋 Привет! Добро пожаловать в Avtozakaz74 Bot!"
    
    welcome_message = f"""{greeting}

Я помогу вам с подбором автомобиля из Китая! 🚗

Отвечу на несколько вопросов, чтобы лучше понять ваши потребности, и передам информацию нашему менеджеру.

Начнем? Напишите ваш бюджет на покупку автомобиля (например: "2-3 млн руб" или "дo 4 млн")"""
    
    try:
        await message.answer(welcome_message, reply_markup=get_main_inline_keyboard())
    except Exception as e:
        logger.error(f"Ошибка при отправке приветственного сообщения: {e}", exc_info=True)
        return
    
    # Переходим к состоянию сбора бюджета
    await state.set_state(ConversationStates.ASKING_BUDGET)


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработка команды /help."""
    help_text = """
ℹ️ <b>Справка по боту</b>

Этот бот помогает с подбором автомобилей из Китая.

<b>Доступные команды:</b>
/start - Начать диалог заново
/help - Показать эту справку
/cancel - Отменить текущий диалог

<b>Контакты:</b>
📞 +7 902 614-25-03 (Дмитрий)
📞 +7 919 302-89-13 (Максим)
💬 Telegram: @avtozakaz74
"""
    await message.answer(help_text, parse_mode="HTML", reply_markup=get_main_inline_keyboard())


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Отмена текущего диалога."""
    current_state = await state.get_state()
    
    if current_state is None:
        await message.answer("❌ Нет активного диалога для отмены.")
        return
    
    await state.clear()
    
    # Удаляем диалог из БД
    async with async_session() as session:
        result = await session.execute(
            select(Conversation).where(Conversation.user_id == message.from_user.id)
        )
        conversation = result.scalar_one_or_none()
        
        if conversation:
            await session.delete(conversation)
            await session.commit()
    
    await message.answer(
        "❌ Диалог отменен.\n\n"
        "Чтобы начать заново, используйте кнопки ниже или /start",
        reply_markup=get_main_inline_keyboard()
    )


# Inline кнопки - обработчики callback

@router.callback_query(F.data == "start")
async def callback_start(callback: CallbackQuery, state: FSMContext):
    """Обработка inline кнопок Старт и Начать заново."""
    await state.clear()
    await callback.message.delete()
    await cmd_start(callback.message, state)
    await callback.answer()


@router.callback_query(F.data == "cancel")
async def callback_cancel(callback: CallbackQuery, state: FSMContext):
    """Обработка inline кнопки Отменить."""
    await cmd_cancel(callback.message, state)
    await callback.answer("Диалог отменен")


@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    """Обработка inline кнопки Справка."""
    help_text = """
ℹ️ <b>Справка по боту</b>

Этот бот помогает с подбором автомобилей из Китая.

<b>Доступные команды:</b>
/start - Начать диалог заново
/help - Показать эту справку
/cancel - Отменить текущий диалог

<b>Контакты:</b>
📞 +7 902 614-25-03 (Дмитрий)
📞 +7 919 302-89-13 (Максим)
💬 Telegram: @avtozakaz74
"""
    await callback.message.answer(help_text, parse_mode="HTML", reply_markup=get_main_inline_keyboard())
    await callback.answer()


@router.callback_query(F.data == "contacts")
async def callback_contacts(callback: CallbackQuery):
    """Обработка inline кнопки Контакты."""
    contacts_text = """
📞 <b>Контакты АвтоЗаказ74</b>

<b>Телефон:</b>
+7 902 614-25-03

<b>Telegram канал:</b>
https://t.me/avtozakaz74

<b>Другие телефоны:</b>
📞 +7 919 302-89-13 (Максим)

Мы работаем напрямую с экспортными компаниями в Китае, Японии и Корее! 🚗
"""
    await callback.message.answer(contacts_text, parse_mode="HTML", reply_markup=get_main_inline_keyboard())
    await callback.answer()
