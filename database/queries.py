from database.models import *

from sqlalchemy import select, update, delete, text


async def insert_to_configs():
    async with async_session() as connect:
        query = """
        INSERT INTO configs(contacts, about_us, welcome_message, new_comers)
        VALUES ('(your message)', '(your message)', '(your message)', '(your message)')
        """
        await connect.execute(text(query))
        await connect.commit()


async def insert_new_description(new_description: str):
    async with async_session() as connect:
        query = """
        UPDATE configs
        SET about_us = :new_description
        WHERE id = 1
        """
        await connect.execute(text(query), {"new_description": new_description})
        await connect.commit()


async def insert_new_contact(new_contacts: str):
    async with async_session() as connect:
        query = """
        UPDATE configs
        SET contacts = :new_contacts
        WHERE id = 1
        """
        await connect.execute(text(query), {"new_contacts": new_contacts})
        await connect.commit()


async def insert_new_w_message(new_message: str):
    async with async_session() as connect:
        query = """
        UPDATE configs
        SET welcome_message = :new_message
        WHERE id = 1
        """
        await connect.execute(text(query), {"new_message": new_message})
        await connect.commit()


async def insert_new_comers_message(new_message: str):
    async with async_session() as connect:
        query = """
        UPDATE configs
        SET new_comers = :new_message
        WHERE id = 1
        """
        await connect.execute(text(query), {"new_message": new_message})
        await connect.commit()


async def get_configs_data():
    async with async_session() as connect:
        configs = await connect.execute(text("SELECT * FROM configs WHERE id = 1"))
        return configs.fetchone()


async def insert_faq(question, answer, category: str):
    async with async_session() as connect:
        query = """
        INSERT INTO question_and_answer(question, answer, category)
        VALUES (:question, :answer, :category)
        """
        await connect.execute(text(query), {"question": question, "answer": answer, "category": category})
        await connect.commit()


async def get_all_categories():
    async with async_session() as connect:
        query = """
        SELECT * FROM question_categories
        ORDER BY id
        """
        data = await connect.execute(text(query))
        return data.fetchall()


async def get_id_of_category(category):
    async with async_session() as connect:
        query = """
        SELECT id FROM question_categories
        WHERE category = :category
        """
        data = await connect.execute(text(query), {'category': category})
        return data.fetchone()[0]


async def alter_category_title(new_category, category_id):
    async with async_session() as connect:
        query = """
        UPDATE question_categories
        SET category = :new_category
        WHERE id = :category_id
        """
        await connect.execute(text(query), {'new_category': new_category, 'category_id': category_id})
        await connect.commit()


async def get_questions_by_category(category_id):
    async with async_session() as connect:
        query = """
        SELECT question FROM question_and_answer
        WHERE category = :category_id
        """
        data = await connect.execute(text(query), {'category_id': category_id})
        return data.fetchall()


async def get_answer_by_question(question):
    async with async_session() as connect:
        query = """
        SELECT answer FROM question_and_answer
        WHERE question = :question
        """
        data = await connect.execute(text(query), {'question': question})
        return data.fetchone()[0]


async def insert_category(title):
    async with async_session() as connect:
        query = """
        INSERT INTO question_categories (category)
        VALUES (:category_title) 
        """
        await connect.execute(text(query), {'category_title': title})
        await connect.commit()


async def delete_category(category):
    async with async_session() as connect:
        query = """
        DELETE FROM question_categories
        WHERE id = :category
        """
        await connect.execute(text(query), {'category': category})
        await connect.commit()


async def get_all_questions():
    async with async_session() as connect:
        query = """
        SELECT question FROM question_and_answer
        """
        data = await connect.execute(text(query))
        questions = data.fetchall()
        return [question[0] for question in questions]


async def get_question_id(question):
    async with async_session() as connect:
        query = """
        SELECT id FROM question_and_answer
        WHERE question = :question
        """
        data = await connect.execute(text(query), {'question': question})
        return data.fetchone()[0]


async def alter_question(question_id, question):
    async with async_session() as connect:
        query = """
        UPDATE question_and_answer
        SET question = :question
        WHERE id = :id
        """
        await connect.execute(text(query), {'question': question, 'id': question_id})
        await connect.commit()


async def alter_answer(question_id, answer):
    async with async_session() as connect:
        query = """
        UPDATE question_and_answer
        SET answer = :answer
        WHERE id = :id
        """
        await connect.execute(text(query), {'answer': answer, 'id': question_id})
        await connect.commit()


async def alter_category(question_id, category):
    async with async_session() as connect:
        query = """
        UPDATE question_and_answer
        SET category = :category
        WHERE id = :id
        """
        await connect.execute(text(query), {'category': category, 'id': question_id})
        await connect.commit()


