from utils.texts import *
from data.config import *
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from loader import dp

about_page_text = f"{about_text}\n\n{about_text_body}"

#` Хендлер для 📕 О магазине                                                             
@dp.message_handler(Text(equals=["⚙️  Помощь"]))
async def show_menu(message: Message):
    await message.answer(about_page_text)
