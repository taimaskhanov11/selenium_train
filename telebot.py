import asyncio
import logging

import requests
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, executor, types

from main2 import correct_time

from main2 import avito_auth

TOKEN = '1829887939:AAHDWw57KSvQi8zZthDOzGzIWuqSKX6WIcs'
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

RUN = True

LAST_TIME = correct_time('00:00')

site = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&s=104&user=1'
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())


# todo доделать proxy

@dp.message_handler(commands="start")
async def start(message: types.Message):
    global RUN
    global LAST_TIME
    RUN = True
    poop = asyncio.get_event_loop()
    poop.create_task(news_every_minute())
    LAST_TIME = correct_time('00:00')
    await message.answer('Бот запущен')


@dp.message_handler(commands="stop")
async def start(message: types.Message):
    global RUN
    RUN = False
    await message.answer('Бот приостановлен')


async def news_every_minute():
    global LAST_TIME
    while RUN:
        try:
            answer = avito_auth(site)
            print(answer)
            ad_time = correct_time(answer['time'])
            if ad_time > LAST_TIME:
                await bot.send_message(269019356, answer['text'], disable_notification=True)
                LAST_TIME = ad_time
            await asyncio.sleep(10)
        except Exception as exp:

            await bot.send_message(269019356, f'{exp}', disable_notification=True)
            await asyncio.sleep(10)


if __name__ == '__main__':
    # asyncio.run(news_every_minute())
    poop = asyncio.get_event_loop()
    poop.create_task(news_every_minute())
    executor.start_polling(dp, skip_updates=True)