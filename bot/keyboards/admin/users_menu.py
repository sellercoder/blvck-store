from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup


users_menu = InlineKeyboardMarkup(row_width=2)
users_menu.insert(InlineKeyboardButton(text="🎟 Купоны", callback_data="coupons"))

coupons_menu = InlineKeyboardMarkup(row_width=2)
coupons_menu.insert(InlineKeyboardButton(text="➕ Добавить купон", callback_data="add_coupon"))
coupons_menu.insert(InlineKeyboardButton(text="🗑 Удалить купон", callback_data="delete_coupon"))

coupon_confirm_menu = InlineKeyboardMarkup(row_width=2)
coupon_confirm_menu.insert(InlineKeyboardButton(text="✅ Добавить купон", callback_data="yes"))
coupon_confirm_menu.insert(InlineKeyboardButton(text="🙅‍♂️ Отмена", callback_data="cancel"))