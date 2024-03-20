from aiogram import types, Router
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto, InlineQueryResultCachedPhoto
import re

from database.db import get_positions_from_db, search_menu_objects
from keyboards.inline import kb_search_menu_bar
from static.utils import format_message_text

router_inline_query = Router()


#
# @router_inline_query.inline_query()
# async def handle_inline_query(inline_query: types.InlineQuery):
#     # Пример поиска данных и формирования ответа
#     query_text = inline_query.query
#
#     mock_data = [
#         {"id": 1, "title": "Пример 1", "description": "Описание примера 1"},
#         {"id": 2, "title": "Пример 2", "description": "Описание примера 2"},
#         # Добавьте больше записей для тестирования
#     ]
#
#     # Здесь должен быть ваш код для поиска в базе данных...
#     search_results = await search_by_title(query_text, mock_data)
#
#     items = [
#         InlineQueryResultArticle(
#             id=str(result["id"]),
#             title=result["title"],
#             input_message_content=InputTextMessageContent(message_text=result["description"])
#         )
#         for result in search_results
#     ]
#
#     await inline_query.answer(results=items, cache_time=1)
#
#
# async def search_by_title(query_text, mock_data):
#     # Пример данных. В реальном приложении данные будут запрашиваться из базы данных
#     # Простой поиск по подстроке. В реальном приложении используйте запросы к базе данных с учётом регистра
#     return [item for item in mock_data if query_text.lower() in item["title"].lower()]


# # При выборе из списка добавляет в сообщение инлайн кнопки
# @router_inline_query.inline_query()
# async def handle_inline_query(inline_query: types.InlineQuery):
#     # Создание инлайн клавиатуры и добавление кнопок
#     inline_kb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Меню", callback_data="menu")],
#         [InlineKeyboardButton(text="Бар", callback_data="bar")]
#     ])
#     await inline_query.answer(
#         results=[
#             InlineQueryResultArticle(
#                 id="1",
#                 title="Выберите категорию",
#                 input_message_content=InputTextMessageContent(message_text="Что вас интересует?"),
#                 reply_markup=inline_kb
#             )
#         ],
#         cache_time=1
#     )


# # РАБОТАЕТ
# @router_inline_query.inline_query()
# async def inline_query_handler(inline_query: types.InlineQuery):
#     query = inline_query.query.lower()
#     results = []
#     url = "https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MXwxOTk3MzJ8MHwxfHNlYXJjaHwxfHx3b21hbiUyMHdvcmtpbmclMjBvbiUyMGElMjBsYXB0b3B8ZW58MHx8fA&ixlib=rb-1.2.1&q=80&w=1080"
#
#     # Фиктивные данные для "Меню"
#     menu_items = [
#         {"id": "menu1", "photo_url": url, "thumb_url": url, "title": "Пицца", "description": "Описание пиццы"},
#         {"id": "menu2", "photo_url": url, "thumb_url": url, "title": "Паста", "description": "Описание пасты"},
#     ]
#
#     # Фиктивные данные для "Бар"
#     bar_items = [
#         {"id": "bar1", "photo_url": url, "thumb_url": url, "title": "Кофе", "description": "Описание кофе хороший кофе, в котором много полезного, он очень вкусный, ещё есть хорошие зёрна, поэтому он такой бодрящий и кайфовый"},
#         {"id": "bar2", "photo_url": url, "thumb_url": url, "title": "Чай", "description": "Описание чая"},
#     ]
#
#     # Выбор данных в зависимости от запроса
#     if "menu" in query:
#         items = menu_items
#     elif "bar" in query:
#         items = bar_items
#     else:
#         items = []  # Пустой список, если запрос не соответствует "menu" или "bar"
#
#     # Фильтрация элементов по тексту в описании (если указан конкретный текст после "menu" или "bar")
#     query_words = query.replace("menu", "").replace("bar", "").strip().split()
#     if query_words:
#         filtered_query = query.replace("menu", "").replace("bar", "").strip()
#         items = [item for item in items if all(word.lower() in item["description"].lower() for word in query_words)]
#
#     for item in items:
#         results.append(
#             InlineQueryResultArticle(
#                 id=item["id"],
#                 title=item["title"],
#                 input_message_content=InputTextMessageContent(
#                     message_text=f"{item['title']}\n{item['description']}\n[Фото]({item['photo_url']})",
#                     parse_mode="MarkdownV2"
#                 ),
#                 description=item["description"],
#                 thumbnail_url=item["photo_url"]
#             )
#         )
#
#     await inline_query.answer(results=results, cache_time=1)


def escape_markdown_v2(text):
    # Список символов для экранирования в MarkdownV2
    escape_chars = r'_*\[]()~`>#+-=|{}.!'
    # Замена каждого символа его экранированным вариантом
    return re.sub(r'([{}])'.format(re.escape(escape_chars)), r'\\\1', text)


@router_inline_query.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery):
    query = inline_query.query.lower()
    inline_category = query.split(' ')[0]
    offset = int(inline_query.offset) if inline_query.offset.isdigit() else 0
    results = []

    items = await get_positions_from_db(query.strip())

    # Фильтрация элементов по тексту в описании
    query_words = query.replace("menu", "").replace("all", "").replace("bar", "").strip().replace("vine", "").strip().split()
    if query_words:
        items = await search_menu_objects(query_words, inline_category=inline_category)

    items_to_show = items[offset:offset+50]  # Показываем следующие 50 элементов на основе offset

    for item in items_to_show:
        results.append(
            InlineQueryResultArticle(
                id=str(item.id),
                title=item.name,
                input_message_content=InputTextMessageContent(
                    message_text=format_message_text(item),
                    parse_mode="MarkdownV2"
                ),
                description=item.category + "\n" + item.composition[:90] + "..." if item.composition and len(item.composition) > 90 else item.category + "\n" + item.composition if item.composition else item.category,
                thumbnail_url=item.photo_url,
                reply_markup=kb_search_menu_bar()
            )
        )

    next_offset = str(offset + 50) if len(items) > offset + 50 else ""  # Если есть еще элементы, увеличиваем offset, иначе возвращаем пустую строку

    await inline_query.answer(results=results, cache_time=1, next_offset=next_offset)

