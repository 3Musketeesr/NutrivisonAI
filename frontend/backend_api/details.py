import requests
url = "http://0.0.0.0:8000/user/{page}"


data = {
    "username":"testuser", 
    "email":"testuser@gmail.com",
    "password":"asjdfkjasldfjs", 
}


response = requests.post(url=url.format(page='login'),json=data,headers={"Content-Type":"application/json"})

token = response.json().get("access_token")

if not token:
    print("Could not get token")
    exit(1)

headers = {

    "Authorization": f"Bearer {token}"
}

response = requests.get(url=url.format(page='details'),headers=headers)

print(response.json()) 