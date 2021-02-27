from utils.misc.logging import *
from data.config import *
from aiogram import types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states.admin import NewCoupon, DeleteCoupon
from keyboards.admin.admin_menu import admin_menu
from keyboards.admin.users_menu import users_menu, coupons_menu, coupon_confirm_menu
from utils.db_api.admin_db_commands import admin_text, summary, create_coupon, get_users_info, coupons_page
from utils.db_api.db_commands import find_user
from utils.db_api.models import User, Payment, Purchase, Coupon

from loader import dp, bot

line = "➖"*11
info = "💬"
users_text = "<b>Управление юзерами</b>"

@dp.message_handler(user_id=ADMIN_ID, text_contains="info", state="*")
async def user_info(message: types.Message, state: FSMContext):
	string = message.text.split("_")[1]
	user_uid = str(string)
	user = find_user(user_uid)
	await message.answer(text=f"{user.full_info()}")


@dp.message_handler(user_id=ADMIN_ID, text="▫️ Юзеры", state="*")
async def admin_users_page(message: types.Message, state: FSMContext):
	logger.info(f"{message.chat.first_name}-{message.text}")
	text = f"{users_text}\n{get_users_info()}\n" 
	await message.answer(text=text, reply_markup=users_menu)

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="coupons", state="*")
async def admin_coupons_page(call: CallbackQuery,state: FSMContext):
	await call.message.edit_text(text=f"Купоны\n{coupons_page()}", reply_markup=coupons_menu)

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="add_coupon", state="*")
async def admin_add_coupon_page(call: CallbackQuery,state: FSMContext):
	await call.message.edit_text(f"{info}")
	await call.message.answer(text=f"<code>{info} Пришли мне уникальное название купона. Это название нужно знать юзеру, чтобы его активировать.</code>", reply_markup=ReplyKeyboardRemove())
	await NewCoupon.Uid.set()

@dp.message_handler(user_id=ADMIN_ID, state=NewCoupon.Uid)
async def admin_add_coupon_uid_page(message: types.Message, state: FSMContext):
	coupon = Coupon()
	coupon.uid = message.text
	await message.answer(f"<code>{info}Теперь пришли мне сумму купона</code>")
	await NewCoupon.Amount.set()
	await state.update_data(coupon=coupon)

@dp.message_handler(user_id=ADMIN_ID, regexp=r"^(\d+)$", state=NewCoupon.Amount)
async def admin_add_coupon_uid_page(message: types.Message, state: FSMContext):
	data = await state.get_data()
	coupon: Coupon = data.get("coupon")
	coupon.amount = message.text
	await message.answer(f"<b>Сумма купона:</b> {coupon.formated_amount()}\n<b>Идентификатор:</b>\n <code>{coupon.uid}</code>\n\n<code>{info}Все верно?</code>", reply_markup=coupon_confirm_menu)
	await NewCoupon.Confirm.set()
	await state.update_data(coupon=coupon)

@dp.message_handler(user_id=ADMIN_ID, state=NewCoupon.Amount)
async def not_amount(message: types.Message, state: FSMContext):
    await message.answer(f"<code>{info} Сумму нужно писать цифрой 😀</code>")

@dp.callback_query_handler(user_id=ADMIN_ID, state=NewCoupon.Confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
	if call.data == "cancel":
		cancel_text = f"<code>{info} Создание купона отменено</code>"
		await call.message.edit_text(cancel_text)
	else:
		try:
			data = await state.get_data()
			coupon: Coupon = data.get("coupon")
			coupon.save()
			success_text = f"<code>{info} Купон: <b>{coupon.uid}</b> успешно создан!</code>"
			await call.message.edit_text(success_text)
		except:
			await call.message.edit_text("Что-то пошло не так... Жми /admin")

	await call.answer(cache_time=1)
	summary_text = summary()
	text = admin_text(summary_text)
	await call.message.answer(text=text, reply_markup=admin_menu)
	await state.reset_state()

@dp.message_handler(user_id=ADMIN_ID, state=NewCoupon.Confirm)
async def not_confirm(message: types.Message, state: FSMContext):
	await message.answer(text=f"<code>{info} Вообще-то я спросил верно или нет... 👆</code>")


@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="delete_coupon", state="*")
async def admin_delete_coupon_page(call: CallbackQuery,state: FSMContext):
	await call.message.edit_text(f"{info}")
	await call.message.answer(text=f"<code>{info} Пришли мне ID купона для удаления</code>", reply_markup=ReplyKeyboardRemove())
	await DeleteCoupon.Id.set()

@dp.message_handler(user_id=ADMIN_ID, regexp=r"^(\d+)$", state=DeleteCoupon.Id)
async def admin_delete_coupon_uid_page(message: types.Message, state: FSMContext):
	coupon_id = message.text
	coupon = Coupon.find(coupon_id)
	coupon.delete()
	await message.answer(text=f"<code>{info} Купон удален. Нажми</code> /admin <code> для выхода в меню</code>")
	await state.reset_state()

@dp.message_handler(user_id=ADMIN_ID, state=DeleteCoupon.Id)
async def not_confirm(message: types.Message, state: FSMContext):
	await message.answer(text=f"<code>{info} Нужен id...</code>")











































