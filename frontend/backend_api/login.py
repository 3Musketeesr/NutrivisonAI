import requests
url = "http://0.0.0.0:8000/user/login" 



data = {
    "username":"testuser", 
    "email":"testuser@gmail.com",
    "password":"asjdfkjasldfjs", 
}


response = requests.post(url=url,json=data,headers={"Content-Type":"application/json"})

print(response.json()) 