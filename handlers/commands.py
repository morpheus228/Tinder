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
async def start(message: Message, state: FSMContext, service):
    # проверяем есть ли у челика форма
    if True:
    
    # если есть - сообщение с кнопкой "Смотреть анкеты"
        text, reply_markup = MessageTemplate.from_json('commands/start_with_form').render()
        await message.answer(text=text, reply_markup=reply_markup)

    # если нет - сообщение с кнопкой заполнить анкету
    else:
        text, reply_markup = MessageTemplate.from_json('commands/start').render()
        await message.answer(text=text, reply_markup=reply_markup)


@router.message(Command("me")) 
async def my_form(message: Message, state: State, service: Service, bot: Bot):
    form = await service.forms.get_by_user_id(message.from_user.id)

    if form is not None:
        text, reply_markup = MessageTemplate.from_json('commands/form').render(form=form)
        await bot.send_photo(message.from_user.id, form.photo_1, 
                             caption=text, reply_markup=reply_markup)
    
    else:
        text, reply_markup = MessageTemplate.from_json('commands/form_absence').render()
        await message.answer(text=text, reply_markup=reply_markup)
        