from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup

items_menu = InlineKeyboardMarkup(row_width=2)
items_menu.insert(InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_item"))
items_menu.insert(InlineKeyboardButton(text="➕ Добавить", callback_data="add_item"))

file_ore_text_keyboard = InlineKeyboardMarkup(row_width=2)
file_ore_text_keyboard.insert(InlineKeyboardButton(text="📁 Файл", callback_data="file"))
file_ore_text_keyboard.insert(InlineKeyboardButton(text="🗒 Текст", callback_data="text"))

confirm_keyboard = InlineKeyboardMarkup(row_width=2)
confirm_keyboard.insert(InlineKeyboardButton(text="✅ Да, верно", callback_data="confirm"))
confirm_keyboard.insert(InlineKeyboardButton(text="🙅‍♂️ Отмена", callback_data="cancel"))

reusable_keyboard = InlineKeyboardMarkup(row_width=2)
reusable_keyboard.insert(InlineKeyboardButton(text="✅ Да", callback_data="yes"))
reusable_keyboard.insert(InlineKeyboardButton(text="🙅‍♂️ Нет", callback_data="no"))

change_item_menu = InlineKeyboardMarkup(row_width=2)
change_item_menu.insert(InlineKeyboardButton(text="Загрузить другой товар в позицию", callback_data="upload_new"))


