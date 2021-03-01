from utils.misc.logging import *
from typing import Union
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery, Document
from keyboards.inline.purchases_menu import pr_menu_cd, purchases_keyboard
from utils.db_api.models import User, Purchase 
from loader import dp

purchases_page_text = f"<b>🛒 Покупки</b>\n\n<code>💬 Здесь находится список всех ваших покупок. Выберите нужную для подробной информации.</code>"

#` Хендлер для 📕 О магазине                                                             
@dp.message_handler(Text(equals=["📂 Покупки"]))
async def show_menu(message: Message):
	await list_purchases(message)

async def list_purchases(message: Union[CallbackQuery, Message], **kwargs):
	user = message.chat.id
	markup = purchases_keyboard(user)
	if isinstance(message, Message):
		await message.answer(purchases_page_text, reply_markup=markup)
	elif isinstance(message, CallbackQuery):
		call = message
		await message.message.edit_text(purchases_page_text, reply_markup=markup)

async def show_purchase(callback: CallbackQuery, user, purchase, **kwargs):
    purchase = Purchase.find(purchase)
    text = f"{purchase.page()}" 
    # html_file = open('test.txt', 'rb')
    if purchase.is_file == True:
        html_file = purchase.item['body']
        await callback.answer(cache_time=1)
        await callback.message.answer_document(document=html_file,caption=text, disable_content_type_detection=True)
    else:
        await callback.message.answer(text)

@dp.callback_query_handler(pr_menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    #` Получаем текущий уровень меню, который запросил пользователь              
    current_level = callback_data.get("level")

    purchase = callback_data.get("purchase")

    #` Получаем текущего юзера        
    user = call.message.chat.id

    #` Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": list_purchases,  
        "1": show_purchase
    }

    #` Забираем нужную функцию для выбранного уровня      
    current_level_function = levels[current_level]

    #` Показываем в логе callback_data                   
    logging.info(f"callback_data='{callback_data}'")

    #` Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        user = user,
        purchase = purchase
    )

