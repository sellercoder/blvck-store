from environs import Env

env = Env()
env.read_env()

IP = env.str("IP")  

BOT_TOKEN = env.str("BOT_TOKEN") 
ADMINS = env.list("ADMINS")  
ADMIN_ID = env.list("ADMIN_ID")

POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD") 
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_DB = env.str("POSTGRES_DB")


DATABASES = {
    'postgres': {
        'driver': 'postgres',
        'host': IP,
        'database': POSTGRES_DB,
        'user': POSTGRES_USER,
        'password': POSTGRES_PASSWORD,
        'prefix': ''
    }
}

try:
	ABOUT_TEXT_TITLE = env.str("ABOUT_TEXT_TITLE")
except:
	ABOUT_TEXT_TITLE = "<code>💬 Это стандартное сообщение раздела 'О магазине'. Чтобы его изменить напишите текст в переменной ABOUT_TEXT_TITLE в файле .env и перезапустите контейнер</code>"

try:
    ABOUT_TEXT_BODY = env.str("ABOUT_TEXT_BODY")
except:
    ABOUT_TEXT_BODY = "<code>💬 Это стандартное сообщение раздела 'О магазине'. Чтобы его изменить напишите текст в переменной ABOUT_TEXT_BODY в файле .env и перезапустите контейнер</code>"

try:
	CATALOG_TEXT_TITLE = env.str("CATALOG_TEXT_TITLE")
except:
	CATALOG_TEXT_TITLE = "<code>💬 Это стандартное сообщение раздела 'Каталог'. Чтобы его изменить напишите текст в переменной CATALOG_TEXT_TITLE в файле .env и перезапустите контейнер</code>"	

try:
    CATALOG_TEXT_BODY = env.str("CATALOG_TEXT_BODY")
except:
    CATALOG_TEXT_BODY = "<code>💬 Это стандартное сообщение раздела 'Каталог'. Чтобы его изменить напишите текст в переменной CATALOG_TEXT_BODY в файле .env и перезапустите контейнер</code>" 

try:
    HELLO_TEXT_TITLE = env.str("HELLO_TEXT_TITLE")
except:
    HELLO_TEXT_TITLE = "<code>💬 Это стандартное сообщение на главной странице. Чтобы его изменить напишите текст в переменной HELLO_TEXT_TITLE в файле .env и перезапустите контейнер</code>" 

try:
    HELLO_TEXT_BODY = env.str("HELLO_TEXT_BODY")
except:
    HELLO_TEXT_BODY = "<code>💬 Это стандартное сообщение на главной странице. Чтобы его изменить напишите текст в переменной HELLO_TEXT_BODY в файле .env и перезапустите контейнер</code>" 








