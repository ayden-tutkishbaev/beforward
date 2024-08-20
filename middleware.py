from typing import Dict, Awaitable, Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

import users.inline as il

from database.queries import get_configs_data

from dotenv import dotenv_values

dotenv = dotenv_values(".env")

CHANNEL_ID = int(dotenv['CHANNEL_LINK'])


class CheckSubscription(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        member = await event.bot.get_chat_member(CHANNEL_ID, event.from_user.id)

        messages = await get_configs_data()

        if member.status == 'left':
            await event.answer(f"{messages[4]}", reply_markup=il.subscribe_channel)
        else:
            return await handler(event, data)
