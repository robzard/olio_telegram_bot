from typing import Callable, Dict, Any

from aiogram import types, BaseMiddleware
from aiogram.types import Update

from database.db import User, get_async_session


async def registration_user(message: types.Message, data: dict):
    async_session = await get_async_session()
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            user = User(id=message.from_user.id, username=message.from_user.username,
                        first_name=message.from_user.first_name, last_name=message.from_user.last_name)
            session.add(user)
            await session.commit()
        data['db_session'] = session


class DBMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Update, Dict[str, Any]], Any], event: Update,
                       data: Dict[str, Any]):

        message = event if isinstance(event, types.Message) else None
        if message and message.text and message.text.startswith('/start'):
            await registration_user(message, data)
        return await handler(event, data)
