from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

from aiogram.fsm.context import FSMContext

from database.queries import *

from states import *
from utils import *

import admins.reply as rp
import users.reply as urp

import admins.inline as il

from dotenv import dotenv_values
import os

dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

rt = Router()


@rt.message(Admin(), F.text.in_(["🔐 Административная панель", "/admin", "⬅️ Назад"]))
async def command_start_handler(message: Message):
    await message.answer(f"Вы вошли в административную панель", reply_markup=await rp.admin_panel(message.chat.id))


@rt.message(Admin(), F.text == '⬅️ Вернуться назад')
async def back_to_main_menu(message: Message):
    await message.answer("Вы вернулись в общее главное меню", reply_markup=await urp.main_keyboard(message.chat.id))


@rt.message(Admin(), F.text == '📃 Изменить описание')
async def alter_about_us_message(message: Message, state: FSMContext):
    await message.answer("Отправьте новое описание:", reply_markup=rp.cancel_operation())
    await state.set_state(AlterAboutUs.confirmation)


@rt.message(Admin(), AlterAboutUs.confirmation)
async def insert_new_description_message(message: Message, state: FSMContext):
    if message.text == "❌ Отменить действие ❌":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await rp.admin_panel(message.chat.id))
    else:
        await state.clear()
        await state.set_state(AlterAboutUs.message)
        await state.update_data(message=message.text)
        new_message = await state.get_data()
        print(new_message['message'])
        await insert_new_description(new_message['message'])
        await message.answer("Описание изменено успешно!", reply_markup=await rp.admin_panel(message.chat.id))


@rt.message(Admin(), F.text == 'Изменить сообщение с контактами')
async def alter_contact_message(message: Message, state: FSMContext):
    await message.answer("Отправьте новое сообщение:", reply_markup=rp.cancel_operation())
    await state.set_state(AlterContact.confirmation)


@rt.message(Admin(), AlterContact.confirmation)
async def insert_new_contact_message(message: Message, state: FSMContext):
    if message.text == "❌ Отменить действие ❌":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await rp.admin_panel(message.chat.id))
    else:
        await state.clear()
        await state.set_state(AlterContact.message)
        await state.update_data(message=message.text)
        new_message = await state.get_data()
        print(new_message['message'])
        await insert_new_contact(new_message['message'])
        await message.answer("Сообщение с контактами изменено успешно!", reply_markup=await rp.admin_panel(message.chat.id))


@rt.message(Admin(), F.text == '👋 Изменить приветственное сообщение')
async def alter_welcome_message(message: Message, state: FSMContext):
    await message.answer("Отправьте новое сообщение:", reply_markup=rp.cancel_operation())
    await state.set_state(AlterWelcomeMessage.message)


@rt.message(Admin(), AlterWelcomeMessage.message)
async def insert_new_welcome_message(message: Message, state: FSMContext):
    if message.text == "❌ Отменить действие ❌":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await rp.admin_panel(message.chat.id))
    else:
        await state.clear()
        await state.set_state(AlterWelcomeMessage.message)
        await state.update_data(message=message.text)
        new_message = await state.get_data()
        await insert_new_w_message(new_message['message'])
        await state.clear()
        await message.answer("Приветственное сообщение изменено успешно!", reply_markup=await rp.admin_panel(message.chat.id))


@rt.message(Admin(), F.text == '👋 Изменить сообщение для новых пользователей')
async def alter_welcome_message(message: Message, state: FSMContext):
    await message.answer("Отправьте новое сообщение:", reply_markup=rp.cancel_operation())
    await state.set_state(AlterNewComersMessage.message)


@rt.message(Admin(), AlterNewComersMessage.message)
async def insert_new_welcome_message(message: Message, state: FSMContext):
    if message.text == "❌ Отменить действие ❌":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await rp.admin_panel(message.chat.id))
    else:
        await state.clear()
        await state.set_state(AlterNewComersMessage.message)
        await state.update_data(message=message.text)
        new_message = await state.get_data()
        await insert_new_comers_message(new_message['message'])
        await state.clear()
        await message.answer("Приветственное сообщение изменено успешно!", reply_markup=await rp.admin_panel(message.chat.id))