async def delete_question(question_id):
    async with async_session() as connect:
        query = """
        DELETE FROM question_and_answer WHERE id = :id;
        """
        await connect.execute(text(query), {'id': question_id})
        await connect.commit()


async def insert_social_media(social_media_name, link):
    async with async_session() as connect:
        query = """
        INSERT INTO social_media(social_media_name, link)
        VALUES(:social_media_name, :link)
        """
        await connect.execute(text(query), {'social_media_name': social_media_name, 'link': link})
        await connect.commit()


async def get_social_media():
    async with async_session() as connect:
        query = """
        SELECT * FROM social_media
        """
        data = await connect.execute(text(query))
        return data.fetchall()


async def get_social_media_by_id(sm_id):
    async with async_session() as connect:
        query = """
        SELECT social_media_name, link FROM social_media
        WHERE id = :sm_id
        """
        data = await connect.execute(text(query), {'sm_id': sm_id})
        return data.fetchone()


async def delete_social_media(sm_id):
    async with async_session() as connect:
        query = """
        DELETE FROM social_media WHERE id = :sm_id
        """
        await connect.execute(text(query), {'sm_id': sm_id})
        await connect.commit()


async def insert_staff(tg_id, name):
    async with async_session() as connect:
        query = """
        INSERT INTO staff(telegram_id, name)
        VALUES (:tg_id, :name)
        """
        await connect.execute(text(query), {'tg_id': tg_id, 'name': name})
        await connect.commit()


async def get_all_admins():
    async with async_session() as connect:
        query = """
        SELECT * FROM staff
        """
        data = await connect.execute(text(query))
        return data.fetchall()


async def get_an_admin_by_id(admin_id):
    async with async_session() as connect:
        query = """
        SELECT name, telegram_id FROM staff
        WHERE id = :admin_id
        """
        data = await connect.execute(text(query), {'admin_id': admin_id})
        return data.fetchone()


async def remove_admin(admin_id):
    async with async_session() as connect:
        query = """
        DELETE FROM staff
        WHERE id = :admin_id
        """
        await connect.execute(text(query), {'admin_id': admin_id})
        await connect.commit()


async def get_all_consumers():
    async with async_session() as connect:
        query = """
        SELECT telegram_id FROM consumers
        """
        data = await connect.execute(text(query))
        users = data.fetchall()
        users = [user[0] for user in users]
        return users


async def insert_consumer_data(telegram_id, telegram_name):
    async with async_session() as connect:
        query = """
        INSERT INTO consumers(telegram_id, telegram_name)
        VALUES (:telegram_id, :telegram_name) ON CONFLICT DO NOTHING
        """
        await connect.execute(text(query), {'telegram_id': telegram_id, 'telegram_name': telegram_name})
        await connect.commit()


async def insert_consumer_data_to_double_table(telegram_id, telegram_name):
    async with async_session() as connect:
        query = """
        INSERT INTO done_consumers(telegram_id, telegram_name)
        VALUES (:telegram_id, :telegram_name) ON CONFLICT DO NOTHING
        """
        await connect.execute(text(query), {'telegram_id': telegram_id, 'telegram_name': telegram_name})
        await connect.commit()


async def insert_other_consumer_data(telegram_id, contact, full_name):
    async with async_session() as connect:
        query = """
        UPDATE consumers
        SET contact = :contact, full_name = :full_name
        WHERE telegram_id = :telegram_id
        """
        await connect.execute(text(query), {'contact': contact, 'full_name': full_name, 'telegram_id': telegram_id})
        await connect.commit()


async def insert_other_consumer_data_to_double_table(telegram_id, contact, full_name):
    async with async_session() as connect:
        query = """
        UPDATE done_consumers
        SET contact = :contact, full_name = :full_name
        WHERE telegram_id = :telegram_id
        """
        await connect.execute(text(query), {'contact': contact, 'full_name': full_name, 'telegram_id': telegram_id})
        await connect.commit()


async def get_consumer_data(consumer_id):
    async with async_session() as connect:
        consumer = await connect.execute(text("""
        SELECT telegram_name, full_name, contact
        FROM consumers
        WHERE telegram_id = :telegram_id
        """), {'telegram_id': consumer_id})
        return consumer.fetchone()


async def get_all_done_consumers():
    async with async_session() as connect:
        query = """
        SELECT * FROM done_consumers
        """
        data = await connect.execute(text(query))
        users = data.fetchall()
        return users


async def delete_a_client(client_id):
    async with async_session() as connect:
        query = """
        DELETE FROM done_consumers
        WHERE id = :client_id
        """
        await connect.execute(text(query), {'client_id': client_id})
        await connect.commit()


async def get_a_done_consumer(client_id):
    async with async_session() as connect:
        query = """
        SELECT * FROM done_consumers
        WHERE id = :id
        """
        data = await connect.execute(text(query), {'id': client_id})
        users = data.fetchone()
        return users