from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.admin_db_commands import get_categories

cms_menu = InlineKeyboardMarkup(row_width=2)
cms_menu.insert(InlineKeyboardButton(text="Главная", callback_data="cms_main"))
cms_menu.insert(InlineKeyboardButton(text="Каталог", callback_data="cms_catalog"))
cms_menu.insert(InlineKeyboardButton(text="О магазине", callback_data="cms_about"))

