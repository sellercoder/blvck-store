from utils.misc.logging import *
from data.config import *
from aiogram import types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states.admin import NewPosition, DeletePosition, ChangePosition
from keyboards.admin.admin_menu import admin_menu
from keyboards.admin.positions_menu import positions_menu, confirm_menu,reusable_menu,one_position_keyboard
from utils.db_api.admin_db_commands import get_categories_help,summary,admin_text, get_positions_page, get_positions_help
from utils.db_api.models import Position, Category

from loader import dp, bot

line = "➖"*11
info = "💬"
positions_text = "<b>Управление позициями</b>"

@dp.message_handler(user_id=ADMIN_ID, text="▫️Позиции", state="*")
async def admin_positions_page(message: types.Message, state: FSMContext):
	logger.info(f"{message.chat.first_name}-{message.text}")
	text = f"{positions_text}\n{get_positions_page()}"
	await message.answer(text=text, reply_markup=positions_menu)

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="delete_position", state="*")
async def admin_delete_position_page(call: CallbackQuery,state: FSMContext):
	help_positions_text = get_positions_help()
	title = f"{info}\n"
	info_text = f"{help_positions_text}\n<code>{info} Пришли ID позиции, которую нужно удалить.\n⚠️ Внимание, после отправки id - позиция будет сразу удалена, товары в этой позиции, так же будут удалены</code>"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await DeletePosition.Id.set()

@dp.message_handler(user_id=ADMIN_ID, state=DeletePosition.Id)
async def enter_id(message: types.Message, state: FSMContext):
	position_id = message.text
	position = Position.find(position_id)
	position.delete()
	await message.answer(f"<code>Позиция удалена!</code>")
	summary_text = summary()
	text = admin_text(summary_text)
	await message.answer(text=text, reply_markup=admin_menu)
	await state.reset_state()

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="change_position", state="*")
async def admin_change_position_page(call: CallbackQuery,state: FSMContext):
	help_positions_text = get_positions_help()
	title = f"{info}\n"
	info_text = f"{help_positions_text}\n<code>{info} Пришли ID позиции, которую нyжно изменить</code>"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await ChangePosition.Id.set()

@dp.message_handler(user_id=ADMIN_ID, state=ChangePosition.Id)
async def admin_id_position_page(message: types.Message, state: FSMContext):
	logger.info(f"Позиция - {message.text}")
	position_id = message.text
	position = Position.find(position_id)
	await message.answer(f"{position.info_page()}\n\n<code>{info} Что нужно изменить в позиции?</code>", reply_markup=one_position_keyboard(position_id))

@dp.callback_query_handler(user_id=ADMIN_ID, state=ChangePosition.Id)
async def admin_edit_position_page(call: CallbackQuery,state: FSMContext):
	current_position = str(call.data).split(':')[2] 
	current_action = str(call.data).split(':')[1]

	if current_action == "name":
		logger.info(f"Name")
		position = Position.find(current_position)
		position.id = current_position
		await call.message.edit_text(f"<code>{info}Напиши новое имя</code>")
		await ChangePosition.Name.set()
		await state.update_data(position=position)
	
	elif current_action == "description":
		logger.info(f"Description")
		position = Position.find(current_position)
		position.id = current_position
		await call.message.edit_text(f"<code>{info}Пришли новое описание для позиции</code>")
		await ChangePosition.Description.set()
		await state.update_data(position=position)

	elif current_action == "price":
		logger.info(f"Price")
		position = Position.find(current_position)
		position.id = current_position
		await call.message.edit_text(f"<code>{info}Пришли новую цену для позиции</code>")
		await ChangePosition.Price.set()
		await state.update_data(position=position)

	elif current_action == "category_id":
		logger.info(f"CategoryID")
		position = Position.find(current_position)
		position.id = current_position
		await call.message.edit_text(f"{get_categories_help()}\n\n<code>{info}Пришли id категории для позиции</code>")
		await ChangePosition.CategoryID.set()
		await state.update_data(position=position)

@dp.message_handler(user_id=ADMIN_ID, state=ChangePosition.Name)
async def position_name(message: types.Message, state: FSMContext):
	data = await state.get_data()
	position: Position = data.get("position")
	name = message.text
	position = Position.find(position.id)
	position.update(name=name)
	await message.answer(f"{position.info_page()}\n<code>{info} Имя изменено! нажми</code> /admin")
	await state.reset_state()

@dp.message_handler(user_id=ADMIN_ID, state=ChangePosition.Description)
async def position_description(message: types.Message, state: FSMContext):
	data = await state.get_data()
	position: Position = data.get("position")
	description = message.text
	position = Position.find(position.id)
	position.update(description=description)
	await message.answer(f"{position.info_page()}\n<code>{info} Описание изменено! нажми</code> /admin")
	await state.reset_state()

@dp.message_handler(user_id=ADMIN_ID, regexp=r"^(\d+)$", state=ChangePosition.Price)
async def position_price(message: types.Message, state: FSMContext):
	data = await state.get_data()
	position: Position = data.get("position")
	price = message.text
	position = Position.find(position.id)
	position.update(price=price)
	await message.answer(f"{position.info_page()}\n<code>{info} Цена изменена! нажми</code> /admin")
	await state.reset_state()

@dp.message_handler(user_id=ADMIN_ID, state=ChangePosition.Price)
async def confirm(message: types.Message, state: FSMContext):
	await message.answer(text=f"<code>{info}Цену пиши цифрами...</code>")