@rt.message(Admin(), F.text == '🛠❓ Править вопросами')
async def manage_faq(message: Message):
    await message.answer("Категории часто задаваемых вопросов", reply_markup=await rp.admins_categories())


@rt.message(Admin(), F.text == '➕ Добавить категорию')
async def add_a_category(message: Message, state: FSMContext):
    await message.answer("Отправьте название новой категории: ", reply_markup=rp.cancel_operation())
    await state.set_state(CategoryAddition.category)


@rt.message(Admin(), CategoryAddition.category)
async def insert_category_handler(message: Message, state: FSMContext):
    if message.text == "❌ Отменить действие ❌":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await rp.admins_categories())
    else:
        await insert_category(message.text)
        await state.clear()
        await message.answer("Категория добавлена успешно!", reply_markup=await rp.admins_categories())


@rt.callback_query(Admin(), F.data.startswith('add_a_question_'))
async def add_a_question(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split('_')[-1])
    await state.set_state(FAQaddition.category)
    await state.update_data(category=category_id)
    await callback.message.delete()
    await callback.message.answer("Отправьте вопрос: ", reply_markup=rp.cancel_operation())
    await state.set_state(FAQaddition.question)


@rt.message(Admin(), FAQaddition.question)
async def question_added(message: Message, state: FSMContext):
    if message.text == "❌ Отменить действие ❌":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await rp.admins_categories())
    else:
        await state.set_state(FAQaddition.question)
        await state.update_data(question=message.text)
        await message.answer("Теперь отправьте на него ответ: ")
        await state.set_state(FAQaddition.answer)


@rt.message(Admin(), FAQaddition.answer)
async def add_answer(message: Message, state: FSMContext):
    await state.set_state(FAQaddition.answer)
    await state.update_data(answer=message.text)
    # await message.answer("Отправьте фото, если их нужно приложить к ответу\nНажмите на «ЗАВЕРШИТЬ», если этого не требуется.")
    await message.answer("Вопрос и ответ на него успешно добавлен!", reply_markup=await rp.admins_categories())
    data = await state.get_data()
    print(data)
    await insert_faq(data['question'], data['answer'], data['category'])
    await state.clear()


@rt.message(Admin(), F.text == 'watch db')
async def watch_db(message: Message):
    data = await get_configs_data()
    print(data)

# @rt.message(Admin(), FAQaddition.photo, F.photo)
# async def add_photos(message: Message, state: FSMContext):
#     data = await state.get_data()
#     photos = data.get("photo", [])
#     photos.append(message.photo[-1].file_id)
#     await state.update_data(photo=photos)
#     await message.answer("Фотография добавлена. Добавьте еще или завершите кнопкой «ЗАВЕРШИТЬ» ниже.")


# @rt.message(Admin(), F.text == 'ЗАВЕРШИТЬ')
# async def insert_new_category(message: Message, state: FSMContext):
#     data = await state.get_data()
#     print(data)
#     name = data.get("name")
#     description = data.get("description")
#     photos = data.get("photos", [])
#
#     await state.clear()

@rt.message(AdminQuestionCatRequests())
async def manage_categories(message: Message):
    category_id = int(await get_id_of_category(message.text))
    await message.answer(f"Управление категорией:", reply_markup=await urp.admins_categories_questions_keyboard(category_id))
    await message.answer(f"{message.text}", reply_markup=await il.category_management(category_id))


@rt.callback_query(Admin(), F.data.startswith("category_edit_"))
async def edit_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split('_')[-1])
    await state.set_state(AlterCategory.id)
    await state.update_data(id=category_id)
    await state.set_state(AlterCategory.category)
    await callback.message.delete()
    await callback.message.answer("Отправьте новое название категории", reply_markup=rp.cancel_operation())


@rt.message(AlterCategory.category)
async def apply_changes_category(message: Message, state: FSMContext):
    if message.text == '❌ Отменить действие ❌':
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await rp.admins_categories())
    else:
        await state.update_data(category=message.text)
        data = await state.get_data()
        await alter_category_title(data['category'], data['id'])
        await message.answer("Категория изменена", reply_markup=await rp.admins_categories())
        await state.clear()


