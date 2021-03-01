from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
	keyboard=[
	  [
	  	KeyboardButton(text="🤙 Купить "),
	  	KeyboardButton(text="📂 Покупки ")
	  ],
	  [
	  	KeyboardButton(text="💳 Баланс"),
	  	KeyboardButton(text="⚙️  Помощь")
	  ],
	],
	resize_keyboard = True
)

