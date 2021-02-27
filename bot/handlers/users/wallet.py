import time
from data.config import ADMIN_ID
from utils.tools.tables import payments_report
from utils.misc.logging import *
from money import Money
from aiogram.dispatcher import FSMContext
from states.admin import ActivateCoupon
from aiogram.dispatcher.filters import Command, Text
from aiogram import types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.inline.wallet_menu import wallet_keyboard, check_qiwi_pay_keyboard
from utils.db_api.models import User
from utils.db_api.db_commands import find_user, add_money, check_success_payment, add_payment, activate_coupon
from utils.payments.qiwi import phone, create_bill, check_bill, get_payments

from loader import dp, bot

line = "➖"*11
info = "💬"
wallet_page_text = f"<b>💳 Кошелек</b>\n\n"
wallet_page_info_text = f"<code>💬 Для пополнения, выберите способ: </code>"

def wallet_bill_text(comment):
	return f"{line}\n<b>◻️ Cпособ пополнения:</b> 🥝 Qiwi\n<b>◻️ Комментарий:</b> {comment}\n<b>◻️ Телефон:</b> {phone}\n{line}\n<code>💬 Переведите на указанный номер необходимую сумму. Обязательно укажите комментарий! После перевода, нажмите кнопку Проверить оплату.</code>"

def succes_payment_message(amount):
	m = Money(amount, 'RUB')
	frmt = m.format('ru_RU',currency_digits=False)	
	return f"Платеж на сумму {frmt} обнаружен. {frmt} зачислены на ваш кошелек"


#` Хендлер для 💳 Кошелек                                                             
@dp.message_handler(Text(equals=["💳 Кошелек"]))
async def menu(message: Message):
	user_uid = message.chat.id
	user = find_user(user_uid)
	user_page = user.wallet_info()
	text = f"{wallet_page_text + user_page}\n\n{wallet_page_info_text}"
	markup = wallet_keyboard()

	await message.answer(text, reply_markup=markup)

@dp.callback_query_handler(text_contains="qiwi")
async def bill(call: CallbackQuery):
	user_uid = call.message.chat.id
	user = find_user(user_uid)
	comment = create_bill(1,"tg")
	text = wallet_bill_text(comment)
	markup = check_qiwi_pay_keyboard(comment)
	await call.answer(cache_time=1)
	await call.message.answer(text, reply_markup=markup)

@dp.callback_query_handler(text_contains="check")
async def check(call: CallbackQuery):
	comment = call.data.split(':')[1]
	logger.info(f"Проверка платежа {comment}")
	if check_bill(comment):
		logger.info(f"Платеж обнаружен")
		if check_success_payment(comment) == True:
			text = "Такой платеж уже есть, деньги по нему уже начислены"
			logger.info(f"{text}")
			await call.answer(cache_time=1,text=text,show_alert=True)
		else:
			user_uid = call.message.chat.id
			user = find_user(user_uid)
			user_id = user.id
			amount = check_bill(comment)
			add_payment(user_id,comment,amount)
			add_money(user_id,amount)
			text = succes_payment_message(amount)
			await call.answer(cache_time=1, text=text)
			await call.message.edit_text(text)
			# await bot.send_message()
			# await call.message.answer(text)
			for admin in ADMIN_ID:
				await bot.send_message(chat_id=admin,text=f"{user.name} оплатил {amount} на киви!")
	else:
		text="Платеж в системе не обнаружен!"
		logger.info(f"{text}")
		await call.answer(cache_time=1, text=text, show_alert=True)


@dp.callback_query_handler(text_contains="coupon")
async def input_coupon_uid(call: CallbackQuery):
	title = f"{info}\n"
	info_text = f"<code>Введите идентификатор купона</code>"
	await call.answer(cache_time=1)
	await call.message.edit_text(text=title)
	await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
	await ActivateCoupon.Uid.set()


@dp.message_handler(state=ActivateCoupon.Uid)
async def input_coupon_uid_handler(message: types.Message, state: FSMContext):
	logger.info(f"Введен купон - {message.text} - {message.chat.id}")
	user = find_user(message.chat.id)
	coupon_uid = message.text
	text = activate_coupon(coupon_uid, user.id)
	await message.answer(text=f"{info}<code>{text} Для выхода в меню, нажмите</code> <b>/start</b>")
	await state.reset_state()

@dp.callback_query_handler(text_contains="history")
async def payment_history(call: CallbackQuery):
	user = find_user(call.message.chat.id)
	info_text = f"<code>{info} Формирую отчет... </code>"
	success_text = f"<code>{info} Отчет готов... Отправляю...</code>"
	file = payments_report(user.id)
	await call.answer(cache_time=1)
	await call.message.edit_text(text=info_text)
	time.sleep(1)
	await bot.send_chat_action(chat_id=call.message.chat.id, action="upload_document")
	await call.message.edit_text(text=success_text)
	time.sleep(1)
	await call.message.answer_document(document=file, disable_content_type_detection=True)


















