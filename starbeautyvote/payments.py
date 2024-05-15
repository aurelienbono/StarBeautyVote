import requests
import json
from .custum import Starbeautyvote 
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("API_PAYMENT_KEY")

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
        print(reference)
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

        print(response.json())
        
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

        print(response.json())
        
        return response


