# 🚀 Развертывание Avtozakaz74 Bot на VPS

## 📋 Требования

- Ubuntu 20.04+ или Debian 11+
- Docker и Docker Compose (опционально)
- PostgreSQL 13+ (если не использовать Docker)
- Python 3.11+
- Git

## 🔧 Вариант 1: С помощью Docker Compose (рекомендуется)

### 1.1 Подготовка сервера

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Docker и Docker Compose
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER

# Перезагружаемся или выполняем
newgrp docker
```

### 1.2 Клонирование репозитория

```bash
cd /home/your_user
git clone <repo_url> avtozakaz-bot
cd avtozakaz-bot
```

### 1.3 Настройка переменных окружения

```bash
# Копируем пример конфигурации
cp .env.example .env

# Редактируем .env с реальными значениями
nano .env
```

**Содержимое `.env`:**
```env
# Telegram Bot
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321

# PostgreSQL
DB_USER=avtozakaz
DB_PASSWORD=your_secure_password_here
DB_NAME=avtozakaz_bot

# Окружение
ENVIRONMENT=production
```

### 1.4 Запуск с Docker Compose

```bash
# Собираем образ и запускаем контейнеры
docker-compose up -d

# Проверяем логи
docker-compose logs -f bot

# Проверяем статус
docker-compose ps
```

### 1.5 Управление

```bash
# Остановить бота
docker-compose stop bot

# Перезапустить бота
docker-compose restart bot

# Посмотреть логи
docker-compose logs -f bot

# Остановить все сервисы
docker-compose down

# Перестроить образ после обновления кода
docker-compose up -d --build
```

---

## 🐍 Вариант 2: Прямое развертывание (без Docker)

### 2.1 Установка зависимостей

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Python, PostgreSQL и необходимые пакеты
sudo apt install -y python3.11 python3.11-venv python3-pip \
                    postgresql postgresql-contrib \
                    git gcc libpq-dev

# Проверяем версию Python
python3 --version
```

### 2.2 Создание пользователя для бота

```bash
# Создаем пользователя
sudo useradd -m -s /bin/bash avtozakaz

# Переходим на этого пользователя
sudo su - avtozakaz
```

### 2.3 Клонирование репозитория

```bash
cd /home/avtozakaz
git clone <repo_url> avtozakaz-bot
cd avtozakaz-bot
```

### 2.4 Создание виртуального окружения

```bash
# Создаем venv
python3 -m venv venv

# Активируем venv
source venv/bin/activate

# Обновляем pip
pip install --upgrade pip setuptools wheel

# Устанавливаем зависимости
pip install -r requirements.txt
```

### 2.5 Настройка PostgreSQL

```bash
# Переходим в postgres
sudo su - postgres

# Входим в psql
psql

# Создаем БД и пользователя
CREATE DATABASE avtozakaz_bot;
CREATE USER avtozakaz WITH PASSWORD 'your_secure_password';
ALTER ROLE avtozakaz SET client_encoding TO 'utf8';
ALTER ROLE avtozakaz SET default_transaction_isolation TO 'read committed';
ALTER ROLE avtozakaz SET default_transaction_deferrable TO on;
ALTER ROLE avtozakaz SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE avtozakaz_bot TO avtozakaz;
\q

# Выходим из postgres
exit
```

### 2.6 Настройка переменных окружения

```bash
# Возвращаемся на пользователя avtozakaz
sudo su - avtozakaz
cd avtozakaz-bot

# Копируем .env.example
cp .env.example .env

# Редактируем .env
nano .env
```

**Содержимое `.env` для PostgreSQL:**
```env
# Telegram Bot
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321

# PostgreSQL (важно!)
DATABASE_URL=postgresql+asyncpg://avtozakaz:your_secure_password@localhost:5432/avtozakaz_bot

# Окружение
ENVIRONMENT=production
```

### 2.7 Инициализация БД

```bash
# Активируем venv если не активирован
source venv/bin/activate

# Запускаем один раз (инициализирует таблицы)
python main.py &

# Даем время на инициализацию (5-10 сек)
sleep 10

# Останавливаем (Ctrl+C или просто ждем)
kill %1
```

