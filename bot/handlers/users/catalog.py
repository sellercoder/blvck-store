from utils.misc.logging import *
from data.config import *
from utils.texts import *
from typing import Union
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from keyboards.inline.catalog_menu import menu_cd, categories_keyboard, positions_keyboard, position_keyboard, buy_position_keyboard, add_money_keyboard
from utils.db_api.db_commands import get_category, get_position, get_user, buy_item, find_user
from utils.db_api.models import Position, User
from loader import dp

#` Текст на странице каталог                                                             
catalog_page_text = f"{catalog_text}\n\n{catalog_text_body()}\n\n<code>💬 Выберите категорию</code>"

#` Хендлер для 🗃 Каталог                                                                
@dp.message_handler(Text(equals=["🗃 Каталог"]))
async def show_menu(message: Message):
    await list_categories(message)

#` LEVEL 0
#` Функция отдающая категории                                                            
async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    markup = categories_keyboard()
    #` Проверяем тип апдейта.           
    #- Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer(catalog_page_text, reply_markup=markup)
    #` Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await message.message.edit_text(catalog_page_text, reply_markup=markup)

#` LEVEL 1
#` Функция отдающая позиции из выбраной категории                                        
async def list_positions(callback: CallbackQuery, category, **kwargs):
    #` Проверяем наличие позиций в категории               
    try:
    #- Если, есть - отдаем клавиатуру с названиями позиций 
    #- и меняем текст с информацие о категории             
        markup = positions_keyboard(category) #` Клавиатура с позициями          
        cat = get_category(category)          #` Находим категорию в базе        
        page = f"{cat.page()}"                #` Достаем информацию о категории  
        #` Меняем и отдаем сообщение                                             
        await callback.message.edit_text(text=page,reply_markup=markup)              
    except:
    #` Если нет, пишем текст, и снова отправляем клавиатуру 
    #- с названиями категорий                               
        markup = categories_keyboard()        #` Клавиатура с категориями        
        cat = get_category(category)          #` Находим категорию в базе        
        #` Меняем и отдаем сообщение                                             
        await callback.message.edit_text(
            text=f"<code>Админ - мудак и забыл загрузить товары\nв категорию {cat.name}\nПните его по адресу в разделе 'О магазине' или полистайте другие категории.</code>", reply_markup=markup)

#` LEVEL 2
#` Функция отдающая информацию о позиции                                           
async def show_position(callback: CallbackQuery, category, position, user, **kwargs):
    markup = position_keyboard(position, user) #` Формируем клавиатуру для позиции
    pos = get_position(position)               #` Достаем позицию из базы         
    page = f"{pos.page()}"                     #` Достаем информацию о позции     
    #` Меняем и отдаем сообщение                                                  
    await callback.message.edit_text(text=page, reply_markup=markup)


#` LEVEL 3
#` Функция проверяющая баланс пользователя и отдающая на основе результата либо         
#` информацию о товаре,который хочет купить юзер и кнопки с отмены/подтверждения,       
#` либо информацию о недостаточной сумме для покупки и кнопкой 'назад'                  
async def buy_position(callback: CallbackQuery, category, position, user, **kwargs):
    current_user = get_user(user)              #` Достаем из базы юзера по id из колбэка
    current_position = get_position(position)  #` Достаем позицию из базы               

    #` Проверяем на возможность покупки товара из текущей позиции                        
    can_paid = current_position.can_paid(current_user.balance)

    if can_paid == True:
    #` Если все хорошо:                             
        #` Формируем клавиатуру, для позиции  c кнопками 'Подтвердить' и 'Отмена'
        markup = buy_position_keyboard(position, user)
        #` Меняем и отправляем сообщение                                        
        await callback.message.edit_text(text=f"{current_position.buy_page()}", reply_markup=markup) 
    else:
    #` В случае если средств на балансе не хватает: 
        #` Формируем клавиатуру, c кнопкой 'Назад'                               
        markup = add_money_keyboard(position)
        #` Формируем сообщение с информацией о сумме недостаточной для покупки  
        page = f"{current_position.page()}\n<code>💬 Для покупки этого товара, вам не хватает {can_paid}.\nПополните баланс или выберите другой товар.</code>"
        #` Меняем и отправляем сообщение                                        
        await callback.message.edit_text(text=page, reply_markup=markup)

#` LEVEL 4
#` Функция отдающая текст об успешной покупке.                                           
async def success_purchase(callback: CallbackQuery, category, position, user, **kwargs):
    current_user = find_user(user).id                #` Достаем юзера из базы            
    current_position = Position.find(position)       #` Достаем позицию из бызы          
    current_item = current_position.items.first().id #` Достаем последний товар в позиции
    buy_item(current_item, current_user)             #` Применяем функцию покупки товара 
    #` Меняем и отправляем сообщение                                        
    await callback.message.edit_text(text=f"{current_position.success_buy_page()}")


#` Функция, которая обрабатывает ВСЕ нажатия на кнопки в этом меню                       
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    #` Получаем текущий уровень меню, который запросил пользователь              
    current_level = callback_data.get("level")

    #` Получаем категорию, которую выбрал пользователь                            
    category = callback_data.get("category")

    #` Получаем позицию, которую выбрал пользователь                              
    position = callback_data.get("position")

    #` Получаем текущего юзера(Передается НЕ ВСЕГДА - может быть 0)               
    user = call.message.chat.id

    #` Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": list_categories,  
        "1": list_positions,
        "2": show_position,
        "3": buy_position,
        "4": success_purchase
    }

    #` Забираем нужную функцию для выбранного уровня      
    current_level_function = levels[current_level]

    #` Показываем в логе callback_data                   
    logger.info(f"callback_data='{callback_data}'")

    #` Обрабатываем коллбэк                              
    await call.answer(cache_time=1)

    #` Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        category=category,
        position=position,
        user = user
    )






