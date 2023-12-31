from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_media_photo import InputMediaPhoto

from services import Service
from services.interfaces import NoFormsError
from utils import get_user_url

from utils.message_template import MessageTemplate
from utils.send_form import send_form

router = Router()


class States(StatesGroup):
    answers = State()


@router.message(Command("my_likes"))
async def look_likes(message: Message, state: FSMContext, service: Service, bot: Bot):
    await state.clear()

    if await send_next_form(message.from_user.id, message, state, service):
        text, reply_markup = MessageTemplate.from_json('answers/no_forms').render()
        await message.answer(text=text, reply_markup=reply_markup)
        await state.clear()


@router.callback_query(States.answers, F.data == "like")
async def like(callback: CallbackQuery, state: FSMContext, service: Service):
    data = await state.get_data()
    match = data['match']
    form = data['form']

    await service.answers.create(callback.from_user.id, match.id, form.id, True)

    url = get_user_url(form.user_id)
    text, reply_markup = MessageTemplate.from_json('answers/full_form_with_button').render(form=form, url=url)
    await callback.message.edit_media(InputMediaPhoto(media=form.photo_1, caption=text), reply_markup=reply_markup)


@router.callback_query(F.data == "continue")
async def cont(callback: CallbackQuery, state: FSMContext, service: Service):
    await callback.message.edit_reply_markup()

    if await send_next_form(callback.from_user.id, callback.message, state, service, True):
        text, reply_markup = MessageTemplate.from_json('answers/last_form').render()
        await callback.message.answer(text=text, reply_markup=reply_markup)
        await state.clear()


@router.callback_query(States.answers, F.data == "dislike")
async def dislike(callback: CallbackQuery, state: FSMContext, service: Service):
    data = await state.get_data()
    match = data['match']
    form = data['form']

    await service.answers.create(callback.from_user.id, match.id, form.id, False)
    
    if await send_next_form(callback.from_user.id, callback.message, state, service):
        text, reply_markup = MessageTemplate.from_json('answers/last_form').render()
        await callback.message.answer(text=text, reply_markup=reply_markup)
        await callback.message.delete()
        await state.clear()


async def send_next_form(user_id: int, message: Message, state: FSMContext, service: Service, not_delete_message: bool = False) -> bool:
    try:
        match, form = await service.answers.get(user_id)

    except NoFormsError:
        return True

    else:
        await state.update_data(match=match, form=form)
        text, reply_markup = MessageTemplate.from_json('answers/form_with_buttons').render(form=form)

        if not_delete_message or message.photo is None:
            await message.answer_photo(form.photo_1, caption=text, reply_markup=reply_markup)
        else:
            await message.edit_media(InputMediaPhoto(media=form.photo_1, caption=text), reply_markup=reply_markup)

        await state.set_state(States.answers)
        return False