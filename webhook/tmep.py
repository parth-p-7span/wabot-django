import requests

url = "https://graph.facebook.com/v13.0/106519662119427/media"

payload = {
    'messaging_product': 'whatsapp'
}

files = [
    ('file', ('json2dart.jpg', open('/home/parthpanchal/Pictures/json2dart.jpg', 'rb'), 'image/jpeg'))
]
headers = {
    'Authorization': 'Bearer EABMCARdnUF8BACps2sgDEVxR3BYl42YpnkllxNbq2N7iCk2ZCo0U0TY3KnZBYCHYMOu3vhZCGwqj7e4vndmqpyuvZCxWc1voUoBqOW8O3k4vRvZB63e59vD5guX1EFZAU6Ddy8yxnDaXF9lq6Emiqknl0hVEooZAZCOeIF2rYytXASs9TQSnPnHCDKRUHvG57eZA94TrfnOVFF6x35Bwvi8Ur'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
