import requests 

url = "http://0.0.0.0:8000/user" 

response = requests.get(url) 

print(response.json()) 