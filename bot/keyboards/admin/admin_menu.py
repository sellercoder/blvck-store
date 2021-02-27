from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.admin_db_commands import get_categories

admin_menu = ReplyKeyboardMarkup(
	keyboard=[
	  [
	  	KeyboardButton(text="▫️Категории"),
	  	KeyboardButton(text="▫️Позиции")
	  ],
	  [
	  	KeyboardButton(text="▫️Товары"),
	   	KeyboardButton(text="▫️ Юзеры")
	  ],
	  [
	  	KeyboardButton(text="▫️Платежка"),
	   	KeyboardButton(text="▫️Страницы")
	  ]
	],
	resize_keyboard = True)

categories_menu = InlineKeyboardMarkup(row_width=2)
categories_menu.insert(InlineKeyboardButton(text="✏️ Изменить", callback_data="change_category"))
categories_menu.insert(InlineKeyboardButton(text="➕ Добавить", callback_data="add_category"))
categories_menu.insert(InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_category"))

admin_wallet_menu = InlineKeyboardMarkup(row_width=1)
admin_wallet_menu.insert(InlineKeyboardButton(text="✏️ Изменить токен", callback_data="change_token"))



cancel_menu = InlineKeyboardMarkup(
	inline_keyboard=
		[
			[InlineKeyboardButton(text="Отмена", callback_data="cancel")],
		]
	)

confirm_menu = InlineKeyboardMarkup(row_width=2)
confirm_menu.insert(InlineKeyboardButton(text="✅ Да, верно", callback_data="confirm"))
confirm_menu.insert(InlineKeyboardButton(text="🙅‍♂️ Отменить", callback_data="cancel"))


def one_category_keyboard(category_id):
	markup = InlineKeyboardMarkup(row_width=2)
	markup.insert(InlineKeyboardButton(
		text="Название", callback_data=f"change:name:{category_id}"))
	markup.insert(InlineKeyboardButton(
		text="Описание", callback_data=f"change:description:{category_id}"))
	return markup




def categories_keyboard():

	# Создаем клавиатуру
	markup = InlineKeyboardMarkup(row_width=2)

	# Забираем список категорий из базы и итерируемся
	categories = get_categories()

	for category in categories:

		# Формируем текст на кнопке 
		button_text = f"{category.name}"
		callback_data = f"category:{category.id}"

		markup.insert(
			InlineKeyboardButton(text=button_text, callback_data=callback_data)
			)
	return markup


