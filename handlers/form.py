from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.commands import my_form
from services import Service


from utils.message_template import MessageTemplate

router = Router()


class States(StatesGroup):
    name = State()
    about = State()
    request = State()
    photo = State()



@router.callback_query(F.data == "fill_form")
async def requset_name(callback: CallbackQuery, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/name').render()
    await callback.message.edit_text(text=text, reply_markup=reply_markup)
    await state.set_state(States.name)


@router.message(States.name)
async def take_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await requset_about(message, state)


async def requset_about(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/about').render()
    await message.answer(text=text, reply_markup=reply_markup)
    await state.set_state(States.about)


@router.message(States.about)
async def take_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await requset_photo(message, state)


async def requset_photo(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/photo').render()
    await message.answer(text=text, reply_markup=reply_markup)
    await state.set_state(States.photo)


@router.message(States.photo, F.photo != None)
async def take_photo(message: Message, state: FSMContext, service: Service):
    await state.update_data(photo_1=message.photo)
    await requset_request(message, state)


async def requset_request(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/request').render()
    await message.answer(text=text, reply_markup=reply_markup)
    await state.set_state(States.request)


@router.message(States.request)
async def take_request(message: Message, state: FSMContext, service: Service, bot: Bot):
    await state.update_data(request=message.text)
    state_data = await state.get_data()
    await service.forms.create(message.from_user.id, state_data)
    await state.clear()
    await my_form(message, state, service, bot)
