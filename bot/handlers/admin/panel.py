from utils.misc.logging import *
from data.config import *
from aiogram import types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputFile
from aiogram.dispatcher import FSMContext
from states.admin import SetToken
from keyboards.admin.admin_menu import admin_menu, admin_wallet_menu
from utils.db_api.admin_db_commands import summary, admin_text, get_token
from utils.db_api.models import Token

from loader import dp, bot

line = "➖"*11
info = "💬"

#` Ловим команду /admin при условии, что отправитель есть в ADMIN_ID

@dp.message_handler(user_id=ADMIN_ID, commands=["admin"], state="*")
async def admin_start(message: types.Message, state: FSMContext):
    summary_text = summary()
    text = admin_text(summary_text)
    await message.answer(text=text, reply_markup=admin_menu)
    await state.reset_state()
    logger.info(f"{message.chat.id} нажал /admin")


@dp.message_handler(user_id=ADMIN_ID, text="▫️Главное меню", state="*")
async def admin_page(message: types.Message, state: FSMContext):
    summary_text = summary()
    text = admin_text(summary_text)
    await message.answer(text=text, reply_markup=admin_menu)
    await state.reset_state()
    logger.info(f"{message.chat.id} Выбрал главное меню в админке")

@dp.message_handler(user_id=ADMIN_ID, text="▫️Платежка", state="*")
async def wallet_page(message: types.Message, state: FSMContext):
    token_obj = get_token()
    token = token_obj.token
    phone = token_obj.phone
    text = f"<b>Здесь можно изменить токен Qiwi</b>\n\nТекущий токен:\n<code>{token}</code>\nТелефон: <code>{phone}</code>"
    await message.answer(text=text, reply_markup=admin_wallet_menu)

@dp.callback_query_handler(user_id=ADMIN_ID, text_contains="change_token", state="*")
async def admin_edit_qiwi_page(call: CallbackQuery,state: FSMContext):
    title = f"{info}\n"
    info_text = f"<b>Пришли токен киви. Для отмены жми</b> /admin"
    await call.message.edit_text(text=title)
    await call.message.answer(text=info_text, reply_markup=ReplyKeyboardRemove())
    await SetToken.set_token.set()

@dp.message_handler(user_id=ADMIN_ID, state=SetToken.set_token)
async def sned_text(message: types.Message, state: FSMContext):
    token = Token.first()
    token.token = message.text
    await state.update_data(token=token)
    await SetToken.set_phone.set()
    info_text = f"<b>Теперь мне нужен телефон от токена в формате +799... </b>"
    await message.answer(text=info_text)

@dp.message_handler(user_id=ADMIN_ID, state=SetToken.set_phone)
async def sned_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    token: Token = data.get("token")
    token.phone = message.text
    token.update()
    await state.reset_state()
    info_text = f"<b>Токен изменен! Жми /admin</b>"
    await message.answer(text=info_text)

