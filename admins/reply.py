from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder, ReplyKeyboardMarkup

from database.queries import *

from dotenv import dotenv_values
import os

dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SYSTEM_ADMINS = [int(dotenv['ADMIN_ID_1']), int(dotenv['ADMIN_ID_2']), int(dotenv['ADMIN_ID_3'])]


async def admin_panel(chat_id):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='🛠❓ Править вопросами'))
    builder.row(KeyboardButton(text='📩 Рассылка'))
    builder.row(
        KeyboardButton(text='Изменить сообщение с контактами'),
        KeyboardButton(text='Править клавиатурой с контактами')
    )
    builder.row(KeyboardButton(text='👋 Изменить приветственное сообщение'))
    builder.row(KeyboardButton(text='👋 Изменить сообщение для новых пользователей'))
    builder.row(KeyboardButton(text='📃 Изменить описание'))
    builder.row(KeyboardButton(text='📲 Показать всех клиентов'))

    if chat_id in SYSTEM_ADMINS:
        builder.row(KeyboardButton(text='👥 Список персонала'))

    builder.row(KeyboardButton(text='⬅️ Вернуться назад'))

    return builder.as_markup(resize_keyboard=True)


async def admins_categories():
    builder = ReplyKeyboardBuilder()
    data = await get_all_categories()

    [builder.row(KeyboardButton(text=question[1])) for question in data]

    builder.row(KeyboardButton(text='➕ Добавить категорию'))
    builder.row(KeyboardButton(text='⬅️ В главное меню'))

    return builder.as_markup(resize_keyboard=True)


def cancel_operation():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='❌ Отменить действие ❌')],
        ], resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard