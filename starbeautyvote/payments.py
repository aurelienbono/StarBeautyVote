import requests
import secrets


api_key = "pk_test.IKq08Kk8qF6hPviQikHy8Mgpn3cxz8mWwhSkyCw0djMVRdj0dVdwiRYvcIvIlllTlQd2c03Lb4MWMldEBtfZyh6JeqNwmH6r96WB1VCiuNUrXaX2Opb6PSXq00AX8"

class Payments: 
    def __init__(self) -> None:
        pass
    
    def generate_random_string(self,length=16):
        """
        Generates a random alphanumeric string of specified length.

        Args:
            length (int, optional): The desired length of the random string. Defaults to 10.

        Returns:
            str: A random alphanumeric string.
        """
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    
    def authentication(self) : 
        url = 'https://api.notchpay.co'
        headers = {
            'Authorization': api_key
        }

        response = requests.get(url, headers=headers)

        print(response.text)
        return response 
    
    
    def initialisePayment(self) : 
        reference = self.generate_random_string()
        url = 'https://api.notchpay.co/payments/initialize'
        headers = {
            'Authorization':api_key,
            'Accept': 'application/json'
        }
        data = {
            'email': 'bonombelleaurelien@outloo.com',
            'currency': 'XAF',
            'amount': '20000',
            'phone': '697783493',
            'reference': reference,
            'description': 'Payment description'
        }

        response = requests.post(url, headers=headers, data=data)

        print(response.json())
        
        response = response.json()
        return response , response["transaction"]["reference"]
    
    
    
    def completePayment(self): 
        url = 'https://api.notchpay.co/payments/trx.test_QIjvmGd3TbP0rrO3kOHv5I9t'
        headers = {
            'Authorization':api_key,
            # 'Accept': 'application/json', 
            'content-type': 'application/json'
        }
        data = {
            "channel": "cm.orange",
            "data" : {
            "phone": "+237697783493"
        }
        }
        response = requests.post(url, headers=headers, data=data)

        print(response.json())
        
        return response
        


pays = Payments()
# _, reference = pays.initialisePayment()
pays.completePayment()