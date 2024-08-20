from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

import users.reply as rp
import admins.inline as ail
import users.inline as il
import admins.reply as akb

from states import *

from utils import QuestionCatRequests, AnswersRequests

from database.queries import *

from dotenv import dotenv_values
import os

dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SYSTEM_ADMINS = [int(dotenv['ADMIN_ID_1']), int(dotenv['ADMIN_ID_2']), int(dotenv['ADMIN_ID_3'])]


CHANNEL_ID = int(dotenv['CHANNEL_LINK'])

rt = Router()


@rt.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    data = await get_configs_data()
    await message.answer(f"{data[3]}")
    if message.chat.id in await get_all_consumers():
        await message.answer(f"Что пожелаете?", reply_markup=await rp.main_keyboard(message.chat.id))
    else:
        await state.set_state(UserRegistration.contact)
        # await message.answer(f"{data[4]}", reply_markup=il.subscribe_channel)
        await message.answer("📞 Отправьте ваш контактный номер телефона", reply_markup=rp.contact_number())


@rt.callback_query(F.data == 'check_subscription')
async def check_subscription(callback: CallbackQuery, state: FSMContext):
    member = await callback.message.bot.get_chat_member(CHANNEL_ID, callback.message.from_user.id)
    messages = await get_configs_data()

    if member.status == 'left':
        await callback.message.answer(f"{messages[4]}", reply_markup=il.subscribe_channel)
    else:
        await command_start_handler(callback.message, state)


@rt.message(UserRegistration.contact)
async def get_contact_handler(message: Message, state: FSMContext):
    if message.chat.id not in await get_all_consumers():
        await insert_consumer_data(message.chat.id, message.from_user.full_name)
        await insert_consumer_data_to_double_table(message.chat.id, message.from_user.full_name)
    if message.contact:
        await state.update_data(contact=f'{message.contact.phone_number}')
    elif message.text:
        await state.update_data(contact=message.text)
    await state.set_state(UserRegistration.full_name)
    await message.answer('👤 Как вас зовут?')


@rt.message(UserRegistration.full_name)
async def get_fullname(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    await insert_other_consumer_data(message.chat.id, data['contact'], data['full_name'])
    await insert_other_consumer_data_to_double_table(message.chat.id, data['contact'], data['full_name'])
    await message.answer('✅ Регистрация пройдена успешно!')
    await message.answer(f"Что пожелаете?", reply_markup=await rp.main_keyboard(message.chat.id))
    await state.clear()


@rt.message(F.text == "⬅️ В главное меню")
async def back_to_main_menu(message: Message):
    await message.answer(f"⬅️ Вы вернулись в главное меню ", reply_markup=await rp.main_keyboard(message.chat.id))


@rt.message(F.text == '📞 Наши контакты')
async def contact_links(message: Message) -> None:
    data = await get_configs_data()
    await message.answer(f"{data[1]}", reply_markup=await il.contacts())


@rt.message(F.text == '📃 О нас')
async def contact_links(message: Message) -> None:
    data = await get_configs_data()
    await message.answer(f"{data[2]}")


@rt.message(F.text == '❓ Часто задаваемые вопросы')
async def contact_links(message: Message) -> None:
    await message.answer("❓ Категории часто задаваемых вопросов", reply_markup=await rp.questions_categories_keyboard())


@rt.message(QuestionCatRequests())
async def answer_message(message: Message):
    category_id = await get_id_of_category(message.text)
    await message.answer(f"❓ Часто задаваемые вопросы представлены ниже",
                         reply_markup=await rp.categories_questions_keyboard(int(category_id)))


@rt.message(AnswersRequests())
async def answer_questions(message: Message):
    answer = await get_answer_by_question(message.text)
    await message.answer(f"{answer}")


@rt.message(F.text == '⬅️ К категориям')
async def back_to_categories(message: Message):
    await message.answer("Вы вернулись к категориям", reply_markup=await rp.questions_categories_keyboard())


@rt.message(F.text == '🙋‍♂️ Задать свой вопрос')
async def ask_my_question(message: Message, state: FSMContext):
    await state.set_state(OtherQuestions.message)
    await message.answer("📨 Отправьте интересующий вас вопрос:",
                         reply_markup=akb.cancel_operation())


@rt.message(OtherQuestions.message)
async def send_question(message: Message, state: FSMContext, bot: Bot):
    if message.text == "❌ Отменить действие ❌":
        await state.clear()
        await message.answer("❌ Действие отменено", reply_markup=await rp.questions_categories_keyboard())
    else:
        try:
            for user in SYSTEM_ADMINS + [admin[1] for admin in await get_all_admins()]:
                if message.from_user.username:
                    await bot.send_message(chat_id=user,
                                           text=f"⬇️ <b>Вам был задан вопрос от пользователя @{message.from_user.username}!</b>")
                else:
                    await bot.send_message(chat_id=user,
                                           text=f"⬇️ <b>Вам был задан вопрос от пользователя <i>{message.from_user.full_name}</i>!</b>")
                await message.send_copy(chat_id=user, reply_markup=ail.admin_answer(message.chat.id))
            await message.answer('✅ Вопрос был успешно отправлен! Наши администраторы ответят на него как можно скорее!',
                                 reply_markup=await rp.questions_categories_keyboard())
            await state.clear()
        except:
            await message.answer("При отправке вопроса произошла неизвестная ошибка. Попробуйте позже!",
                                 reply_markup=await rp.questions_categories_keyboard())
            await state.clear()


@rt.message(F.text == '👤 Ваш профиль')
async def my_data(message: Message):
    consumer_data = await get_consumer_data(message.chat.id)
    await message.answer(f"{consumer_data[0]},\n\n👤<b>Ваше имя</b>\n<i>{consumer_data[1]}</i>\n📞<b>Ваш контактный номер телефона</b>\n<i>{consumer_data[2]}</i>",
                         reply_markup=il.change_consumer_data)


@rt.callback_query(F.data == 'change_consumer_data')
async def alter_consumer_data(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AlterConsumerData.contact)
    await callback.message.answer("📞 Отправьте ваш контактный номер телефона", reply_markup=rp.contact_number())


@rt.message(AlterConsumerData.contact)
async def change_contact_data(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(contact=f'{message.contact.phone_number}')
    elif message.text:
        await state.update_data(contact=message.text)
    await state.set_state(AlterConsumerData.full_name)
    await message.answer('👤 Как вас зовут?', reply_markup=akb.cancel_operation())


@rt.message(AlterConsumerData.full_name)
async def get_fullname(message: Message, state: FSMContext):
    if message.text == '❌ Отменить действие ❌':
        await state.clear()
        await message.answer("❌ Действие отменено", reply_markup=await rp.main_keyboard(message.chat.id))
    else:
        await state.update_data(full_name=message.text)
        data = await state.get_data()
        await insert_other_consumer_data(message.chat.id, data['contact'], data['full_name'])
        await insert_other_consumer_data_to_double_table(message.chat.id, data['contact'], data['full_name'])
        await message.answer('✅ Данные успешно изменены!', reply_markup=await rp.main_keyboard(message.chat.id))
        await state.clear()