from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_media_photo import InputMediaPhoto

from services import Service

from utils.message_template import MessageTemplate

router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext, service: Service):
    await state.clear()
    form = await service.forms.get_by_user_id(message.from_user.id)
    
    if form is not None:
        text, reply_markup = MessageTemplate.from_json('commands/form').render(form=form)
        await message.answer(text=text, reply_markup=reply_markup)

    else:
        text, reply_markup = MessageTemplate.from_json('commands/start').render()
        await message.answer(text=text, reply_markup=reply_markup)


@router.message(Command("me")) 
async def my_form(message: Message, state: State, service: Service, bot: Bot):
    await state.clear()
    form = await service.forms.get_by_user_id(message.from_user.id)

    if form is not None:
        text, reply_markup = MessageTemplate.from_json('commands/form').render(form=form)
        await message.answer_photo(photo=form.photo_1, caption=text, reply_markup=reply_markup)
    
    else:
        text, reply_markup = MessageTemplate.from_json('commands/form_absence').render()
        await message.answer(text=text, reply_markup=reply_markup)
        