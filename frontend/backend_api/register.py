import requests
url = "http://127.0.0.1:8000/user/signup"

data = {
    "username":"testuser", 
    "email":"testuser@gmail.com",
    "password":"asjdfkjasldfjs", 
}

response = requests.post(url=url,json=data)

print(response.json()) 