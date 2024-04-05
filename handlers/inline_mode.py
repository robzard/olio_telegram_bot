from aiogram import types, Router
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto, InlineQueryResultCachedPhoto
import re

from database.db import get_positions_from_db, search_menu_objects
from keyboards.inline import kb_search_menu_bar
from static.utils import format_message_text

router_inline_query = Router()


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
    query_words = query.replace("menu", "").replace("all", "").replace("bar", "").strip().replace("vine", "").strip().replace("krepach", "").strip().split()
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

    await inline_query.answer(results=results, cache_time=300, next_offset=next_offset)

