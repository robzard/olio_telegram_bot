from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from static.servicebook import servicebook_data


def servicebook_keyboard() -> InlineKeyboardBuilder:
    i = 0
    builder = InlineKeyboardBuilder()
    for el in servicebook_data:
        i += 1
        # builder.button(text=f'{i}', url=el[1])
        builder.button(text=el[0], url=el[1])
    builder.adjust(2)  # Adjust buttons in rows, 2 buttons per row or as needed
    return builder


def kb_search_menu_bar() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Меню", switch_inline_query_current_chat="menu ")
    builder.button(text="Бар Original", switch_inline_query_current_chat="original ")
    builder.button(text="Бар Classic", switch_inline_query_current_chat="classic ")
    builder.button(text="Весь список", switch_inline_query_current_chat="all ")
    builder.adjust(1,2,1)
    return builder.as_markup()