### 2.8 Запуск бота

```bash
# Активируем venv
source venv/bin/activate

# Запускаем бота в фоне с логированием
nohup python main.py > logs/bot.log 2>&1 &

# Или используем screen/tmux для интерактивного режима
screen -S avtozakaz_bot
source venv/bin/activate
python main.py
# Ctrl+A+D для выхода из screen
```

### 2.9 Проверка логов

```bash
# Смотрим логи в реальном времени
tail -f logs/bot.log

# Или последние 100 строк
tail -100 logs/bot.log

# Поиск ошибок
grep ERROR logs/bot.log
```

---

## 📊 Мониторинг и обслуживание

### Проверка статуса

```bash
# Проверить запущены ли процессы Python
ps aux | grep python

# Проверить использование памяти/CPU
htop
```

### Обновление кода

```bash
# Останавливаем бота
# Docker: docker-compose stop bot
# Прямой: killall python (или найти PID и kill)

cd /home/avtozakaz/avtozakaz-bot  # или ваш путь

# Обновляем код
git pull origin main

# Переустанавливаем зависимости если нужно
source venv/bin/activate
pip install -r requirements.txt

# Перезапускаем бота
nohup python main.py > logs/bot.log 2>&1 &
```

### Резервное копирование БД

```bash
# Для PostgreSQL
sudo su - postgres

# Создаем дамп БД
pg_dump -U avtozakaz avtozakaz_bot > /backups/avtozakaz_bot_$(date +%Y%m%d_%H%M%S).sql

# Восстановление если нужно
psql -U avtozakaz avtozakaz_bot < /backups/avtozakaz_bot_backup.sql
```

---

## 🐛 Решение проблем

### Проблема: БД не подключается

```bash
# Проверяем статус PostgreSQL
sudo systemctl status postgresql

# Если не запущена, запускаем
sudo systemctl start postgresql

# Проверяем соединение
psql -U avtozakaz -d avtozakaz_bot -c "SELECT 1"
```

### Проблема: Порт 5432 занят (Docker)

```bash
# Меняем в docker-compose.yml port с 5432 на другой
# Например: "5433:5432"

docker-compose restart
```

### Проблема: Бот не отвечает

```bash
# Проверяем логи
tail -f logs/bot.log

# Убиваем все python процессы
pkill -f "python main.py"

# Перезапускаем
nohup python main.py > logs/bot.log 2>&1 &
```

### Проблема: DATABASE_URL не читается

```bash
# Убедитесь что:
# 1. .env файл в корне проекта
# 2. Не коммитится в git (.gitignore должен содержать .env)
# 3. Используется правильный синтаксис для PostgreSQL:
#    postgresql+asyncpg://user:password@host:port/dbname
```

---

## 📝 Полезные команды

```bash
# Просмотр использования дискового пространства
df -h

# Очистка логов старше 30 дней
find logs -name "*.log" -mtime +30 -delete

# Проверка открытых портов
sudo netstat -tulpn | grep LISTEN

# Просмотр процессов Python
ps aux | grep python

# Килл процесса по имени
pkill -f "python main.py"
```

---

## 🔒 Безопасность

### Обязательные шаги

1. **Не коммитим `.env`** - добавлено в `.gitignore`
2. **Используем сильные пароли** - особенно для БД и BOT_TOKEN
3. **Ограничиваем доступ** - firewall должен открывать только необходимые порты
4. **Регулярно обновляем** - `git pull` и `pip install -r requirements.txt`
5. **Мониторим логи** - проверяем на ошибки и подозрительную активность

### Настройка firewall

```bash
# Если используется ufw
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP (если нужен webhook)
sudo ufw allow 443/tcp # HTTPS (если нужен webhook)

# PostgreSQL НЕ должна быть открыта (только localhost)
```

---

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `tail -f logs/bot.log`
2. Убедитесь что `.env` правильно настроен
3. Проверьте доступность PostgreSQL: `psql -U avtozakaz -d avtozakaz_bot -c "SELECT 1"`
4. Убедитесь что BOT_TOKEN правильный

---

**Версия:** 1.0  
**Последнее обновление:** 2026-01-30
