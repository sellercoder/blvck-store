import os
import random
import xlsxwriter
from utils.db_api.models import *
from aiogram import types
from aiogram.types import InputFile

def payments_report(user_id):
	"""Формирует отчет по платежам пользователя"""

	# Создаем будущего файла 
	number = random.randint(10000,50000)
	user = User.find(user_id)
	payments = user.payments
	filename = f"{number}.xlsx"
	input_file = f"Отчет по платежам.xlsx"
	
	# Создаем обьект таблицы
	workbook = xlsxwriter.Workbook(filename)
	worksheet = workbook.add_worksheet()
	row = 0
	col = 0

    # Добавляем в таблицу названия колонок
	worksheet.write(row, 0, 'Сумма')
	worksheet.write(row, 1, 'Провайдер')
	worksheet.write(row, 2, 'Дата платежа')

	# Достаем из базы платежи и добавляем в таблицу
	for payment in payments:
		worksheet.write(row + 1, col, f"{payment.formated_amount()}")
		worksheet.write(row + 1, col + 1, f"{payment.provider}")
		worksheet.write(row + 1, col + 2, f"{payment.get_dt()}")
		row +=1

	workbook.close()

	# Формируем таблицу, удаляем временный файл.
	file = InputFile(filename, filename=input_file)
	os.remove(filename)

	return file


