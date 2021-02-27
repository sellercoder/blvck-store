from utils.misc.logging import *
from data.config import *
from aiogram import types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states.admin import Cms
from keyboards.admin.cms_menu import cms_menu
from utils.db_api.models import Page

# from utils.db_api.admin_db_commands import summary,admin_text,get_categories_help, get_categories_page

from loader import dp, bot

line = "➖"*11
info = "💬"
cms_title = "<b>Управление страницами</b>"

@dp.message_handler(user_id=ADMIN_ID, text="▫️Страницы", state="*")
async def cms_main(message: types.Message, state: FSMContext):
	logger.info(f"{message.chat.first_name}-{message.text}")
	text = f"{cms_title}\n\n<code>{info} Выбери страницу,которую желаешь изменить</code>"
	await message.answer(text=text, reply_markup=cms_menu)

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="cms_main", state="*")
async def edit_cms_main(call: CallbackQuery,state: FSMContext):
	logger.info(f"{call.data}")
	title = f"{info}\n"
	info_text = f"<code>Напиши новый текст или нажми </code>/cancel\n\n"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await Cms.set_home.set()

@dp.message_handler(user_id=ADMIN_ID, state=Cms.set_home)
async def sned_text(message: types.Message, state: FSMContext):
	try:
		Page.where('types', 'hello').first().body
		page = Page.where('types','hello').first()
	except:
		page = Page()
	
	page.body = message.text
	page.save()
	await state.reset_state()
	success_text = f"<code>{info} Успешно! Жми</code> /admin"
	await message.answer(success_text)


@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="cms_catalog", state="*")
async def edit_cms_catalog(call: CallbackQuery,state: FSMContext):
	logger.info(f"{call.data}")
	title = f"{info}\n"
	info_text = f"<code>Напиши новый текст или нажми </code>/cancel\n\n"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await Cms.set_catalog.set()

@dp.message_handler(user_id=ADMIN_ID, state=Cms.set_catalog)
async def sned_text(message: types.Message, state: FSMContext):
	page = Page.where('types','catalog').first()
	page.body = message.text
	page.save()
	await state.reset_state()
	success_text = f"<code>{info} Успешно! Жми</code> /admin"
	await message.answer(success_text)


@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="cms_about", state="*")
async def edit_cms_about(call: CallbackQuery,state: FSMContext):
	logger.info(f"{call.data}")
	title = f"{info}\n"
	info_text = f"<code>Напиши новый текст или нажми </code>/cancel\n\n"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await Cms.set_catalog.set()

@dp.message_handler(user_id=ADMIN_ID, state=Cms.set_catalog)
async def sned_text(message: types.Message, state: FSMContext):
	page = Page.where('types','about').first()
	page.body = message.text
	page.save()
	await state.reset_state()
	success_text = f"<code>{info} Успешно! Жми</code> /admin"
	await message.answer(success_text)

