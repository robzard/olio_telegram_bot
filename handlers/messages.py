from aiogram import types, Router, F, Bot

from database.db import get_all_users

router_messages = Router()


@router_messages.message(lambda message: message.text.lower() == "отправить")
async def gpt_question(message: types.Message):
    i = 0
    users = await get_all_users()
    for user in users:
        try:
            if user.id != message.chat.id:
                await message.reply_to_message.forward(chat_id=user.id)
                i+=1
        except Exception as e:
            print(f"Error forwarding message to {user.id}: {e}")
    await message.answer(f'Сообщение отправлено.\nКоличество пользователей, кому было отправлено сообщение: {i}')