from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.commands import my_form
from services import Service


from utils.message_template import MessageTemplate

router = Router()


class States(StatesGroup):
    gender = State()
    gender_search = State()
    name = State()
    faculty = State()
    course = State()
    about = State()
    request = State()
    photo = State()


@router.callback_query(F.data.in_({"fill_form", "edit_form"}))
async def requset_gender(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    text, reply_markup = MessageTemplate.from_json('form/gender').render()
    await callback.message.answer(text=text, reply_markup=reply_markup)
    await state.set_state(States.gender)

@router.message(States.gender)
async def take_gender(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/gender').render()
    buttons = [x.text for sub_arr in reply_markup.keyboard for x in sub_arr]
    
    if message.text == buttons[0]:
        await state.update_data(gender=True)
        await requset_gender_search(message, state)

    elif message.text == buttons[1]:
        await state.update_data(gender=False)
        await requset_gender_search(message, state)
    
    else:
        text, reply_markup = MessageTemplate.from_json('form/gender_unsuccess').render()
        await message.answer(text=text, reply_markup=reply_markup)


async def requset_gender_search(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/gender_search').render()
    await message.answer(text=text, reply_markup=reply_markup)
    await state.set_state(States.gender_search)

@router.message(States.gender_search)
async def take_gender_search(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/gender_search').render()
    buttons = [x.text for sub_arr in reply_markup.keyboard for x in sub_arr]

    if message.text == buttons[0]:
        await state.update_data(gender_search=True)
        await requset_name(message, state)

    elif message.text == buttons[1]:
        await state.update_data(gender_search=False)
        await requset_name(message, state)
    
    elif message.text == buttons[2]:
        await state.update_data(gender_search=None)
        await requset_name(message, state)
    
    else:
        text, reply_markup = MessageTemplate.from_json('form/gender_search_unsuccess').render()
        await message.answer(text=text, reply_markup=reply_markup)


async def requset_name(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/name').render()
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.name)

@router.message(States.name)
async def take_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await requset_faculty(message, state)


async def requset_faculty(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/faculty').render()
    await message.answer(text=text, reply_markup=reply_markup)
    await state.set_state(States.faculty)

@router.message(States.faculty)
async def take_faculty(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/faculty').render()
    buttons = [x.text for sub_arr in reply_markup.keyboard for x in sub_arr]

    if message.text in buttons:
        await state.update_data(faculty=message.text)
        await requset_course(message, state)
    else:
        text, reply_markup = MessageTemplate.from_json('form/faculty_unsuccess').render()
        await message.answer(text=text, reply_markup=reply_markup)


async def requset_course(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('form/course').render()
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.course)

@router.message(States.course)
async def take_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
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
    text, reply_markup = MessageTemplate.from_json('form/request').render()
    buttons = [x.text for sub_arr in reply_markup.keyboard for x in sub_arr]
    
    if message.text in buttons:
        await state.update_data(request=message.text, username=message.from_user.username)
        state_data = await state.get_data()
        await service.forms.create(message.from_user.id, state_data)
        await state.clear()

        text, reply_markup = MessageTemplate.from_json('form/success').render()
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
        await my_form(message, state, service, bot)
    else:
        text, reply_markup = MessageTemplate.from_json('form/request_unsuccess').render()
        await message.answer(text=text, reply_markup=reply_markup)
