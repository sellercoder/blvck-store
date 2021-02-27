import random
import requests
import json
# PUT
rand = random.randint(10000000000,50000000000)
api_url = f"https://api.qiwi.com/partner/bill/v1/bills/{rand}"

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InRpZWF3eC0wMCIsInVzZXJfaWQiOiI3OTUxMDEzMTk4OSIsInNlY3JldCI6ImJjMzczYWJhZjEyZGY3YWE1NjA1MjY5MjQ0N2FlYmZjNmJlZTU4ZDAzMWFlM2QyYTMyMjlkNTVhMzEzNWJlODIifX0='
}

payload = {  
   "amount": {   
     "currency": "KZT",   
     "value": "10.00" 
   },  
   "comment": "Привет дорогой!",  
   "expirationDateTime": "2025-12-10T09:02:00+03:00",  
   "customer": {
     "phone": "79510131989",
     "email": "veniamin4e@gmail.com",
     "account": "454686",
   },
     "customFields" : {
     "paySourcesFilter": "qw",
     "themeCode": "Venyamyn-ChZ7lmjPgmw",
      "yourParam1": "or",
       "yourParam2": "jh"
   }
 }

r = requests.put(api_url, headers=headers, data=json.dumps(payload))
print(r.text)

# 48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPxePbvx8t45TgAv2wRR6mVKv7F1DkxE4F8seTWwN4WWLTfvYaVsJBhehbYbuahr3MhdNFL5bpksWm5y4PqtBLucxfsJg1MSY8vfsSVS6KK
