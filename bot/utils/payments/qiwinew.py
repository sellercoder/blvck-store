import random
import requests
import json
from utils.db_api.models import Bill

phone = "79510131989"

api_url = "https://api.qiwi.com/partner/bill/v1/bills/"

headers = {'Content-type': 'application/json','Accept': 'application/json',
'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InRpZWF3eC0wMCIsInVzZXJfaWQiOiI3OTUxMDEzMTk4OSIsInNlY3JldCI6ImJjMzczYWJhZjEyZGY3YWE1NjA1MjY5MjQ0N2FlYmZjNmJlZTU4ZDAzMWFlM2QyYTMyMjlkNTVhMzEzNWJlODIifX0='
}

status_headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InRpZWF3eC0wMCIsInVzZXJfaWQiOiI3OTUxMDEzMTk4OSIsInNlY3JldCI6ImJjMzczYWJhZjEyZGY3YWE1NjA1MjY5MjQ0N2FlYmZjNmJlZTU4ZDAzMWFlM2QyYTMyMjlkNTVhMzEzNWJlODIifX0='
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







