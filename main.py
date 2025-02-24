import os
import asyncio

from dotenv import load_dotenv

import openai
from openai import OpenAI

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


load_dotenv()

BOT_TOKEN = str(os.getenv('bot_token'))
API_KEY = str(os.getenv('openai_key'))
TELEGRAM_TOKEN = str(os.getenv('bot_token'))
MAX_TOKENS = 500

users = str(os.getenv('users'))
USERS = [int(element.strip()) for element in users.split(',') if len(element) >= 9]


client = OpenAI(
    api_key=API_KEY,
)


def get_ai_response(request_text, max_tokens=MAX_TOKENS, temperature=0):
    messages = [
        {
            'role': 'user',
            'content': request_text,
        }
    ]

    chat_completion = client.chat.completions.create(
        max_tokens=max_tokens,
        model="gpt-3.5-turbo",  # модель для выбора
        messages=messages,  # сообщение
        temperature=temperature,  # степень креативности ответа
    )

    return chat_completion.choices[0].message.content



dp = Dispatcher()

bot = Bot(token=TELEGRAM_TOKEN,
          default=DefaultBotProperties(
              parse_mode=ParseMode.HTML
          ),
          disable_web_page_preview=True
          )

@dp.message(Command("start"))
async def start(message):
    telegram_id = message.from_user.id
    # print('telegram_id', telegram_id)
    if telegram_id in USERS:
        text = 'Привет!'
    else:
        text = 'Привет! Я не разговариваю с незнакомыми!'

    await bot.send_message(
        chat_id=telegram_id,
        text=text,
    )


@dp.message()
async def any_message(message):
    telegram_id = message.from_user.id
    # print('telegram_id', telegram_id)
    request = message.text

    try:
        res = get_ai_response(request + 'Ответ раздели на абзацы по содержанию', )
    except Exception:
        res = 'Упппсс.... \nЧто-то пошло не так, обратитесь к администратору!'

    await bot.send_message(
        chat_id=telegram_id,
        text=res
    )


async def start_bot():
    await bot.delete_webhook(drop_pending_updates=False)
    try:
        await dp.start_polling(bot, polling_timeout=1)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start_bot())