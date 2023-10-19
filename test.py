import asyncio
import logging
import time

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, FSInputFile, InlineKeyboardButton, InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.input_media_photo import InputMediaPhoto

from config import Config

logging.basicConfig(level=logging.INFO)


async def main():
    config = Config()
    bot = Bot(config.bot.token, parse_mode='HTML')

    reply_markup = InlineKeyboardBuilder([[InlineKeyboardButton(text="Test", callback_data="test")]]).as_markup()
    message = await bot.send_photo(
        587247376, 
        photo=FSInputFile("files/1.jpg"),
        caption="Test", 
        reply_markup=reply_markup
    )
    
    time.sleep(5)

    file = InputMediaPhoto(media=FSInputFile("files/2.png"), caption="Updated caption :)")
    await message.edit_media(file, reply_markup=reply_markup)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
