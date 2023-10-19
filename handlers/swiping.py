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
    swiping = State()


@router.message(Command("swiping")) 
async def swiping_from_command(message: Message, state: State, service: Service, bot: Bot):
    no_forms = await send_next_form(message.from_user.id, message, None, state, service)

    if no_forms:
        text, reply_markup = MessageTemplate.from_json('swiping/no_forms').render()
        await message.answer(text=text, reply_markup=reply_markup)


@router.callback_query(F.data == "swiping")
async def swiping_from_callback(callback: CallbackQuery, state: State, service: Service, bot: Bot):
    # await callback.message.edit_text(text=callback.message.text)
    no_forms = await send_next_form(callback.from_user.id, callback.message, None, state, service)

    if no_forms:
        text, reply_markup = MessageTemplate.from_json('swiping/no_forms').render()
        await callback.message.edit_text(text=text, reply_markup=reply_markup)



@router.callback_query(States.swiping, F.data == "like")
async def like(callback: CallbackQuery, state: FSMContext, service: Service):
    form_id = (await state.get_data())['form_id']
    await service.swiping.create_rate(callback.from_user.id, form_id, value=True)
    no_forms = await send_next_form(callback.from_user.id, callback.message, form_id, state, service)

    if no_forms:
        text, reply_markup = MessageTemplate.from_json('swiping/no_forms').render()
        await callback.message.answer(text=text, reply_markup=reply_markup)
        await callback.message.delete()



@router.callback_query(States.swiping, F.data == "dislike")
async def dislike(callback: CallbackQuery, state: FSMContext, service: Service):
    form_id = (await state.get_data())['form_id']
    await service.swiping.create_rate(callback.from_user.id, form_id, value=False)
    no_forms = await send_next_form(callback.from_user.id, callback.message, form_id, state, service)

    if no_forms:
        text, reply_markup = MessageTemplate.from_json('swiping/no_forms').render()
        await callback.message.answer(text=text, reply_markup=reply_markup)
        await callback.message.delete()



async def send_next_form(user_id: int, message: Message, prev_form_id: int, state: FSMContext, service: Service) -> bool:
    try:
        form = await service.swiping.get_form(user_id, prev_form_id)

    except NoFormsError:
        return True

    else:
        await state.update_data(form_id=form.id)
        text, reply_markup = MessageTemplate.from_json('swiping/form').render(form=form)

        if message.photo is None:
            await message.answer_photo(form.photo_1, caption=text, reply_markup=reply_markup)
        else:
            await message.edit_media(InputMediaPhoto(media=form.photo_1, caption=text), reply_markup=reply_markup)

        await state.set_state(States.swiping)
        return False
