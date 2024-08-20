from sqlalchemy import ForeignKey, BigInteger, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from typing import List

from dotenv import dotenv_values
import os


dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

engine = create_async_engine(url=dotenv['DB_URL'], echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    ...


class Configs(Base):
    __tablename__ = 'configs'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contacts: Mapped[str] = mapped_column(Text)
    about_us: Mapped[str] = mapped_column(Text)
    welcome_message: Mapped[str] = mapped_column(Text)
    new_comers: Mapped[str] = mapped_column(Text)


class QuestionCategory(Base):
    __tablename__ = 'question_categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(Text)
    question_rel: Mapped[List['FrequentlyAskedQuestions']] = relationship(back_populates='category_rel',
                                                                          cascade="all, delete", passive_deletes=True)


class FrequentlyAskedQuestions(Base):
    __tablename__ = 'question_and_answer'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    category: Mapped[int] = mapped_column(ForeignKey('question_categories.id', ondelete='CASCADE'))
    category_rel: Mapped['QuestionCategory'] = relationship(back_populates='question_rel')


class SocialMedia(Base):
    __tablename__ = 'social_media'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    social_media_name: Mapped[str] = mapped_column(Text)
    link: Mapped[str] = mapped_column(Text)


class Staff(Base):
    __tablename__ = 'staff'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(240))


class Consumers(Base):
    __tablename__ = 'consumers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    telegram_name: Mapped[str] = mapped_column(String(240), nullable=True)
    full_name: Mapped[str] = mapped_column(String(240), nullable=True)
    contact: Mapped[str] = mapped_column(String(240), nullable=True)


class DoneConsumers(Base):
    __tablename__ = 'done_consumers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    telegram_name: Mapped[str] = mapped_column(String(240), nullable=True)
    full_name: Mapped[str] = mapped_column(String(240), nullable=True)
    contact: Mapped[str] = mapped_column(String(240), nullable=True)



async def async_main():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


