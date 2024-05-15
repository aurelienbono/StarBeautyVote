import requests
import secrets


api_key = "pk_test.IKq08Kk8qF6hPviQikHy8Mgpn3cxz8mWwhSkyCw0djMVRdj0dVdwiRYvcIvIlllTlQd2c03Lb4MWMldEBtfZyh6JeqNwmH6r96WB1VCiuNUrXaX2Opb6PSXq00AX8"

def generate_random_string(length=16):
        """
        Generates a random alphanumeric string of specified length.

        Args:
            length (int, optional): The desired length of the random string. Defaults to 10.

        Returns:
            str: A random alphanumeric string.
        """
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(secrets.choice(chars) for _ in range(length))


class Payments: 
    def __init__(self) -> None:
        pass
    
    
    def authentication() : 
        url = 'https://api.notchpay.co'
        headers = {
            'Authorization': api_key
        }

        response = requests.get(url, headers=headers)

        return response 
    
    
    # def initialisePayment(amount, phone) : 
    def initialisePayment(amount) : 

        reference = generate_random_string()
        url = 'https://api.notchpay.co/payments/initialize'
        headers = {
            'Authorization':api_key,
            'Accept': 'application/json'
        }
        data = {
            'email': 'bonombelleaurelien@outlook.com',
            'currency': 'XAF',
            'amount': f"{amount}",
            'phone': '697783493',
            'reference': reference,
            'description': 'Candidate Vote Election'
        }

        response = requests.post(url, headers=headers, data=data)
        
        response = response.json()
        return response , response["transaction"]["reference"]
    
    
    
    def completePayment(reference=0, phone=0): 
        url = 'https://api.notchpay.co/payments/trx.test_jhO8CPcJIbT7pJqSgVSlG8Zl'
        headers = {
            'Authorization':api_key,
            'Accept': 'application/json', 
            'Content-Type': 'application/json'
        }
        data = {
            "channel": "cm.orange",
            "data" : {
            # "phone": f"{phone}" for production 
            "phone": "237656019261" #for sandbox
        },
        }
        response = requests.post(url, headers=headers, data=data)
        
        return response
        


# pays = Payments()
# pays.completePayment()