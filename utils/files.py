import logging
import os
from datetime import datetime

from aiogram import Bot
from aiogram.types import Message, FSInputFile, PhotoSize, Document, File
from sqlalchemy.orm import Session


async def save_document(bot: Bot, user_id: int, document: PhotoSize|Document) -> str:
    file: File = await bot.get_file(document.file_id)
    file_name = file.file_id

    path = f"files/{file_name}"
    await bot.download_file(file.file_path, path)

    return file_name


async def get_document(user_id: int, file: str, user_files_path: str) -> FSInputFile:
    """
    :return: пользовательский файл с резюме в виде FSInputFile
    """
    path = f"files/{file}"
    return FSInputFile(path)

