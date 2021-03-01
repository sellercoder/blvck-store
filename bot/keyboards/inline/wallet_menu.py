from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

def wallet_keyboard():
	
	# Создаем клавиатуру
	markup = InlineKeyboardMarkup(row_width=1)
	qiwi_button = "🥝 Qiwi перевод"
	qiwi_new_button = "🥝 QiwiP2P счёт"
	cupon_button = "🎟 Ввести купон"
	history_button = "📒 История платежей"
	# 🎫

	markup.insert(
		InlineKeyboardButton(text=qiwi_button, callback_data="qiwi"))
	markup.insert(
		InlineKeyboardButton(text=qiwi_new_button, callback_data="qnew"))
	markup.insert(
		InlineKeyboardButton(text=cupon_button, callback_data="coupon"))
	markup.insert(
		InlineKeyboardButton(text=history_button, callback_data="history"))

	return markup


def check_qiwi_pay_keyboard(comment):
	
	# Создаем клавиатуру
	markup = InlineKeyboardMarkup(row_width=2)

	check_button = "Проверить оплату"
	data = f"check:{comment}"

	markup.insert(
		InlineKeyboardButton(text=check_button, callback_data=data))

	return markup