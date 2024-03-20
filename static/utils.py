import os
import zipfile
from aiogram import types
from aiogram.types import InputMediaPhoto, InputMediaVideo

from database.db import MenuObject


def save_images():
    xlsx_file_path = './Меню Олио.xlsx'
    extract_folder = 'extracted_images'

    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    # Открываем xlsx файл как zip-файл
    with zipfile.ZipFile(xlsx_file_path, 'r') as zip_ref:
        # Перебираем содержимое zip-файла
        for file_info in zip_ref.infolist():
            # Проверяем, находится ли файл в папке с изображениями
            if file_info.filename.startswith('xl/media/'):
                # Извлекаем файл
                zip_ref.extract(file_info, extract_folder)


def escape_md_v2(text: str) -> str:
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, '\\' + char)
    return text


def format_message_text(item) -> str:
    message = ""
    if item.name:
        message += f"📌 *Название:* \n{escape_md_v2(item.name.strip())}\n\n"
    if item.price:
        message += f"💰 *Цена:* \n{escape_md_v2(item.price.strip())}\n\n"
    if item.city:
        message += f"🏠 *Место производства:* \n{escape_md_v2(item.city.strip())}\n\n"
    if item.composition:
        message += f"📝 *Состав:* \n{escape_md_v2(item.composition.strip())}\n\n"
    if item.preparation:
        message += f"🍳 *Приготовление:* \n{escape_md_v2(item.preparation.strip())}\n\n"
    if item.history:
        message += f"📖 *История:* \n{escape_md_v2(item.history.strip())}\n\n"

    if item.photo_url:
        message += f"[Фото]({item.photo_url})"

    return message

