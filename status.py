import random
import requests
import json
# PUT
api_url = f"https://api.qiwi.com/partner/bill/v1/bills/12777321377 "
headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InRpZWF3eC0wMCIsInVzZXJfaWQiOiI3OTUxMDEzMTk4OSIsInNlY3JldCI6ImJjMzczYWJhZjEyZGY3YWE1NjA1MjY5MjQ0N2FlYmZjNmJlZTU4ZDAzMWFlM2QyYTMyMjlkNTVhMzEzNWJlODIifX0='
}

r = requests.get(api_url, headers=headers)
print(r.text)

