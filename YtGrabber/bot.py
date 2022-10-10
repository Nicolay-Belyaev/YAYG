import logging
from aiogram import Bot, Dispatcher, executor, types
from Logic import *

API_TOKEN = '5769763160:AAHxSYMlH2KI4G6Qn1pTgG2-eLn-DwIqzt8'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('Привет! Это бог-граббер аудио и видео с YouTube. Кидай ссылку - получишь файлы.')


@dp.message_handler(commands=['url'])
async def get_quality(message: types.Message):
    audio_quality = get_audio_quality('https://www.youtube.com/watch?v=_raAGyI8-kA&list=PLwVBSkoL97Q3phZRyInbM4lShvS1cBl-U&index=5')
    video_quality = get_video_resolutions('https://www.youtube.com/watch?v=_raAGyI8-kA&list=PLwVBSkoL97Q3phZRyInbM4lShvS1cBl-U&index=5')
    await message.reply(audio_quality)
    await message.reply(video_quality)

executor.start_polling(dp, skip_updates=True)