@rt.callback_query(Admin(), F.data.startswith('category_delete_'))
async def category_deletion(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[-1])
    await callback.message.edit_text("Вы уверены в том, что хотите удалить эту категорию?\n\nВопросы с ней тоже удалятся!",
                                           reply_markup=await il.delete_confirm(category_id))


@rt.callback_query(Admin(), F.data.startswith('deleteconfirm_'))
async def category_deletion_confirmed(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[-1])
    await delete_category(category_id)
    await callback.message.delete()
    await callback.message.answer("Удалено успешно!", reply_markup=await rp.admins_categories())


@rt.callback_query(Admin(), F.data == 'categories')
async def cancelled_action(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Вы вернулись к категориям", reply_markup=await rp.admins_categories())


@rt.message(Admin(), F.text == '⬅️ К категориям')
async def back_to_categories(message: Message):
    await message.answer("Вы вернулись к категориям", reply_markup=await rp.admins_categories())


@rt.message(AdminAnswersRequests())
async def answer_message(message: Message):
    answer = await get_answer_by_question(message.text)
    question_id = await get_question_id(message.text)
    await message.answer(f"{answer}", reply_markup=il.manage_question(question_id))


@rt.callback_query(Admin(), F.data.startswith('question_edit_'))
async def question_edit(callback: CallbackQuery, state: FSMContext):
    question_id = callback.data.split("_")[-1]
    await state.set_state(AlterQuestion.id)
    await state.update_data(id=int(question_id))
    await state.set_state(AlterQuestion.question)
    await callback.message.delete()
    await callback.message.answer("Отправьте измененный вопрос", reply_markup=rp.cancel_operation())


@rt.message(Admin(), AlterQuestion.question)
async def question_update(message: Message, state: FSMContext):
    if message.text == "❌ Отменить действие ❌":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await rp.admins_categories())
    else:
        await state.update_data(question=message.text)
        data = await state.get_data()
        await alter_question(data['id'], data['question'])
        await message.answer("Вопрос изменён", reply_markup=await rp.admins_categories())


@rt.callback_query(Admin(), F.data.startswith('change_question_cat_'))
async def change_question_category(callback: CallbackQuery, state: FSMContext):
    question_id = callback.data.split("_")[-1]
    await state.set_state(AlterFAQcategory.id)
    await state.update_data(id=int(question_id))
    await state.set_state(AlterFAQcategory.category)
    await callback.message.delete()
    await callback.message.answer("Выберите новую категорию вопроса:", reply_markup=await il.categories_selection())


@rt.callback_query(AlterFAQcategory.category)
async def apply_changes_to_categories_switch(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'categories_cancel':
        await state.clear()
        await callback.message.delete()
        await callback.message.answer("Вы вернулись к категориям", reply_markup=await rp.admins_categories())
    else:
        await state.update_data(category=int(callback.data.split("_")[-1]))
        data = await state.get_data()
        await alter_category(data['id'], data['category'])
        await callback.message.delete()
        await callback.message.answer("Категория вопроса изменена!", reply_markup=await rp.admins_categories())
        await state.clear()


@rt.callback_query(Admin(), F.data.startswith('answer_edit_'))
async def answer_delete(callback: CallbackQuery, state: FSMContext):
    question_id = callback.data.split("_")[-1]
    await state.set_state(AlterAnswer.id)
    await state.update_data(id=int(question_id))
    await state.set_state(AlterAnswer.answer)
    await callback.message.delete()
    await callback.message.answer("Отправьте измененный ответ", reply_markup=rp.cancel_operation())


@rt.message(Admin(), AlterAnswer.answer)
async def answer_update(message: Message, state: FSMContext):
    if message.text == "❌ Отменить действие ❌":
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await rp.admins_categories())
    else:
        await state.update_data(answer=message.text)
        data = await state.get_data()
        await alter_answer(data['id'], data['answer'])
        await message.answer("Ответ изменён", reply_markup=await rp.admins_categories())
        await state.clear()


@rt.callback_query(F.data.startswith('question_delete_'))
async def question_delete(callback: CallbackQuery):
    question_id = callback.data.split("_")[-1]
    await delete_question(int(question_id))
    await callback.message.delete()
    await callback.message.answer("Вопрос удалён", reply_markup=await rp.admins_categories())


