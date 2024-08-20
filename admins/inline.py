from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from database.queries import *


def manage_question(question_id):
    builder = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Изменить вопрос', callback_data=f'question_edit_{question_id}')],
            [InlineKeyboardButton(text='Изменить ответ', callback_data=f'answer_edit_{question_id}')],
            [InlineKeyboardButton(text='Изменить категорию', callback_data=f'change_question_cat_{question_id}')],
            [InlineKeyboardButton(text='❌ Удалить ❌', callback_data=f'question_delete_{question_id}')],
        ]
    )
    return builder


async def category_management(category_id):
    builder = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='➕ Добавить вопрос', callback_data=f'add_a_question_{category_id}')],
            [InlineKeyboardButton(text='🛠 Изменить название категории', callback_data=f'category_edit_{category_id}')],
            [InlineKeyboardButton(text='❌ Удалить', callback_data=f'category_delete_{category_id}')],
        ]
    )
    return builder


async def manage_social_media():
    builder = InlineKeyboardBuilder()

    [builder.row(InlineKeyboardButton(text=data[1], callback_data=f'edit_social_media_{data[0]}')) for data in await get_social_media()]

    builder.row(InlineKeyboardButton(text='➕ Добавить', callback_data=f'add_social_media'))

    return builder.as_markup()


async def manage_single_sm(link, sm_id):
    builder = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='▶️ Ссылка', url=link)],
            [InlineKeyboardButton(text='❌ Удалить', callback_data=f'sm_delete_{sm_id}')],
            [InlineKeyboardButton(text='⬅️ Назад', callback_data=f'back_to_social_media')],
        ]
    )
    return builder


async def delete_confirm(item_id):
    builder = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='ПОДТВЕРДИТЬ', callback_data=f'deleteconfirm_{item_id}')],
            [InlineKeyboardButton(text='❌ОТМЕНИТЬ❌', callback_data=f'categories')],
        ]
    )
    return builder


def client_delete_confirm(item_id):
    builder = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='ПОДТВЕРДИТЬ', callback_data=f'client_delete_{item_id}')],
            [InlineKeyboardButton(text='❌ОТМЕНИТЬ❌', callback_data=f'client_cancelled_{item_id}')],
        ]
    )
    return builder


async def categories_selection():
    builder = InlineKeyboardBuilder()
    data = await get_all_categories()

    [builder.row(InlineKeyboardButton(text=question[1], callback_data=f"category_{question[0]}")) for question in data]

    builder.row(InlineKeyboardButton(text='❌ Отменить действие ❌', callback_data=f"categories_cancel"))

    return builder.as_markup()


def admin_answer(sender_id):
    button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Ответить',
                                                                         callback_data=f"answer_to_{sender_id}")]])

    return button


async def admins_manage():
    keyboard = InlineKeyboardBuilder()

    [keyboard.row(InlineKeyboardButton(text=f'{worker[2]}', callback_data=f'manage_an_admin_{worker[0]}')) for worker in await get_all_admins()]

    keyboard.row(InlineKeyboardButton(text='➕ Добавить нового работника', callback_data='add_a_worker'))

    return keyboard.as_markup()


def manage_an_admin(admin_id):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='❌ Удалить работника', callback_data=f'delete_an_admin_{admin_id}'))
    keyboard.row(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'staff'))

    return keyboard.as_markup()


def delete_client(client_id):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='❌ Удалить клиента', callback_data=f'delete_a_client_{client_id}'))

    return keyboard.as_markup()