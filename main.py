import requests

response = requests.get('https://coinmarketcap.com/ru/')

print(response.headers)
