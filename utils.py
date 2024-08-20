from aiogram.filters import Filter
from aiogram.types import Message

import re

from database.queries import *

from dotenv import dotenv_values

dotenv = dotenv_values(".env")

SYSTEM_ADMINS = [int(dotenv['ADMIN_ID_1']), int(dotenv['ADMIN_ID_2']), int(dotenv['ADMIN_ID_3'])]


class Admin(Filter):
    async def __call__(self, message: Message) -> bool:
        admins = [admin[1] for admin in await get_all_admins()] + SYSTEM_ADMINS
        return message.from_user.id in admins


class MainAdmins(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in SYSTEM_ADMINS


class QuestionCatRequests(Filter):
    async def __call__(self, message: Message) -> bool:
        questions = [question[1] for question in await get_all_categories()]
        admins = [admin[1] for admin in await get_all_admins()] + SYSTEM_ADMINS
        return message.text in questions and message.from_user.id not in admins


class AdminQuestionCatRequests(Filter):
    async def __call__(self, message: Message) -> bool:
        questions = [question[1] for question in await get_all_categories()]
        admins = [admin[1] for admin in await get_all_admins()] + SYSTEM_ADMINS
        return message.text in questions and message.from_user.id in admins


class AnswersRequests(Filter):
    async def __call__(self, message: Message) -> bool:
        questions = await get_all_questions()
        admins = [admin[1] for admin in await get_all_admins()] + SYSTEM_ADMINS
        return message.text in questions and message.from_user.id not in admins


class AdminAnswersRequests(Filter):
    async def __call__(self, message: Message) -> bool:
        questions = await get_all_questions()
        admins = [admin[1] for admin in await get_all_admins()] + SYSTEM_ADMINS
        return message.text in questions and message.from_user.id in admins


def links_filter(message):
    url_pattern = re.compile(
        r'\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
    )
    if message:
        if url_pattern.search(message):
            return True
    return False