"""Модели базы данных."""

from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime, Text, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""
    pass


class User(Base):
    """Модель пользователя."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.telegram_id} (@{self.username})>"


class Conversation(Base):
    """Модель текущего диалога пользователя."""
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=True)  # 'channel', 'site'
    source_detail: Mapped[str] = mapped_column(String(255), nullable=True)  # название сайта или ID поста
    state: Mapped[str] = mapped_column(String(50), nullable=True)  # текущее состояние FSM
    budget: Mapped[str] = mapped_column(String(255), nullable=True)
    preferences: Mapped[str] = mapped_column(Text, nullable=True)
    timeline: Mapped[str] = mapped_column(String(255), nullable=True)
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Conversation {self.user_id} from {self.source}>"


class Lead(Base):
    """Модель готового лида (завершенного диалога)."""
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(String(50), nullable=True)
    source_detail: Mapped[str] = mapped_column(String(255), nullable=True)
    budget: Mapped[str] = mapped_column(String(255), nullable=True)
    preferences: Mapped[str] = mapped_column(Text, nullable=True)
    timeline: Mapped[str] = mapped_column(String(255), nullable=True)
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Lead {self.id} from @{self.username}>"
