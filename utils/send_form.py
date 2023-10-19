from aiogram import Bot
from aiogram.types import InputMediaPhoto

from repositories.postgres.models import Form
from utils.message_template import MessageTemplate


async def send_form(bot: Bot, user_id: int, form: Form, template: str):
    text, reply_markup = MessageTemplate.from_json(template).render(form=form)
    await bot.send_photo(user_id, form.photo_1, caption=text, reply_markup=reply_markup)




def get_media_group(form: Form):
    photos = []
    for i in range(1, 4):
        photo = getattr(form, f'photo_{i}')
        if photo is not None:
            photos.append(InputMediaPhoto(media=photo))
    return photos