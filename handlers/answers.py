from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_media_photo import InputMediaPhoto

from services import Service
from services.interfaces import NoFormsError

from utils.message_template import MessageTemplate
from utils.send_form import send_form

router = Router()


class States(StatesGroup):
    answers = State()


@router.message(Command("my_likes"))
async def look_likes(message: Message, state: State, service: Service, bot: Bot):
    no_forms = await send_next_form(message.from_user.id, message, state, service)

    if no_forms:
        text, reply_markup = MessageTemplate.from_json('answers/no_forms').render()
        await message.answer(text=text, reply_markup=reply_markup)


@router.callback_query(States.answers, F.data == "like")
async def like(callback: CallbackQuery, state: FSMContext, service: Service):
    data = await state.get_data()
    match = data['match']
    form = data['form']

    await service.answers.create(callback.from_user.id, match.id, form.id, True)

    text, reply_markup = MessageTemplate.from_json('answers/match').render(form=form)
    await callback.message.edit_media(InputMediaPhoto(media=form.photo_1, caption=text), reply_markup=reply_markup)


@router.callback_query(F.data == "continue")
async def cont(callback: CallbackQuery, state: FSMContext, service: Service):
    await callback.message.edit_reply_markup()

    no_forms = await send_next_form(callback.from_user.id, callback.message, state, service, True)

    if no_forms:
        text, reply_markup = MessageTemplate.from_json('answers/no_forms').render()
        await callback.message.answer(text=text, reply_markup=reply_markup)


@router.callback_query(States.answers, F.data == "dislike")
async def dislike(callback: CallbackQuery, state: FSMContext, service: Service):
    data = await state.get_data()
    match = data['match']
    form = data['form']

    await service.answers.create(callback.from_user.id, match.id, form.id, False)
    
    no_forms = await send_next_form(callback.from_user.id, callback.message, state, service)

    if no_forms:
        text, reply_markup = MessageTemplate.from_json('answers/no_forms').render()
        await callback.message.answer(text=text, reply_markup=reply_markup)
        await callback.message.delete()


async def send_next_form(user_id: int, message: Message, state: FSMContext, service: Service, not_delete_message: bool = False) -> bool:
    try:
        match, form = await service.answers.get(user_id)

    except NoFormsError:
        return True

    else:
        await state.update_data(match=match, form=form)
        text, reply_markup = MessageTemplate.from_json('answers/form').render(form=form)

        if not_delete_message or message.photo is None:
            await message.answer_photo(form.photo_1, caption=text, reply_markup=reply_markup)
        else:
            await message.edit_media(InputMediaPhoto(media=form.photo_1, caption=text), reply_markup=reply_markup)

        await state.set_state(States.answers)
        return False