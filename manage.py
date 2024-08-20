import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import dotenv_values
from database.models import async_main
from database.queries import insert_to_configs

from admins import handlers as admins
from users import handlers as users

from middleware import *

dotenv = dotenv_values(".env")


async def main() -> None:
    await async_main()
    await insert_to_configs()
    dp = Dispatcher()
    dp.message.middleware(CheckSubscription())
    bot = Bot(token=dotenv['BOT_TOKEN'], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(
        users.rt, admins.rt
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("BOT CLOSED")