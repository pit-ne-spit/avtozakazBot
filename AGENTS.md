# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Telegram бот для автоматизации приема заявок на подбор автомобилей из Китая. Бот собирает информацию от пользователей через интерактивный диалог и отправляет сформированные лиды менеджерам.

## Essential Commands

### Setup and Configuration
```powershell
# Установка зависимостей
pip install -r requirements.txt

# Настройка окружения (только при первом запуске)
Copy-Item .env.example .env
# Затем отредактировать .env с реальным BOT_TOKEN и ADMIN_IDS
```

### Running the Bot
```powershell
# Запуск бота (polling режим)
python main.py

# Остановка: Ctrl+C
```

## Architecture

### Conversation Flow (FSM)
Бот использует Finite State Machine для управления диалогом:
1. `/start` → парсинг deep link → создание `Conversation` → переход в `ASKING_BUDGET`
2. `ASKING_BUDGET` → сохранение ответа → `ASKING_PREFERENCES`
3. `ASKING_PREFERENCES` → сохранение ответа → `ASKING_TIMELINE`
4. `ASKING_TIMELINE` → сохранение ответа → `ASKING_COMMENTS`
5. `ASKING_COMMENTS` → создание `Lead` → удаление `Conversation` → уведомление менеджерам

Все состояния определены в `bot/states/conversation.py`. Каждый обработчик сохраняет данные как в FSM state (in-memory), так и в БД `Conversation` для персистентности.

### Deep Link Source Tracking
Формат deep links:
- `?start=channel` или `?start=channel_post123` - из Telegram канала
- `?start=site_avtozakaz74` - с веб-сайта (название сайта после префикса `site_`)
- без параметров - прямой переход (`source="direct"`)

Парсинг происходит в `bot/handlers/start.py:cmd_start()`, где извлекается `source` и `source_detail`, которые сохраняются в `Conversation` и затем переносятся в `Lead`.

### Database Design
Три основные модели в `database/models.py`:

**User** - информация о пользователях Telegram (создается при первом `/start`)
- `telegram_id` (unique) - используется для всех запросов вместо внутреннего `id`

**Conversation** - активный диалог (1 на пользователя)
- Хранит промежуточные ответы (`budget`, `preferences`, `timeline`, `comments`)
- Хранит состояние FSM в поле `state` (дублирует aiogram FSM для персистентности)
- Хранит `source` и `source_detail` для отслеживания происхождения лида
- Удаляется после завершения диалога

**Lead** - завершенная заявка (создается после финального ответа)
- Копирует все данные из `Conversation` для долгосрочного хранения
- Используется для отправки уведомления менеджерам

### Handler Registration
Все роутеры регистрируются в `main.py`:
```python
dp.include_router(start.router)
dp.include_router(conversation.router)
```

Порядок регистрации важен: более специфичные обработчики (FSM states) должны быть после общих команд.

### Admin Notifications
Когда `Lead` создан, функция `send_lead_to_admins()` в `bot/handlers/conversation.py` отправляет уведомление всем ID из `ADMIN_IDS`. Формат сообщения включает:
- Источник с эмодзи (🌐 для сайта, 📢 для канала)
- Username и Telegram ID пользователя
- Все собранные данные (бюджет, предпочтения, сроки, комментарии)
- Ссылку `tg://user?id=` для быстрого контакта

### Configuration
`config.py` загружает настройки из `.env`:
- `BOT_TOKEN` - обязательный, валидируется при запуске
- `ADMIN_IDS` - comma-separated list, преобразуется в `list[int]`
- `DATABASE_URL` - по умолчанию SQLite с aiosqlite драйвером

## Development Patterns

### Adding New Handler
1. Создать файл в `bot/handlers/`
2. Определить `router = Router()`
3. Добавить обработчики с декораторами `@router.message(...)`
4. Зарегистрировать в `main.py`: `dp.include_router(your_handler.router)`

### Adding New FSM State
1. Добавить состояние в `bot/states/conversation.py:ConversationStates`
2. Создать обработчик в `bot/handlers/conversation.py` с декоратором `@router.message(ConversationStates.YOUR_STATE)`
3. Обновить `Conversation.state` в БД при переходе между состояниями

### Database Migrations
При изменении моделей:
- Текущая версия использует автоматическое `Base.metadata.create_all()` в `init_db()`
- Для продакшена рекомендуется использовать Alembic для миграций
- База данных создается автоматически при первом запуске

## Integration Notes

### Website Integration
Для интеграции с веб-сайтом добавить ссылку с deep link:
```html
<a href="https://t.me/YOUR_BOT_USERNAME?start=site_SITENAME">
  Написать в Telegram
</a>
```
Замените `YOUR_BOT_USERNAME` и `SITENAME` на актуальные значения.

### Channel Integration
В постах канала использовать кнопку с URL:
```
https://t.me/YOUR_BOT_USERNAME?start=channel_post123
```
Можно генерировать уникальные идентификаторы постов для детальной аналитики.

## Response Language
Все ответы бота на русском языке согласно пользовательским правилам.
