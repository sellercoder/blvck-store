import random
import requests
import json
from utils.db_api.models import Bill

phone = "77779717706"

api_url = "https://api.qiwi.com/partner/bill/v1/bills/"

headers = {'Content-type': 'application/json','Accept': 'application/json',
'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6Ing0ejVjZC0wMCIsInVzZXJfaWQiOiI3Nzc3OTcxNzcwNiIsInNlY3JldCI6IjJhZWY5OGRkNWZhMjBiNmNkZWI0OTBiZjJkYjU0ZGIwNDg0ZTAyMTMzMmY4OTU3M2Y5M2U1N2YyNWQ5ZTAzZDMifX0='
}

status_headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6Ing0ejVjZC0wMCIsInVzZXJfaWQiOiI3Nzc3OTcxNzcwNiIsInNlY3JldCI6IjJhZWY5OGRkNWZhMjBiNmNkZWI0OTBiZjJkYjU0ZGIwNDg0ZTAyMTMzMmY4OTU3M2Y5M2U1N2YyNWQ5ZTAzZDMifX0='
}

def new_bill(value):
	rand = random.randint(10000000000,50000000000)
	url = f"{api_url}{rand}"
	payload = {  
	   "amount": {   
	     "currency": "KZT",   
	     "value": f"{value}" 
	   },  
	   "comment": "Оплата из бота",  
	   "expirationDateTime": "2025-12-10T09:02:00+03:00",  
	   "customer": {
	     "phone": f"{phone}",
	     "account": "67"
	   },
	     "customFields" : {
	     "paySourcesFilter": "qw,card",
	     "themeCode": "Venyamyn-ChZ7lmjPgmw",
	     "message_id": f"dd"}}

	r = requests.put(url, headers=headers, data=json.dumps(payload))
	json_data = json.loads(r.text)
	return json_data

def status_bill(bill_id):
	api_url = f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id}"
	r = requests.get(api_url, headers=headers)
	json_data = json.loads(r.text)
	return json_data







