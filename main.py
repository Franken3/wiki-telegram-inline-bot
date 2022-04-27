from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import hashlib

import logging
from aiogram import Bot, Dispatcher, executor

from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
from config import TOKEN, TEXT

from wiki_good_parser import find_me

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['/start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, TEXT.hello_text)


@dp.message_handler()
async def process_command(message: types.Message):
    await bot.send_message(message.from_user.id, find_me(message.text)[0])


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    text = inline_query.query
    found = find_me(text)
    if found[0]:
        input_content = InputTextMessageContent(found[0] + '\n\n' + found[1])
        title = TEXT.title_found_text + text
        # url = found[1]
    else:
        input_content = InputTextMessageContent(f'Статья с названием "{text}" на Википедии не найдена.')
        title = TEXT.title_not_found_text

    result_id: str = hashlib.md5(text.encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        title=title,
        input_message_content=input_content,
        thumb_url='https://w7.pngwing.com/pngs/223/1020/png-transparent-wikipedia-logo-wikimedia-foundation-globe-globe-miscellaneous-angle-globe.png'
    )
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp)
