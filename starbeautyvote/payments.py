import requests
import json
from .custum import Starbeautyvote 
import os
from dotenv import load_dotenv
from decouple import config


load_dotenv()
api_key = config("API_PAYMENT_KEY")
private_key = config("PRIVATE_API_PAYMENT_KEY")
class Payments: 
    def __init__(self) -> None:
        pass
     
    
    def authentication() : 
        url = 'https://api.notchpay.co'
        headers = {
            'Authorization': api_key
        }

        response = requests.get(url, headers=headers)

        print(response.text)
        return response 
    
    
    def initialisePayment(amout) : 
        reference = Starbeautyvote.generate_random_string()
        url = 'https://api.notchpay.co/payments/initialize'
        headers = {
            'Authorization':api_key,
            'Accept': 'application/json'
        }
        data = {
            'email': 'bonombelleaurelien@outloo.com',
            'currency': 'XAF',
            'amount': f'{amout}',
            'phone': '697783493',
            'reference': reference,
            'description': 'StartBeautyVote Candidate Vote By Customer '
        }

        response = requests.post(url, headers=headers, data=data)

        
        response = response.json()
        return response , response["transaction"]["reference"]
    
    
    

    def completePayment(reference): 
        url = f'https://api.notchpay.co/payments/{reference}'
        headers = {
            'Authorization': api_key,
            'Accept': 'application/json', 
            'Content-Type': 'application/json'
        }
        data = {
            "channel": "cm.orange",
            "data" : {"phone": "237656019261"},
        }
        # Convertir les données en format JSON
        json_data = json.dumps(data)
        response = requests.post(url, headers=headers, data=json_data)
        
        return response
    
    
    
    def launchTransfert(reference , name = "John Doe", phone='+237656019261'): 
        url = 'https://api.notchpay.co/transfers'
        
        payload = {
            'currency': 'XAF',
            'amount': '1325',
            'channel': 'cm.mobile',
            'beneficiary':
                {
                    'number': '+237656019261', 
                    'name': f'{name}'
                }, 
            'reference': f'{reference}',
            'description': 'Account refund'
        }
        
        
        headers = {
            'Authorization': api_key,
            'Grant-Authorization': private_key,
            'Accept': 'application/json'
        }
        
        
        response = requests.post(url, json=payload, headers=headers)
        response = response.json()
        return response , response["status"] 


