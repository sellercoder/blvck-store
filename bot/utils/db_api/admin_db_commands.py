from typing import List
from utils.db_api.connect import db
from utils.db_api.models import Category, Position, Item, User, Purchase, Payment, Coupon,Token

line = "➖"*11
info = "💬"

# ==========================================
# Команды для админа

def admin_text(txt): 
	return f"<b>🎛 Панель управления ботом.</b>\n\nДля выхода в обычный режим отправь команду /start\n\n{txt}"

def summary():
	users_count = User.all().count()
	categories_count = Category.all().count()
	positions_count = Position.all().count()
	items_count = Item.stocked().count()
	coupons_count = Coupon.all().count()
	return f"<b>📊 Статистика:</b>\n<code>📌 Категорий:</code> {categories_count}\n<code>📌 Позиций:</code> {positions_count}\n<code>📌 Товаров:</code> {items_count}\n<code>📌 Пользователей:</code> {users_count}\n<code>📌 Купонов:</code> {coupons_count}\n"

def get_categories() -> List[Category]:
	return Category.all()

def get_categories_page():
	clean_string = ""
	categories = Category.all()
	for category in categories:
		uid = category.id
		name = category.name
		description = category.description
		title = f"{line}\n 🆔 {uid} <b>Имя:</b> {name} <b>Описание:</b> <i>{description}</i>\n"
		clean_string+=title
	return clean_string

def get_categories_help():
	clean_string = ""
	categories = Category.all()
	for category in categories:
		uid = category.id
		name = category.name
		title = f"{uid} - {name}\n"
		clean_string+=title
	return clean_string

def get_positions_page():
	clean_string = ""
	positions = Position.all()
	for position in positions:
		uid = position.id
		name = position.name
		description = position.description
		title = f"{line}\n 🆔 {uid} <b>Имя:</b> {name}\n<b>Описание:</b> <i>{description}</i>\n<b>Категория:</b> {position.category.name}\n"
		clean_string+=title
	return clean_string

def get_positions_help():
	clean_string = ""
	positions = Position.all()
	for position in positions:
		position_id = position.id
		position_name = position.name
		title = f"{position_id} - {position_name} - {position.category.name}\n"
		clean_string+=title
	return clean_string

def get_items_page():
	clean_string = ""
	items = Item.where('buy', False).get()
	for item in items:
		uid = item.id
		position = item.position.name
		category = item.position.category.name
		title = f"{line}\n <b>Товар 🆔 {uid}</b> в позиции: {position} и категории {category}\n"
		clean_string+=title
	return clean_string


def get_users_info():
	users = User.all()
	count = users.count()
	cp_count = Coupon.all().count()
	users_list = f"{line}\n<b>Юзеры:</b>\n{line}\n"
	for user in users:
		users_list += f"{user.info()}\n"
	return f"Всего юзеров в системе: {count}\nРабочих купонов: {cp_count}\n{users_list}"

def coupons_page():
	"""Возвращает информацию о купонах"""
	clean_string = ""
	coupons = Coupon.all()
	for coupon in coupons:
		coupon_id = coupon.id
		coupon_uid = coupon.uid
		coupon_amount = coupon.formated_amount()
		title = f"<b>🆔 {coupon_id}</b> <code>{coupon_uid}</code> {coupon_amount}\nСколько юзеров активировало: {coupon.activators_count()}\n{line}\n"
		clean_string+=title
	return clean_string

def create_coupon(uid,amount):
	try:
		Coupon.create(uid=uid,amount=amount)
		return f"Купон на сумму {amount} создан"
	except:
		return "Такой купон уже есть"

def create_token(token,phone):
	if Token.all().count() > 0:
		Token.first().delete()
	res = Token.create(token=token, phone=phone)
	return res

def get_token():
	token = Token.first()
	return token




















