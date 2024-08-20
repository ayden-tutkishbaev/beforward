from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup

from database.queries import *


async def contacts():
    builder = InlineKeyboardBuilder()

    [builder.row(InlineKeyboardButton(text=data[1], url=data[2])) for data in await get_social_media()]

    return builder.as_markup()


change_consumer_data = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⚙️ Изменить данные', callback_data='change_consumer_data')]
    ]
)

subscribe_channel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Подписаться на канал', url='https://t.me/beforwardkorea')],
        [InlineKeyboardButton(text='Проверить подписку', callback_data='check_subscription')]
    ]
)