from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder, ReplyKeyboardMarkup

from database.queries import *

from dotenv import dotenv_values
import os

dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SYSTEM_ADMINS = [int(dotenv['ADMIN_ID_1']), int(dotenv['ADMIN_ID_2']), int(dotenv['ADMIN_ID_3'])]


async def main_keyboard(user_id):
    builder = ReplyKeyboardBuilder()

    builder.row(KeyboardButton(text='❓ Часто задаваемые вопросы'))
    builder.row(KeyboardButton(text='📃 О нас'), KeyboardButton(text='📞 Наши контакты'))
    builder.row(KeyboardButton(text='👤 Ваш профиль'))

    if user_id in [admin[1] for admin in await get_all_admins()] + SYSTEM_ADMINS:
        builder.row(KeyboardButton(text='🔐 Административная панель'))

    return builder.as_markup(resize_keyboard=True)


async def questions_categories_keyboard():
    builder = ReplyKeyboardBuilder()
    data = await get_all_categories()

    [builder.row(KeyboardButton(text=question[1])) for question in data]
    builder.row(KeyboardButton(text='🙋‍♂️ Задать свой вопрос'))
    builder.row(KeyboardButton(text='⬅️ В главное меню'))

    return builder.as_markup(resize_keyboard=True)


async def categories_questions_keyboard(category_id):
    builder = ReplyKeyboardBuilder()
    data = await get_questions_by_category(category_id)

    [builder.row(KeyboardButton(text=question[0])) for question in data]

    builder.row(KeyboardButton(text='🙋‍♂️ Задать свой вопрос'))
    builder.row(KeyboardButton(text='⬅️ К категориям'))

    return builder.as_markup(resize_keyboard=True)


async def admins_categories_questions_keyboard(category_id):
    builder = ReplyKeyboardBuilder()
    data = await get_questions_by_category(category_id)

    [builder.row(KeyboardButton(text=question[0])) for question in data]

    builder.row(KeyboardButton(text='⬅️ К категориям'))

    return builder.as_markup(resize_keyboard=True)


def contact_number():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📱 Поделиться контактом', request_contact=True)]
        ], resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard