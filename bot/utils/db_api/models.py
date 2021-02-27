import json
import pendulum
from money import Money

from utils.db_api.connect import db

from orator import Model
from orator.orm import has_many
from orator.orm import belongs_to
from orator.orm import has_many_through
from orator.orm import scope

line = "➖" * 11

class User(Model):
	__guarded__ = ['created_at', 'updated_at']
	
	@has_many
	def purchases(self):
		return Purchase
	@has_many
	def payments(self):
		return Payment

	def formated_balance(self):
		price = self.balance
		m = Money(price, 'RUB')
		frmt = m.format('ru_RU',currency_digits=False)
		return frmt

	def get_dt(self):
		obj = str(self.created_at)
		dt = pendulum.parse(obj)
		return dt.strftime("🗓  %-d.%m.%yг.")

	def wallet_info(self):
		return f"Ваш баланс {self.formated_balance()}"

	def info(self):
		return f"@{self.username} - {self.name} - {self.uid} /info_{self.uid}"

	def full_info(self):
		purch = self.purchases
		purch_list = ""
		for purchase in purch:
			purch_list+=f"{purchase.for_admin_page()}\n"

		return f"{line}\n{self.uid}\n{line}\n<b>Имя:</b> {self.name}\n<b>Никнейм:</b> @{self.username}\n<b>Баланс:</b> {self.formated_balance()}\n<b>Регистрация:</b>{self.get_dt()}\n<b>Покупок:</b> {self.purchases.count()}\n{purch_list}\n"


class Coupon(Model):
	__guarded__ = ['created_at', 'updated_at']

	def formated_amount(self):
		amount = self.amount
		m = Money(amount, 'RUB')
		frmt = m.format('ru_RU',currency_digits=False)
		return frmt

	def activators_count(self):
		return len(self.activators['users'])


class Payment(Model):
	@belongs_to
	def user(self):
		return User

	def formated_amount(self):
		amount = self.amount
		m = Money(amount, 'RUB')
		frmt = m.format('ru_RU',currency_digits=False)
		return frmt

	def get_dt(self):
		obj = str(self.created_at)
		dt = pendulum.parse(obj)
		return dt.strftime("🗓  %-d.%m.%yг.")


class Purchase(Model):
	@belongs_to
	def user(self):
		return User

	def get_dt(self):
		obj = str(self.created_at)
		dt = pendulum.parse(obj)
		return dt.strftime("🗓 %-d.%m.%yг. ⏳ %H:%M")

	def formated_price(self):
		price = self.item['price']
		m = Money(price, 'RUB')
		frmt = m.format('ru_RU',currency_digits=False)
		return frmt

	def title(self):
		price = self.formated_price()
		category = self.item['category']
		position = self.item['position']
		return f"{self.get_dt()}"

	def for_admin_page(self):
		price = self.formated_price()
		category = self.item['category']
		position = self.item['position']
		date = self.get_dt()
		return f"{line}\n<b>◻️</b>{category}<b>◻️</b>{position}\n<b>◻️</b>{price} {date}"
	
	def page(self):
		if self.is_file == True:
			body = "Информация находится в файле"
		else:
			body = self.item['body']
		price = self.formated_price()
		category = self.item['category']
		position = self.item['position']
		return f"{line}\n<b>◻️ Категория:</b>{category}\n<b>◻️ Позиция:</b>{position}\n<b>◻️ Цена:</b>{price}\n{line}\n{body}"

	__guarded__ = ['created_at', 'updated_at']


class Item(Model):
	@belongs_to
	def position(self):
		return Position

	@scope
	def stocked(self,query):
		return query.where('buy', False)

	def check_file(self):
		if self.is_file == True:
			return True

	def jsn(self):
		is_file = self.is_file
		body = self.body
		price = self.position.price
		item_id = self.id
		position = self.position.name
		category = self.position.category.name
		dct = dict(is_file=is_file, body=body, price=price, position=position, category=category, item_id=item_id)
		jsn = json.dumps(dct)
		return jsn

	def page(self):
		return f"{line}\n<b>Категория:</b> {self.position.category.name}\n<b>Позиция:</b> {self.position.name}"
	__hidden__ = ['created_at', 'updated_at']
	__guarded__ = ['created_at', 'updated_at']


class Position(Model):

	@belongs_to
	def category(self):
		return Category

	@has_many
	def items(self):
		return Item.stocked()

	@scope
	def stocked(self, query):
		return query.has('items').get()		

	def formated_price(self):
		m = Money(self.price, 'RUB')
		frmt = m.format('ru_RU',currency_digits=False)
		return frmt

	def page(self):
		return f"{self.category.page()}\n<b>◻️ Позиция:</b> {self.name}\n<b>◻️ Описание позиции:</b> {self.description}\n<b>◻️ Цена:</b> {self.formated_price()}\n{line}"
	def info_page(self):
		return f"<b>◻️ Позиция:</b> {self.name}\n<b>◻️ Описание позиции:</b> {self.description}\n<b>◻️ Цена:</b> {self.formated_price()}\n<b>◻️ Категория:</b> {self.category.name}\n{line}"
	def buy_page(self):
		return f"{self.page()}\n<code>💬 Стоимость покупки составит:</code><b>{self.formated_price()}</b>\n<code>Подтверждаете заказ?</code>"

	def success_buy_page(self):
		return f"{self.page()}\n<code>💬 Успешно! {self.formated_price()} Списано с вашего кошелька. Перейдите в раздел 'Покупки` для информации о товаре.</code>"

	def can_paid(self,balance):
		amount =  int(balance) - int(self.price)
		if amount < 0:
			st = str(amount)
			stt = st.split("-")[1]
			m = Money(stt, 'RUB')
			frmt = m.format('ru_RU',currency_digits=False)
			return frmt
		else:
			return True


	__guarded__ = ['created_at', 'updated_at']



class Category(Model):

	@has_many
	def positions(self):
		return Position

	@has_many_through(Position)
	def items(self):
		return Item.stocked()

	@scope
	def stocked(self, query):
		return query.has('positions').get()

	def page(self):
		return f"{line}\n<b>◻️ Категория:</b> {self.name}\n<b>◻️ Описание:</b> {self.description}\n{line}"

	__guarded__ = ['created_at', 'updated_at']


class Token(Model):
	__guarded__ = ['created_at', 'updated_at']


class Page(Model):
	__guarded__ = ['created_at', 'updated_at']








