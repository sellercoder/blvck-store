from utils.misc.logging import *
from data.config import *
from aiogram import types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.admin import NewItem, DeleteItem, ManyItems
from keyboards.admin.items_menu import items_menu, file_ore_text_keyboard,confirm_keyboard,reusable_keyboard,change_item_menu
from keyboards.admin.admin_menu import admin_menu
from utils.db_api.models import Position, Category, Item
from utils.db_api.admin_db_commands import get_positions_help,summary,admin_text, get_items_page

from loader import dp, bot

line = "➖"*11
info = "💬"
items_text = "Управление товарами"

@dp.message_handler(user_id=ADMIN_ID, text="▫️Товары", state="*")
async def admin_positions_page(message: types.Message, state: FSMContext):
	logger.info(f"{message.chat.first_name}-{message.text}")
	text = f"{items_text}\n{get_items_page()}"
	await message.answer(text=text, reply_markup=items_menu)

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="multi", state="*")
async def admin_itempage(call: CallbackQuery,state: FSMContext):
	logger.info(f"{call.data}")
	help_position_text = get_positions_help()
	title = f"{info}\n"
	info_text = f"<code>Для начала пришли ID позиции в которую хочешь добавить товар.</code>\n\n{help_position_text}"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await ManyItems.PositionID.set()

@dp.message_handler(user_id=ADMIN_ID, regexp=r"^(\d+)$", state=ManyItems.PositionID)
async def enter_id(message: types.Message, state: FSMContext):
	position_id = message.text
	info_text = f"Теперь пришли мне сообщение, где каждая строчка - товар"
	await ManyItems.SetLines.set()
	await state.update_data(position_id=position_id)
	await message.answer(text=info_text)

@dp.message_handler(user_id=ADMIN_ID, state=ManyItems.SetLines)
async def update_all(message: types.Message, state: FSMContext):
	data = await state.get_data()
	position_id = data.get("position_id")
	f = message.text.split("\n")
	for line in f:
		print(line)
		Item.create(position_id=position_id, body=f"{line}")
	await state.reset_state()
	await message.answer(text="Товары загружены - жми /admin")

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="add_item", state="*")
async def admin_add_item_page(call: CallbackQuery,state: FSMContext):
	logger.info(f"{call.data}")
	help_position_text = get_positions_help()
	title = f"{info}\n"
	info_text = f"<code>Для начала пришли ID позиции в которую хочешь добавить товар.</code>\n\n{help_position_text}"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await NewItem.PositionID.set()

@dp.message_handler(user_id=ADMIN_ID, regexp=r"^(\d+)$", state=NewItem.PositionID)
async def enter_id(message: types.Message, state: FSMContext):
	position_id = message.text
	if Position.find(position_id) == None:
		logger.info(f"Такой позиции не существует!")
		await message.answer(text=f"<code>{info} Такой позиции не существует!</code>\n\n{get_positions_help()}")
	else:
		logger.info(f"Есть такая")
		position = Position.find(position_id)
		if position.reusable == True:
			if position.items.count() == 0:
				logger.info(f"Позиция для одного товара")
				item = Item()
				item.reusable = True
				item.position_id = position_id
				await message.answer(f"<code>{info}Чем является товар? Файлом или текстом</code>", reply_markup=file_ore_text_keyboard)
				await NewItem.IsText.set()
				await state.update_data(item=item)
			else:
				logger.info(f"Тут есть товар")
				await message.answer(f"<code>{info} Позиция для одного товара и в ней уже есть товар. Удалите ее и создайте новую, выбрав тип 'много товаров'. Вернуться в меню </code> /admin")
		else:
			logger.info(f"Позиция для нескольких товаров")
			item = Item()
			item.reusable = False
			item.position_id = position_id
			await message.answer(f"<code>{info}Чем является товар? Файлом или текстом?</code>", reply_markup=file_ore_text_keyboard)
			await NewItem.IsText.set()
			await state.update_data(item=item)

