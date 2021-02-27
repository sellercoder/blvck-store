curl --location --request PUT 'https://api.qiwi.com/partner/bill/v1/bills/cc961e8d-d4d6-4f02-b737-2297e51fb48e75757' \
--header 'content-type: application/json' \
--header 'accept: application/json' \
--header 'Authorization: Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InRpZWF3eC0wMCIsInVzZXJfaWQiOiI3OTUxMDEzMTk4OSIsInNlY3JldCI6ImJjMzczYWJhZjEyZGY3YWE1NjA1MjY5MjQ0N2FlYmZjNmJlZTU4ZDAzMWFlM2QyYTMyMjlkNTVhMzEzNWJlODIifX0=' \
--data-raw '{  
   "amount": {   
     "currency": "RUB",   
     "value": "1.00" 
   },  
   "comment": "Text comment",  
   "expirationDateTime": "2025-12-10T09:02:00+03:00",  
   "customer": {
     "phone": "78710009999",
     "email": "test@tester.com",
     "account": "454678"
   }, 
   "customFields" : {
     "paySourcesFilter":"qw",
     "themeCode": "Yvan-YKaSh",
     "yourParam1": "64728940",
     "yourParam2": "order 678"
   }
 }'