import logging
from data.config import *
from utils.texts import *
from aiogram import types
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputFile
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command, Text
from utils.db_api.db_commands import register_user, find_user

from keyboards.default.menu import menu

from loader import dp, bot

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

	uid = message.from_user.id
	name = message.from_user.full_name
	username = message.from_user.username
	
	register_user(uid,name,username)  

	user = find_user(uid)

	text = f"{hello_text}\n\n{hello_text_body}\n\n{user.wallet_info()}"

	await message.answer(text=text, reply_markup=menu)
	