@dp.message_handler(user_id=ADMIN_ID, regexp=r"^(\d+)$", state=ChangePosition.CategoryID)
async def position_price(message: types.Message, state: FSMContext):
	data = await state.get_data()
	position: Position = data.get("position")
	category_id = message.text
	position = Position.find(position.id)
	position.update(category_id=category_id)
	await message.answer(f"{position.info_page()}\n<code>{info} Категория изменена! нажми</code> /admin")
	await state.reset_state()

@dp.message_handler(user_id=ADMIN_ID, state=ChangePosition.CategoryID)
async def categoryid(message: types.Message, state: FSMContext):
	await message.answer(text=f"<code>{info}Нужен id категории...</code>")


# ==============================================================


@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="add_position", state="*")
async def admin_add_position_page(call: CallbackQuery,state: FSMContext):
	logger.info(f"{call.data}")
	help_categories_text = get_categories_help()
	title = f"{info}\n"
	info_text = f"<code>Для начала пришли ID категории в которую хочешь добавить позицию.</code>\n\n{help_categories_text}"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await NewPosition.CategoryID.set()


@dp.message_handler(user_id=ADMIN_ID, regexp=r"^(\d+)$", state=NewPosition.CategoryID)
async def enter_id(message: types.Message, state: FSMContext):
	category_id = message.text
	if Category.find(category_id) == None:
		logger.info(f"Такой категории не существует!")
		await message.answer(text=f"<code>{info} Такой категории не существует!</code>\n\n{get_categories_help()}")
	else:
		logger.info(f"Есть такая")
		position = Position()
		position.category_id = category_id
		await message.answer(f"<code>{info}Позиция для одного товара?</code>", reply_markup=reusable_menu)
		await NewPosition.Reusable.set()
		await state.update_data(position=position)

@dp.message_handler(user_id=ADMIN_ID, state=NewPosition.Reusable)
async def wtf(message: types.Message, state: FSMContext):
    await message.answer(f"{info} Позиция для одного товара?", reply_markup=reusable_menu)

@dp.callback_query_handler(user_id=ADMIN_ID, state=NewPosition.Reusable)
async def one_ore_many(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	position: Position = data.get("position")
	print(call.data)
	if call.data == "multi":
		position.reusable = True
	else:
		position.reusable = False
	await call.message.edit_text(f"<code>{info}Теперь пришли мне имя позиции</code>")
	await NewPosition.Name.set()
	await state.update_data(position=position)

@dp.message_handler(user_id=ADMIN_ID, state=NewPosition.CategoryID)
async def not_quantity_id(message: types.Message, state: FSMContext):
    await message.answer(f"{info} Неверное значение, введи число\n{get_categories_help()}")

@dp.message_handler(user_id=ADMIN_ID, state=NewPosition.Name)
async def enter_name(message: types.Message, state: FSMContext):
	data = await state.get_data()
	position: Position = data.get("position")
	name = message.text
	position.name = name
	await message.answer(text=f"<code>{info} Теперь пришли мне описание позиции</code>")
	await NewPosition.Description.set()
	await state.update_data(position=position)

@dp.message_handler(user_id=ADMIN_ID, state=NewPosition.Description)
async def enter_description(message: types.Message, state: FSMContext):
	data = await state.get_data()
	position: Position = data.get("position")
	description = message.text
	position.description = description
	await message.answer(text=f"<code>{info} Теперь пришли мне цену позиции</code>")
	await NewPosition.Price.set()
	await state.update_data(position=position)


@dp.message_handler(user_id=ADMIN_ID, regexp=r"^(\d+)$", state=NewPosition.Price)
async def not_quantity(message: types.Message, state: FSMContext):
	data = await state.get_data()
	position: Position = data.get("position")
	price = message.text
	position.price = price
	category_id = position.category_id
	category = Category.find(category_id)
	await message.answer(text=f"<b>Категория:</b> {category.name}\n<b>Название:</b> {position.name}\n<b>Описание:</b>\n{position.description}\n<b>Цена:</b> {position.price}\n\n<code>{info} Все верно?</code>",reply_markup=confirm_menu)
	await NewPosition.Confirm.set()
	await state.update_data(position=position)


@dp.message_handler(user_id=ADMIN_ID, state=NewPosition.Price)
async def enter_price(message: types.Message, state: FSMContext):
    await message.answer(f"<code>{info} Цену нужно писать цифрой 😀</code>")


@dp.callback_query_handler(user_id=ADMIN_ID, state=NewPosition.Confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
	if call.data == "cancel":
		cancel_text = f"<code>{info} Создание позиции отменено</code>"
		await call.message.edit_text(cancel_text)
	else:
		data = await state.get_data()
		position: Position = data.get("position")
		position.save()
		success_text = f"<code>{info} Позиция: <b>{position.name}</b> успешно создана!\nНе забудь добавить товары 😀</code>"
		await call.message.edit_text(success_text)

	await call.answer(cache_time=1)
	summary_text = summary()
	text = admin_text(summary_text)
	await call.message.answer(text=text, reply_markup=admin_menu)
	await state.reset_state()

@dp.message_handler(user_id=ADMIN_ID, state=NewPosition.Confirm)
async def confirm(message: types.Message, state: FSMContext):
	await message.answer(text=f"<code>{info} Вообще-то я спросил верно или нет... 👆</code>")






















