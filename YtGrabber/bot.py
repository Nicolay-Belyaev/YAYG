import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Logic import *

API_TOKEN = '5769763160:AAHxSYMlH2KI4G6Qn1pTgG2-eLn-DwIqzt8'
logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# TODO: сделать отправку медиа в чат (будет проблема с большими файлами)
# TODO: вынести бота на хостинг (проще будет работать с большими файлами)
# TODO: время от времени загрузчик валиться с http.client.IncompleteRead: IncompleteRead
# TODO: сузить эксепты
# TODO: написать комментарии ко всему
# TODO: подумать над архитектурой + вынести дублирующийся код за функции


@dp.callback_query_handler(text='audio_only')
async def audio_handler(callback, state: FSMContext):
    try:
        async with state.proxy() as data:
            url = data['url']
            chat_id = data['chat']
        audio_quality = get_audio_quality(f'r"{url}')
        audio_buttons = [[InlineKeyboardButton(text=button, callback_data=button)] for button in audio_quality]
        keyboard_inline_buttons_audio = InlineKeyboardMarkup(inline_keyboard=audio_buttons)
        await bot.send_message(chat_id=chat_id,
                               text='Твоя выбирать, какое качество звука качать!',
                               reply_markup=keyboard_inline_buttons_audio)
    except Exception:
        await bot.send_message(chat_id=chat_id,
                               text='Моя не смочь! Твоя пробовать опять! Твоя пробовать давать другой ссылка!')


@dp.callback_query_handler(text='video_only')
async def video_handler(callback, state: FSMContext):
    try:
        async with state.proxy() as data:
            url = data['url']
            chat_id = data['chat']
        video_quality = get_video_resolutions(f'r"{url}')
        video_buttons = [[InlineKeyboardButton(text=button, callback_data=button)] for button in video_quality]
        keyboard_inline_buttons_audio = InlineKeyboardMarkup(inline_keyboard=video_buttons)
        await bot.send_message(chat_id=chat_id,
                               text='Твоя выбирать, какое качество видео качать!',
                               reply_markup=keyboard_inline_buttons_audio)
    except Exception:
        await bot.send_message(chat_id=chat_id,
                               text='Моя не смочь! Твоя пробовать опять! Твоя пробовать давать другой ссылка!')


@dp.callback_query_handler(text='audio_and_video')
async def audio_and_video_handler(callback,  state: FSMContext):
    try:
        async with state.proxy() as data:
            url = data['url']
            chat_id = data['chat']
        video_quality = get_video_resolutions(f'r"{url}')
        video_quality = list(map(lambda x: x + ' + audio', video_quality))
        video_buttons = [[InlineKeyboardButton(text=button, callback_data=button)] for button in video_quality]
        keyboard_inline_buttons_audio = InlineKeyboardMarkup(inline_keyboard=video_buttons)
        await bot.send_message(chat_id=chat_id,
                               text='Твоя выбирать, какое качество видео со звуком качать!',
                               reply_markup=keyboard_inline_buttons_audio)
    except Exception:
        await bot.send_message(chat_id=chat_id,
                               text='Моя не смочь! Твоя пробовать опять! Твоя пробовать давать другой ссылка!')


@dp.callback_query_handler()
async def downloader(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        url = data['url']
        chat_id = data['chat']
    if '+' in callback.data:
        merge_audio_video(url, callback.data[:len(callback.data) - 8], '160kbps')
    elif 'k' in callback.data:
        download_audio_only(url, callback.data)
    elif 'p' in callback.data:
        download_video_only(url, callback.data)


@dp.message_handler(commands=['help', 'start'])
async def welcome(message: types.Message):
    await message.reply('Моя уметь граббить видео и аудио с YouTube. Твоя давать ссылка, моя давать качать!')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def mode_selector(message, state: FSMContext):
    selectors = [[InlineKeyboardButton(text='Аудио', callback_data='audio_only')],
                 [InlineKeyboardButton(text='Видео', callback_data='video_only')],
                 [InlineKeyboardButton(text='Качать всё вместе!', callback_data='audio_and_video')]]
    keyboard_inline_buttons_mode = InlineKeyboardMarkup(inline_keyboard=selectors)
    await bot.send_message(message.chat.id,
                           text='Твоя хотеть качать аудио, видео или все вместе?',
                           reply_markup=keyboard_inline_buttons_mode)
    async with state.proxy() as data:
        data['url'] = message.html_text
        data['chat'] = message.chat.id

executor.start_polling(dp, skip_updates=True)
