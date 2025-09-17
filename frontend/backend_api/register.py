import requests
url = "http://0.0.0.0:8000/user/signup" 


data = {
    "username":"lewisnjue", 
    "email":"lewisnjue@gmail.com",
    "password":"adfu2asdfajfoasdf", 
}

response = requests.post(url=url,json=data)

print(response.json()) 