from utils.misc.logging import *
from data.config import *
from aiogram import types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states.admin import NewCategory, ChangeCategory, DeleteCategory
from keyboards.admin.admin_menu import admin_menu, categories_keyboard, categories_menu, cancel_menu,confirm_menu,one_category_keyboard
from utils.db_api.admin_db_commands import summary,admin_text,get_categories_help, get_categories_page
from utils.db_api.models import Category

from loader import dp, bot

line = "➖"*11
info = "💬"
categories_text = "<b>Управление категориями</b>"

@dp.message_handler(user_id=ADMIN_ID, text="▫️Категории", state="*")
async def admin_categories_page(message: types.Message, state: FSMContext):
	logger.info(f"{message.chat.first_name}-{message.text}")
	text = f"{categories_text}\n{get_categories_page()}\n<code>{info} Выбери необходимое действие - Изменить категорию, добавить новую или изменить существующую</code>" 
	await message.answer(text=text, reply_markup=categories_menu)

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="delete_category", state="*")
async def admin_delete_category_page(call: CallbackQuery,state: FSMContext):
	title = f"{info}\n"
	info_text = f"{get_categories_help()}\n<code>Пришли мне id категории которую нужно удалить или отправь</code> /admin <code>если передумал</code>"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await DeleteCategory.Id.set()

@dp.message_handler(user_id=ADMIN_ID, state=DeleteCategory.Id)
async def enter_id(message: types.Message, state: FSMContext):
	logger.info(f"Id категории: {message.text}")
	category_id = message.text
	category = Category.find(category_id)
	category.delete()
	await message.answer(f"<code>Категория удалена!</code>")
	summary_text = summary()
	text = admin_text(summary_text)
	await message.answer(text=text, reply_markup=admin_menu)
	await state.reset_state()

# ===============================================
@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="change_category", state="*")
async def admin_edit_category_page(call: CallbackQuery,state: FSMContext):
	title = f"{info}\n"
	info_text = f"{get_categories_help()}\n<code>{info} Пришли ID категории, которую нyжно изменить</code>"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await ChangeCategory.Id.set()

@dp.message_handler(user_id=ADMIN_ID, state=ChangeCategory.Id)
async def admin_id_category_page(message: types.Message, state: FSMContext):
	logger.info(f"Категория - {message.text}")
	category_id = message.text
	category = Category.find(category_id)
	await message.answer(f"{category.page()}\n\n<code>{info} Что нужно изменить в категории?</code>", reply_markup=one_category_keyboard(category_id))


@dp.callback_query_handler(user_id=ADMIN_ID, state=ChangeCategory.Id)
async def admin_edit_category_page(call: CallbackQuery,state: FSMContext):
	current_category = str(call.data).split(':')[2] 
	current_action = str(call.data).split(':')[1]
	logger.info(f"{call.data}")

	if current_action == "name":
		logger.info(f"Name")
		category = Category.find(current_category)
		category.id = current_category
		await call.message.edit_text(f"<code>{info}Напиши новое имя</code>")
		await ChangeCategory.Name.set()
		await state.update_data(category=category)
	
	elif current_action == "description":
		logger.info(f"Description")
		category = Category.find(current_category)
		category.id = current_category
		await call.message.edit_text(f"<code>{info}Пришли новое описание категории</code>")
		await ChangeCategory.Description.set()
		await state.update_data(category=category)

@dp.message_handler(user_id=ADMIN_ID, state=ChangeCategory.Name)
async def category_name(message: types.Message, state: FSMContext):
	data = await state.get_data()
	category: Category = data.get("category")
	name = message.text
	category = Category.find(category.id)
	category.update(name=name)
	await message.answer(f"{category.page()}\n<code>{info} Имя изменено! нажми</code> /admin")
	await state.reset_state()

@dp.message_handler(user_id=ADMIN_ID, state=ChangeCategory.Description)
async def category_description(message: types.Message, state: FSMContext):
	data = await state.get_data()
	category: Category = data.get("category")
	description = message.text
	category = Category.find(category.id)
	category.update(description=description)
	await message.answer(f"{category.page()}\n<code>{info} Описание изменено! нажми</code> /admin")
	await state.reset_state()



@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="add_category", state="*")
async def admin_add_category_page(call: CallbackQuery,state: FSMContext):
	title = f"{info}\n"
	info_text = f"<code>Пришли мне название категории</code>"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await NewCategory.Name.set()

@dp.message_handler(user_id=ADMIN_ID, state=NewCategory.Name)
async def enter_name(message: types.Message, state: FSMContext):
	logger.info(f"название категории: {message.text}")
	name = message.text
	category = Category()
	category.name = name
	await message.answer(f"<code>Теперь пришли описание категории</code>")
	await NewCategory.Description.set()
	await state.update_data(category=category)

@dp.message_handler(user_id=ADMIN_ID, state=NewCategory.Description)
async def enter_description(message: types.Message, state: FSMContext):
	data = await state.get_data()
	category: Category = data.get("category")
	description = message.text
	category.description = description
	await message.answer(text=f"<b>Название:</b> {category.name}\n<b>Описание:</b>\n{description}\n<code>{info}Все верно?</code>",reply_markup=confirm_menu)
	await NewCategory.Confirm.set()
	await state.update_data(category=category)

@dp.callback_query_handler(user_id=ADMIN_ID, state=NewCategory.Confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
	if call.data == "cancel":
		cancel_text = f"<code>{info} Добавление категории отменено</code>"
		await call.message.edit_text(cancel_text)
	else:
		data = await state.get_data()
		category: Category = data.get("category")
		category.save()
		success_text = f"<code>{info} Категория: <b>{category.name}</b> успешно создана!\nНе забудь добавить в нее позиции, а в позиции товары 😀</code>"
		await call.message.edit_text(success_text)

	await call.answer(cache_time=1)
	summary_text = summary()
	text = admin_text(summary_text)
	await call.message.answer(text=text, reply_markup=admin_menu)
	await state.reset_state()

@dp.message_handler(user_id=ADMIN_ID, state=NewCategory.Confirm)
async def confirm(message: types.Message, state: FSMContext):
	await message.answer(text=f"<code>{info} Вообще-то я спросил верно или нет... 👆</code>")

@dp.message_handler(user_id=ADMIN_ID, state=ChangeCategory.Confirm)
async def confirm(message: types.Message, state: FSMContext):
	await message.answer(text=f"<code>{info} Вообще-то я спросил верно или нет... 👆</code>")