@rt.message(Admin(), F.text == 'Править клавиатурой с контактами')
async def social_media(message: Message):
    await message.answer("Ваши соцсети:", reply_markup=await il.manage_social_media())


@rt.callback_query(Admin(), F.data == 'add_social_media')
async def add_social_media(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(SocialMediaAddition.name)
    await callback.message.answer("Отправьте название вашей соцсети", reply_markup=rp.cancel_operation())


@rt.message(Admin(), SocialMediaAddition.name)
async def add_social_media_name(message: Message, state: FSMContext):
    if message.text == '❌ Отменить действие ❌':
        await state.clear()
        await message.answer('Действие отменено', reply_markup=await rp.admin_panel(message.chat.id))
    else:
        await state.update_data(name=message.text)
        await state.set_state(SocialMediaAddition.link)
        await message.answer("Отправьте ссылку на вашу соцсеть")


@rt.message(Admin(), SocialMediaAddition.link)
async def add_social_media_link(message: Message, state: FSMContext):
    if not links_filter(message.text):
        await message.answer("Отправьте ссылку")
    else:
        await state.update_data(link=message.text)
        data = await state.get_data()
        await insert_social_media(data['name'], data['link'])
        await message.answer("Ссылка на соцсети добавлена успешно!", reply_markup=await rp.admin_panel(message.chat.id))
        await state.clear()


@rt.callback_query(Admin(), F.data.startswith('edit_social_media_'))
async def single_social_media(callback: CallbackQuery):
    sm_id = int(callback.data.split('_')[-1])
    print(sm_id)
    data = await get_social_media_by_id(sm_id)
    await callback.message.edit_text(f"{data[0]}", reply_markup=await il.manage_single_sm(data[1], sm_id))


@rt.callback_query(Admin(), F.data == 'back_to_social_media')
async def back_to_social_media(callback: CallbackQuery):
    await callback.message.edit_text("Ваши соцсети:", reply_markup=await il.manage_social_media())


@rt.callback_query(Admin(), F.data.startswith('sm_delete_'))
async def sm_delete(callback: CallbackQuery):
    sm_id = int(callback.data.split('_')[-1])
    await delete_social_media(sm_id)
    await get_social_media_by_id(sm_id)
    await callback.message.edit_text("Соцсеть удалена", reply_markup=await il.manage_social_media())


@rt.callback_query(Admin(), F.data.startswith("answer_to_"))
async def answer_asked_question(callback: CallbackQuery, state: FSMContext):
    receiver = int(callback.data.split("_")[2])
    await state.set_state(QuestionAnswer.to)
    await state.update_data(to=receiver)
    await state.set_state(QuestionAnswer.message)
    await callback.message.answer("Отправьте ответ на заданный вопрос пользователя:")


@rt.message(Admin(), QuestionAnswer.message)
async def send_answer_to_asked_question(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if message.text == '❌ Отменить действие ❌':
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await rp.admin_panel(message.chat.id))
    else:
        try:
            await bot.send_message(chat_id=data['to'], text=f"⬇️ <b>Вы получили ответ на свой вопрос!</b>")
            await message.send_copy(chat_id=data['to'])
            await state.clear()
            await message.answer("Отправлено успешно!", reply_markup=await rp.admin_panel(message.chat.id))
        except:
            await message.answer("При отправке ответа на вопрос произошла неизвестная ошибка. Попробуйте позже!",
                                 reply_markup=await rp.admin_panel(message.chat.id))
            await state.clear()


@rt.message(MainAdmins(), F.text == '👥 Список персонала')
async def administration_manage(message: Message):
    await message.answer("Список персонала:", reply_markup=await il.admins_manage())


@rt.callback_query(MainAdmins(), F.data == 'staff')
async def administration_manage(callback: CallbackQuery):
    await callback.message.answer("Список персонала:", reply_markup=await il.admins_manage())


@rt.callback_query(MainAdmins(), F.data.startswith('manage_an_admin_'))
async def manage_admin(callback: CallbackQuery):
    admin_id = int(callback.data.split('_')[-1])
    data = await get_an_admin_by_id(admin_id)
    await callback.message.edit_text(f"{data[0]}, {data[1]}", reply_markup=il.manage_an_admin(admin_id))


@rt.callback_query(MainAdmins(), F.data.startswith('delete_an_admin_'))
async def delete_worker_handler(callback: CallbackQuery):
    admin_id = int(callback.data.split('_')[-1])
    await remove_admin(admin_id)
    await callback.message.edit_text("Работник удалён", reply_markup=await il.admins_manage())


@rt.callback_query(MainAdmins(), F.data == 'add_a_worker')
async def add_a_worker(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StaffAdd.telegram_id)
    await callback.message.answer("Отправьте Telegram ID работника, для которого вы хотите открыть доступ в админ-панель:\nОн может его взять через https://t.me/getmyid_bot",
                                  reply_markup=rp.cancel_operation())


@rt.message(MainAdmins(), StaffAdd.telegram_id)
async def ask_workers_name(message: Message, state: FSMContext):
    if message.text == '❌ Отменить действие ❌':
        await state.clear()
        await message.answer("Действие отменено", reply_markup=await il.admins_manage())
    else:
        await state.update_data(telegram_id=int(message.text))
        await state.set_state(StaffAdd.name)
        await message.answer("Отправьте имя работника")


@rt.message(MainAdmins(), StaffAdd.name)
async def apply_change_to_staff(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await insert_staff(data['telegram_id'], data['name'])
    await message.answer("Работник добавлен успешно!", reply_markup=await rp.admin_panel(message.chat.id))
    await state.clear()


@rt.message(Admin(), F.text == '📲 Показать всех клиентов')
async def display_all_clients(message: Message):
    all_clients = await get_all_done_consumers()
    for client in all_clients:
        await message.answer(f"{client[2]}\n\n<b>Имя</b>\n<i>{client[3]}</i>\n<b>Контактный номер телефона</b>\n<i>{client[4]}</i>",
                             reply_markup=il.delete_client(client[0]))
    await message.answer("⬆️ <b>Все клиенты представлены выше</b>")


@rt.callback_query(Admin(), F.data.startswith('delete_a_client_'))
async def delete_a_client_confirm(callback: CallbackQuery):
    client_id = int(callback.data.split('_')[-1])
    await callback.message.edit_text("Вы уверены, что хотите удалить клиента из вашей базы?",
                                           reply_markup=il.client_delete_confirm(client_id))


@rt.callback_query(Admin(), F.data.startswith('client_delete_'))
async def delete_a_client_handler(callback: CallbackQuery):
    client_id = int(callback.data.split('_')[-1])
    await delete_a_client(client_id)
    await callback.message.edit_text("Клиент удален успешно!")


@rt.callback_query(Admin(), F.data.startswith('client_cancelled'))
async def cancel_deletion(callback: CallbackQuery):
    client_id = int(callback.data.split('_')[-1])
    client = await get_a_done_consumer(client_id)
    await callback.message.edit_text(
        f"{client[2]}\n\n<b>Имя</b>\n<i>{client[3]}</i>\n<b>Контактный номер телефона</b>\n<i>{client[4]}</i>",
        reply_markup=il.delete_client(client[0]))


@rt.message(Admin(), F.text == '📩 Рассылка')
async def newsletter(message: Message, state: FSMContext) -> None:
    await state.set_state(NewsLetter.message)
    await message.answer('Отправьте ваше сообщение, которое хотите разослать всем пользователям бота',
                         reply_markup=rp.cancel_operation())


@rt.message(Admin(), NewsLetter.message)
async def sending_to_all(message: Message, state: FSMContext) -> None:
    users = await get_all_consumers()
    if message.text in '❌ Отменить действие ❌':
        await state.clear()
        await message.answer('Действие отменено',
                                reply_markup=await rp.admin_panel(message.chat.id))
    else:
        for user in users:
            try:
                await message.send_copy(chat_id=user)
            except:
                pass
        await message.answer('Сообщение было разослано всем успешно!', reply_markup=await rp.admin_panel(message.chat.id))
        await state.clear()