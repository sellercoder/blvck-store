import random
import json

from SimpleQIWI import *
# from data.config import QIWI_TOKEN, QIWI_PHONE
from time import sleep
from utils.db_api.admin_db_commands import get_token

tk = str(get_token().token)
ph = str(get_token().phone)

token = tk       
phone = ph

api = QApi(token=token, phone=phone)

def create_bill(price,prefix):
	number = random.randint(10000,50000)
	generate_comment = str(prefix) + '-' + str(number)
	bill = api.bill(price=price, comment=generate_comment)
	return f"{generate_comment}"

def get_payments():
	payments = api.payments['data']
	payments_dict = {}
	for payment in payments:
		comment = payment['comment']
		amount = payment['sum']['amount']
		new_dict = {comment:amount}
		payments_dict.update(new_dict)
	return payments_dict

def check_bill(comment):
	payments = get_payments()
	if comment in payments:
		return payments[comment]
	else:
		return False



		










