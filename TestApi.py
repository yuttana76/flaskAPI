import requests
URL="http://127.0.0.1:5000/weather"
response = requests.get(URL)
print(response.json())