@dp.message_handler(user_id=ADMIN_ID, state=NewItem.PositionID)
async def not_id(message: types.Message, state: FSMContext):
    await message.answer(f"<code>{info} Нужно ввести ID позиции</code>\n\n{get_positions_help()}")

@dp.message_handler(user_id=ADMIN_ID, state=NewItem.IsText)
async def not_id(message: types.Message, state: FSMContext):
    await message.answer(f"<code>{info} Чем является товар? Файлом или текстом?</code>\n\n", reply_markup=file_ore_text_keyboard)

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="file", state=NewItem.IsText)
async def upload_file(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	item: Item = data.get("item")
	item.is_file = True
	await state.update_data(item=item)
	await NewItem.UploadFile.set()
	await call.message.edit_text(f"<code>{info} Хорошо, файл. Прошли мне файл.</code>\n\n")

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="text", state=NewItem.IsText)
async def set_text(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	item: Item = data.get("item")
	item.is_file = False
	await state.update_data(item=item)
	await NewItem.SendText.set()
	await call.message.edit_text(f"<code>{info} Хорошо, текст. пришли мне этот текст.</code>\n\n")

@dp.message_handler(user_id=ADMIN_ID, content_types=types.ContentTypes.DOCUMENT, state=NewItem.UploadFile)
async def sned_text(message: Message, state: FSMContext):
	data = await state.get_data()
	item: Item = data.get("item")
	item.body = message['document']['file_id']
	await state.update_data(item=item)
	await NewItem.Confirm.set()
	await message.answer(f"Товар в позиции {item.position.name}<code>{info} Добавить?</code>\n\n", reply_markup=confirm_keyboard)

@dp.message_handler(user_id=ADMIN_ID, state=NewItem.UploadFile)
async def not_file(message: types.Message, state: FSMContext):
    await message.answer(f"<code>{info} Мне нужен файл...</code>\n\n")

@dp.message_handler(user_id=ADMIN_ID, state=NewItem.SendText)
async def sned_text(message: types.Message, state: FSMContext):
	data = await state.get_data()
	item: Item = data.get("item")
	item.body = message.text
	await state.update_data(item=item)
	await NewItem.Confirm.set()
	await message.answer(item.page(), reply_markup=confirm_keyboard)
	# await message.answer(f"{item.position.name} - {item.is_file} - {item.body}<code>{info} Все верно?</code>\n\n", reply_markup=confirm_keyboard)

@dp.callback_query_handler(user_id=ADMIN_ID, state=NewItem.Confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
	if call.data == "confirm":
		data = await state.get_data()
		item: Item = data.get("item")
		item.save()
		success_text = f"<code>{info} Товар успешно добавлен!</code>"
		await call.message.edit_text(success_text)
		await call.answer(cache_time=1)
	else:
		cancel_text = f"<code>{info} Вы отменили создание товара!</code>"
		await call.message.edit_text(cancel_text)
		await call.answer(cache_time=1)

	summary_text = summary()
	text = admin_text(summary_text)
	await call.message.answer(text=text, reply_markup=admin_menu)
	await state.reset_state()

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="delete_item", state="*")
async def admin_delete_item_page(call: CallbackQuery,state: FSMContext):
	title = f"{info}\n"
	info_text = f"{get_items_page()}\n<code>{info} Пришли ID товара, который нужно удалить.\n⚠️ Внимание, после отправки id - товар будет сразу удален!</code>"
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await DeleteItem.Id.set()

@dp.message_handler(user_id=ADMIN_ID, state=DeleteItem.Id)
async def enter_id(message: types.Message, state: FSMContext):
	item_id = message.text
	item = Item.find(item_id)
	item.delete()
	await message.answer(f"<code>Товар удален!</code>")
	summary_text = summary()
	text = admin_text(summary_text)
	await message.answer(text=text, reply_markup=admin_menu)
	await state.reset_state()









































