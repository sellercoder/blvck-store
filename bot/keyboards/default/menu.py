from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
	keyboard=[
	  [
	  	KeyboardButton(text="🗃 Каталог"),
	  	KeyboardButton(text="🛒 Покупки")
	  ],
	  [
	  	KeyboardButton(text="💳 Кошелек"),
	  	KeyboardButton(text="📕 О магазине")
	  ],
	],
	resize_keyboard = True
)

