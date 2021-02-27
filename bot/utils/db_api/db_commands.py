import json
import random
from typing import List
from utils.db_api.connect import db, schema
from utils.db_api.models import Category, Position, Item, User, Purchase, Payment, Coupon

# ==========================================
# Команды для Юзера,работы с его балансом  
# и покупкамм 

def register_user(uid,name,username):
	user = User.first_or_create(uid=uid,name=name,username=username)
	return user

def find_user(uid):
	user = User.where("uid", uid).first()
	return user

def add_money(user_id, money):
	user = User.find(user_id)
	start_balance = user.balance 
	finish_balance = start_balance + money
	user.balance = finish_balance
	user.save()
	return f"Баланс пополнен на сумму {money}"

def check_success_payment(comment):
	if Payment.where('comment', comment).first():
		return True
	else:
		return False

def add_payment(user,comment,amount):
	payment = Payment()
	payment.user_id = user
	payment.comment = comment
	payment.amount = amount
	payment.success = True
	payment.save()

def buy_item(item_id,user_id):
	item = Item.find(item_id)
	user = User.find(user_id)
	balance = user.balance
	check = balance - item.position.price
	if item.buy == True:
		return f"Уже куплено"
	elif check < 0:
		return f"Не хватает денег"
	else:
		purchase = Purchase()
		purchase.user_id = user_id
		purchase.item = item.jsn()
		if item.check_file() == True:
			purchase.is_file = True 
		purchase.save()
		if item.reusable == True:
			item.buy = False
		else:
			item.buy = True
		item.save()
		user.balance = check
		user.save()
		return f"Покупка прошла успешно"



def activate_coupon(coupon_uid, user_id):
	try:
		coupon = Coupon.where('uid', coupon_uid).first()
		dct = coupon.activators
		if user_id in dct['users']:
			return "Купон уже активирован!"
		else:
			user = User.find(user_id)
			add_money(user_id,int(coupon.amount))
			dct['users'].append(user_id)
			jsn = json.dumps(dct)
			coupon.update(activators=jsn)
			generate_comment = random.randint(10000000000000,50000000000000)
			payment = Payment()
			payment.user_id = user_id
			payment.provider = "coupon"
			payment.success = True
			payment.amount = coupon.amount
			payment.comment = generate_comment
			payment.save()
			return f"Купон успешно активирован! Деньги зачислены на ваш счет!"
	except:
		return "Такого купона не существует!"

# ==========================================
# Команды для каталога
def get_categories() -> List[Category]:
	return Category.stocked()

def get_user(uid):
	return User.where('uid', uid).first()

def get_category(category):
	return Category.find(category)

def get_positions(category) -> List[Position]:
	cat = Category.find(category)
	positions = cat.positions().stocked()
	return positions

def get_position(position):
	return Position.find(position)

def get_position_id(position):
	pos = Position.find(position)
	return pos.id

def get_category_id(position):
	pos = Position.find(position)
	return pos.category.id


# ==========================================
# Команды для админа
def summary():
	users_count = User.all().count()
	categories_count = Category.all().count()
	positions_count = Position.all().count()
	items_count = Item.all().count()
	return f"<b>📊 Статистика:</b>\n<code>📌 Категорий:</code> {categories_count}\n<code>📌 Позиций:</code> {positions_count}\n<code>📌 Товаров:</code> {items_count}\n<code>📌 Пользователей:</code> {users_count}"

def add_item(position_id, body):
	item = Item()
	item.body = body
	item.position_id = position_id
	item.save()
	return True



