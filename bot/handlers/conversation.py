"""Обработчики диалога с пользователем."""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from database import Conversation, Lead, async_session
from bot.states.conversation import ConversationStates
from config import ADMIN_IDS

router = Router()


@router.message(ConversationStates.ASKING_BUDGET)
async def process_budget(message: Message, state: FSMContext):
    """Обработка ответа о бюджете."""
    budget = message.text
    
    # Сохраняем в state
    await state.update_data(budget=budget)
    
    # Сохраняем в БД
    async with async_session() as session:
        result = await session.execute(
            select(Conversation).where(Conversation.user_id == message.from_user.id)
        )
        conversation = result.scalar_one_or_none()
        
        if conversation:
            conversation.budget = budget
            conversation.state = "ASKING_PREFERENCES"
            await session.commit()
    
    # Следующий вопрос
    await message.answer(
        "Отлично! 👍\n\n"
        "Какие у вас предпочтения по автомобилю?\n"
        "(Например: марка, тип кузова, год выпуска и т.д.)"
    )
    
    await state.set_state(ConversationStates.ASKING_PREFERENCES)


@router.message(ConversationStates.ASKING_PREFERENCES)
async def process_preferences(message: Message, state: FSMContext):
    """Обработка предпочтений."""
    preferences = message.text
    
    await state.update_data(preferences=preferences)
    
    # Сохраняем в БД
    async with async_session() as session:
        result = await session.execute(
            select(Conversation).where(Conversation.user_id == message.from_user.id)
        )
        conversation = result.scalar_one_or_none()
        
        if conversation:
            conversation.preferences = preferences
            conversation.state = "ASKING_TIMELINE"
            await session.commit()
    
    await message.answer(
        "Понял! 📝\n\n"
        "В какие сроки планируете покупку?\n"
        "(Например: \"в течение месяца\", \"2-3 месяца\", \"не срочно\")"
    )
    
    await state.set_state(ConversationStates.ASKING_TIMELINE)


@router.message(ConversationStates.ASKING_TIMELINE)
async def process_timeline(message: Message, state: FSMContext):
    """Обработка сроков."""
    timeline = message.text
    
    await state.update_data(timeline=timeline)
    
    # Сохраняем в БД
    async with async_session() as session:
        result = await session.execute(
            select(Conversation).where(Conversation.user_id == message.from_user.id)
        )
        conversation = result.scalar_one_or_none()
        
        if conversation:
            conversation.timeline = timeline
            conversation.state = "ASKING_COMMENTS"
            await session.commit()
    
    await message.answer(
        "Спасибо! 🙏\n\n"
        "Есть ли у вас дополнительные комментарии или вопросы?\n"
        "(Или напишите \"нет\", если дополнений нет)"
    )
    
    await state.set_state(ConversationStates.ASKING_COMMENTS)


@router.message(ConversationStates.ASKING_COMMENTS)
async def process_comments(message: Message, state: FSMContext):
    """Обработка комментариев и завершение диалога."""
    comments = message.text if message.text.lower() not in ["нет", "no", "-"] else None
    
    await state.update_data(comments=comments)
    
    # Получаем все данные
    data = await state.get_data()
    
    # Получаем информацию из БД
    async with async_session() as session:
        result = await session.execute(
            select(Conversation).where(Conversation.user_id == message.from_user.id)
        )
        conversation = result.scalar_one_or_none()
        
        if conversation:
            conversation.comments = comments
            conversation.state = "COMPLETED"
            
            # Создаем лид
            lead = Lead(
                user_id=message.from_user.id,
                username=message.from_user.username,
                source=conversation.source,
                source_detail=conversation.source_detail,
                budget=data.get('budget'),
                preferences=data.get('preferences'),
                timeline=data.get('timeline'),
                comments=comments
            )
            session.add(lead)
            
            # Удаляем активный диалог
            await session.delete(conversation)
            await session.commit()
            
            # Отправляем уведомление менеджерам
            await send_lead_to_admins(message, lead)
    
    await message.answer(
        "✅ Отлично! Все данные получены.\n\n"
        "Наш менеджер свяжется с вами в ближайшее время! 👨‍💼\n\n"
        "Если у вас появятся еще вопросы, используйте /start"
    )
    
    await state.clear()


async def send_lead_to_admins(message: Message, lead: Lead):
    """Отправка информации о лиде менеджерам."""
    
    # Определяем источник
    if lead.source == "site":
        source_text = f"🌐 Сайт: {lead.source_detail}"
    elif lead.source == "channel":
        source_text = f"📢 Канал: {lead.source_detail}"
    else:
        source_text = "🔗 Прямой переход"
    
    # Формируем сообщение
    username = f"@{lead.username}" if lead.username else "без username"
    
    lead_message = f"""
🔔 <b>Новый лид!</b>

<b>Источник:</b> {source_text}
<b>Пользователь:</b> {username} (ID: {lead.user_id})

<b>💰 Бюджет:</b> {lead.budget}
<b>🚗 Предпочтения:</b> {lead.preferences}
<b>⏰ Сроки:</b> {lead.timeline}
"""
    
    if lead.comments:
        lead_message += f"<b>💬 Комментарий:</b> {lead.comments}\n"
    
    lead_message += f"\n<a href='tg://user?id={lead.user_id}'>Написать клиенту</a>"
    
    # Отправляем всем администраторам
    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(
                chat_id=admin_id,
                text=lead_message,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"⚠️ Не удалось отправить сообщение админу {admin_id}: {e}")
