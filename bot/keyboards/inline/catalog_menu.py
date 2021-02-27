from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from utils.db_api.db_commands import get_categories, get_positions, get_position_id, get_category_id, get_category

#` Функция формирующая колбэк, содержит уровень(всегда), категорию(может быть 0), позицию(может быть 0) и юзера (может быть 0)
menu_cd = CallbackData("show_menu", "level", "category", "position", "user")
def make_callback_data(level, category="0", position="0", user="0"):
    return menu_cd.new(level=level, category=category, position=position, user=user)

def categories_keyboard():
	# Указываем, что текущий уровень меню - 0
	CURRENT_LEVEL = 0

	# Создаем клавиатуру
	markup = InlineKeyboardMarkup(row_width=2)

	# Забираем список категорий из базы и итерируемся
	categories = get_categories()

	for category in categories:

		# Формируем текст на кнопке 
		button_text = f"{category.name}"

		# Формируем коллбэк на кнопке
		callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category.id)
		markup.insert(
			InlineKeyboardButton(text=button_text, callback_data=callback_data)
			)
	return markup

def positions_keyboard(category):
    # Текущий уровень - 1
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    positions = get_positions(category)
    for position in positions:

        # Сформируем текст, который будет на кнопке
        button_text = f"{position.name} за {position.formated_price()}"

        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category, position=position.id)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )
    return markup

def position_keyboard(position, user):
    # Текущий уровень - 2
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()

    pos = get_position_id(position)
    cat = get_category_id(position)

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 1.
    markup.row(
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=cat, position=pos)),
        InlineKeyboardButton(
            text="🛒 Купить",
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1, category=cat, position=pos, user=user))
    )
    return markup

def buy_position_keyboard(position, user):
    # Текущий уровень - 3
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()

    pos = get_position_id(position)
    cat = get_category_id(position)

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="✅ Подтверждаю",
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1, category=cat, position=pos, user=user)),
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=cat, position=pos))
    )
    return markup

def add_money_keyboard(position):
    # Текущий уровень - 3
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()

    pos = get_position_id(position)
    cat = get_category_id(position)

    markup.row(
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=cat, position=pos))
    )
    return markup
