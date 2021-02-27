from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from utils.db_api.db_commands import Purchase, User

pr_menu_cd = CallbackData("show_menu_purchases", "level", "user", "purchase")
def make_pr_callback_data(level, user, purchase="0"):
    return pr_menu_cd.new(level=level, user=user, purchase=purchase)

def purchases_keyboard(user):
	# Указываем, что текущий уровень меню - 0
	CURRENT_LEVEL = 0

	# Создаем клавиатуру
	markup = InlineKeyboardMarkup(row_width=2)

	current_user = User.where('uid',user).first()

	# Забираем список категорий из базы и итерируемся
	purchases = current_user.purchases

	for purchase in purchases:

		# Формируем текст на кнопке 
		button_text = f"{purchase.title()}"

		# Формируем коллбэк на кнопке
		callback_data = make_pr_callback_data(level=CURRENT_LEVEL + 1, user=current_user.id, purchase=purchase.id)
		markup.insert(
			InlineKeyboardButton(text=button_text, callback_data=callback_data)
			)
	return markup









