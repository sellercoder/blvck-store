# alert = "❕"
# line = "➖"*11
info = "💬"
from utils.db_api.models import Page

hello_text = f"<b>🏪️AutoShop ᗷᒪᐺᑢᖽᐸ°•ᖇᗩᗷᗷᓰᖶ</b>"

def hello_text_body():
	try:
		return Page.where('types', 'hello').first().body
	except:
		return f"{info} Отредактируй меня"

catalog_text = f"<b>🗃 Каталог товаров</b>"

def catalog_text_body():
	try:
		return Page.where('types', 'catalog').first().body
	except:
		return f"{info} Отредактируй меня"

about_text = f"<b>📕 О магазине</b>"

def about_text_body(): 
	try:
		return Page.where('types', 'about').first().body
	except:
		return f"{info} Отредактируй меня"






