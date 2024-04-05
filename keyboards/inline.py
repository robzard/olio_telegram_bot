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
    builder.button(text="Бар", switch_inline_query_current_chat="bar ")
    builder.button(text="Крепач", switch_inline_query_current_chat="krepach ")
    builder.button(text="Вино", callback_data='vine')
    builder.button(text="Весь список", switch_inline_query_current_chat="all ")
    builder.adjust(1, 2, 1)
    return builder.as_markup()


def kb_search_menu_vine() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Красное", switch_inline_query_current_chat="vine Красное вино")
    builder.button(text="Белое", switch_inline_query_current_chat="vine Белое вино")
    builder.button(text="Игристое", switch_inline_query_current_chat="vine Игристое вино")
    builder.button(text="Розовое", switch_inline_query_current_chat="vine Розовое вино")
    builder.button(text="Оранжевое", switch_inline_query_current_chat="vine Оранжевое вино")
    builder.button(text="Сладкое", switch_inline_query_current_chat="vine Сладкое вино")
    builder.button(text="Крепленое", switch_inline_query_current_chat="vine Крепленое вино")
    builder.button(text="Назад", callback_data='vine_back')
    builder.adjust(2)
    return builder.as_markup()
