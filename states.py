from aiogram.fsm.state import State, StatesGroup


class AlterAboutUs(StatesGroup):
    confirmation = State()
    message = State()


class AlterContact(StatesGroup):
    confirmation = State()
    message = State()


class AlterWelcomeMessage(StatesGroup):
    message = State()


class AlterNewComersMessage(StatesGroup):
    message = State()


class FAQaddition(StatesGroup):
    question = State()
    answer = State()
    category = State()


class CategoryAddition(StatesGroup):
    category = State()


class AlterCategory(StatesGroup):
    id = State()
    category = State()


class AlterFAQcategory(StatesGroup):
    id = State()
    category = State()


class AlterQuestion(StatesGroup):
    id = State()
    question = State()


class AlterAnswer(StatesGroup):
    id = State()
    answer = State()


class SocialMediaAddition(StatesGroup):
    name = State()
    link = State()


class OtherQuestions(StatesGroup):
    message = State()


class QuestionAnswer(StatesGroup):
    to = State()
    message = State()


class StaffAdd(StatesGroup):
    telegram_id = State()
    name = State()


class UserRegistration(StatesGroup):
    full_name = State()
    contact = State()


class AlterConsumerData(StatesGroup):
    full_name = State()
    contact = State()


class NewsLetter(StatesGroup):
    message = State()
