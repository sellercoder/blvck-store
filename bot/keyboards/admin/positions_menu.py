from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup

positions_menu = InlineKeyboardMarkup(row_width=2)
positions_menu.insert(InlineKeyboardButton(text="✏️ Изменить", callback_data="change_position"))
positions_menu.insert(InlineKeyboardButton(text="➕ Добавить", callback_data="add_position"))
positions_menu.insert(InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_position"))

confirm_menu = InlineKeyboardMarkup(row_width=2)
confirm_menu.insert(InlineKeyboardButton(text="✅ Да, верно", callback_data="confirm"))
confirm_menu.insert(InlineKeyboardButton(text="🙅‍♂️ Отмена", callback_data="cancel"))


reusable_menu = InlineKeyboardMarkup(row_width=2)
reusable_menu.insert(InlineKeyboardButton(text="Много товаров", callback_data="one_buy_one_item"))
reusable_menu.insert(InlineKeyboardButton(text="Один товар", callback_data="multi"))

def one_position_keyboard(positions_id):
	markup = InlineKeyboardMarkup(row_width=2)
	markup.insert(InlineKeyboardButton(
		text="Название", callback_data=f"change:name:{positions_id}"))
	markup.insert(InlineKeyboardButton(
		text="Описание", callback_data=f"change:description:{positions_id}"))
	markup.insert(InlineKeyboardButton(
		text="Цену", callback_data=f"change:price:{positions_id}"))
	markup.insert(InlineKeyboardButton(
		text="Категорию", callback_data=f"change:category_id:{positions_id}"))
	return markup

