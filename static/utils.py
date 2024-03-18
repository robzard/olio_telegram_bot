import os
import zipfile

from database.db import Drink


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


# def format_message_text(item: Drink):
#     f"{item.name}\n{item.composition}\n{item.preparation}\n{item.history}\n[Фото]({item.photo_url})"
#     text = 'item.name'

def escape_md_v2(text: str) -> str:
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, '\\' + char)
    return text


def format_message_text(item) -> str:
    name = escape_md_v2(item.name.strip()) if item.name else "Информация отсутствует"
    composition = escape_md_v2(item.composition.strip()) if item.composition else "Информация отсутствует"
    preparation = escape_md_v2(item.preparation.strip()) if item.preparation else "Информация отсутствует"
    history = escape_md_v2(item.history.strip()) if item.history else "Информация отсутствует"
    photo_url = item.photo_url if item.photo_url else ""

    message = (
        f"📌 *Название:* {name}\n\n"
        f"📝 *Состав:* \n{composition}\n\n"
        f"🍳 *Приготовление:* \n{preparation}\n\n"
        f"📖 *История:* \n{history}\n\n"
    )

    if photo_url:
        message += f"[Фото]({photo_url})"

    return message
