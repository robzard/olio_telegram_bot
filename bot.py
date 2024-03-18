import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand, Update, Message
import os
from dotenv import load_dotenv

from database.db import create_tables, add_excel_to_db, get_all_users, User
from handlers.callbacks import router_callback_query
from handlers.commands import start, servicebook, router_commands
from handlers.inline_mode import router_inline_query
from handlers.messages import router_messages
from middlewares.middlewares import DBMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv('TOKEN')

# Инициализация бота и сессии
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

# Регистрация команд и мидлвари
dp.message.middleware(DBMiddleware())


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Список команд"),
        BotCommand(command="servicebook", description="Service Book"),
        BotCommand(command="search_menu_bar", description="Поиск меню"),
        BotCommand(command="forward_message", description="Переслать сообщение всем")
    ]
    await bot.set_my_commands(commands)


async def on_startup():
    users: [User] = await get_all_users(admins=True)
    for user in users:
        await bot.send_message(chat_id=user.id, text='Я запустился')


async def on_shutdown():
    users: [User] = await get_all_users(admins=True)
    for user in users:
        await bot.send_message(chat_id=user.id, text='Я остановился')


async def main():
    # Создание таблиц БД, если это необходимо
    await create_tables()
    await add_excel_to_db('Меню Олио.xlsx', 'Меню', start_row=3, inline_category='menu')
    await add_excel_to_db('коктейли.xlsx', 'Original', inline_category='original')
    await add_excel_to_db('коктейли.xlsx', 'Classic', inline_category='classic')

    # Настройка команд бота
    await set_commands(bot)

    # Запуск polling
    dp.include_router(router_commands)
    dp.include_router(router_callback_query)
    dp.include_router(router_inline_query)
    dp.include_router(router_messages)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
