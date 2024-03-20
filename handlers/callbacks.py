from aiogram import types, Router
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, CallbackQuery

from keyboards.inline import kb_search_menu_vine, kb_search_menu_bar

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


@router_callback_query.callback_query(lambda c: c.data == 'vine')
async def handle_menu_bar_query(query: types.CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=kb_search_menu_vine())


@router_callback_query.callback_query(lambda c: c.data == 'vine_back')
async def handle_menu_bar_query(query: types.CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=kb_search_menu_bar())
