import requests
import json
import os
from dotenv import load_dotenv

url = 'https://api.notchpay.co/transfers'
public_key = 'pk_test.IKq08Kk8qF6hPviQikHy8Mgpn3cxz8mWwhSkyCw0djMVRdj0dVdwiRYvcIvIlllTlQd2c03Lb4MWMldEBtfZyh6JeqNwmH6r96WB1VCiuNUrXaX2Opb6PSXq00AX8'
private_key = 'sk_test.tQsnaDNsyfcABFf30Gxj9BjS442ooSAI1DHdkcAxKU5VVjeHAzh65kw5lInnAduKs4HuRBYYtKmhWM37cF9v8wcn156GfP6dpTLQ3sEOTbtywR6tJx6eGWqmFBT2r'



payload = {
    'currency': 'XAF',
    'amount': '1325',
    'channel': 'cm.mobile',
    'beneficiary':
        {
            'number': '+237656019261', 
            'name': 'John Doe'
        }
    ,
    'reference': 'asasasecfassaqnwsfc',
    'description': 'Account refund'
}

headers = {
    'Authorization': public_key,
    'Grant-Authorization': private_key,
    'Accept': 'application/json'
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

print(response.json())