from aiogram import types, Router
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, CallbackQuery

router_callback_query = Router()

menu_data = [
    {"id": 1, "name": "Пицца Маргарита", "description": "Классическая пицца с томатами и моцареллой"},
    {"id": 2, "name": "Цезарь", "description": "Салат Цезарь с курицей, сыром и соусом"},
    # Добавьте другие пункты меню по желанию
]

bar_data = [
    {"id": 1, "name": "Эспрессо", "description": "Крепкий черный кофе"},
    {"id": 2, "name": "Мохито", "description": "Освежающий коктейль с мятой и лаймом"},
    # Добавьте другие напитки по желанию
]


@router_callback_query.callback_query(lambda c: c.data == 'menu')
async def handle_menu_bar_query(query: types.CallbackQuery):
    text = ""
    if query.data == "menu":
        text += "Список меню:\n"
        for item in menu_data:
            text += f"{item['name']}: {item['description']}\n"
    elif query.data == "bar":
        text += "Список напитков бара:\n"
        for item in bar_data:
            text += f"{item['name']}: {item['description']}\n"

    await query.answer(text=text, show_alert=True)
