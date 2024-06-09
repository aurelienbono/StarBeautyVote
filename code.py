import re

def is_valid_phone_number(phone_number):
    # Pattern pour les numéros valides
    pattern = re.compile(r'^\+237 6[5-9] \d{2} \d{2} \d{2} \d{2}$')
    
    # Remplacer les lettres par des chiffres fictifs pour le test
    phone_number = phone_number.replace('CD', '12').replace('EF', '34').replace('GH', '56').replace('D', '3').replace('B', '1')

    return bool(pattern.match(phone_number))

# Test des numéros de téléphone
phone_numbers = [
    "+237 6 55 CD EF GH",
    "+237 6 56 CD EF GH",
    "+237 6 57 CD EF GH",
    "+237 6 58 CD EF GH",
    "+237 6 59 0 D EF GH",
    "+237 6 59 1 D EF GH",
    "+237 6 59 2 D EF GH",
    "+237 6 59 3 D EF GH",
    "+237 6 59 4 D EF GH",
    "+237 6 59 5 D EF GH",
    "+237 6 9B CD EF GH"
]

for number in phone_numbers:
    print(f"{number}: {is_valid_phone_number(number)}")
