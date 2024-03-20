import logging

from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import delete

from database.db import get_all_users, User, get_async_session, MenuObject, add_excel_to_db
from keyboards.inline import servicebook_keyboard, kb_search_menu_bar
from messages_text.txt import txt

router_commands = Router()


@router_commands.message(CommandStart())
async def start(message: types.Message):
    await message.answer(txt['start'], parse_mode="HTML")


@router_commands.message(Command('servicebook'))
async def servicebook(message: types.Message):
    builder = servicebook_keyboard()
    await message.answer(txt['servicebook'], reply_markup=builder.as_markup(), parse_mode="HTML")


@router_commands.message(Command('search_menu_bar'))
async def cmd_delete(message: types.Message):
    await message.answer(
        text="Выберите, что вас интересует:",
        reply_markup=kb_search_menu_bar(), parse_mode="HTML"
    )


@router_commands.message(Command('forward_message'))
async def gpt_question(message: types.Message):
    admins: [User] = await get_all_users(admins=True)
    if message.chat.id in [admin.id for admin in admins]:
        i = 0
        users = await get_all_users()
        for user in users:
            try:
                if user.id == message.chat.id:
                    await message.reply_to_message.send_copy(chat_id=user.id)
                    i += 1
            except Exception as e:
                print(f"Error forwarding message to {user.id}: {e}")
        await message.answer(f'Сообщение отправлено.\nКоличество пользователей, кому было отправлено сообщение: {i}')
    else:
        await message.answer(f'Сообщения может отправлять только администратор.')


@router_commands.message(Command('refresh_menu'))
async def cmd_delete(message: types.Message):
    admins: [User] = await get_all_users(admins=True)
    if message.chat.id in [admin.id for admin in admins]:
        async_session = await get_async_session()
        async with async_session() as session:
            try:
                logging.info('Удаляю данные')
                await session.execute(delete(MenuObject))
                await session.commit()
                logging.info('Данные удалены')
                await add_excel_to_db('Меню', inline_category='menu')
                await add_excel_to_db('Бар', inline_category='bar')
                await add_excel_to_db('Вино', inline_category='vine')
                await message.answer(text="Данные обновлены.")
            except Exception as ex:
                logging.info(f'ex - {str(ex)}')
                await message.answer(text=f"Произошла ошибка при обновлении, обратитесь к разработчику.:\n{str(ex)}")
    else:
        await message.answer(f'Обновлять данные может только администратор.')
