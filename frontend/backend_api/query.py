import requests


BASE_URL = "http://0.0.0.0:8000"


def login(username: str, password: str) -> str | None:
    url = f"{BASE_URL}/user/login"
    data = {
        "username": username,
        "password": password,
    }
    resp = requests.post(url, json=data, headers={"Content-Type": "application/json"})
    if resp.status_code != 200:
        print("Login failed:", resp.status_code, resp.text)
        return None
    return resp.json().get("access_token")


def query_backend(message: str, token: str):
    url = f"{BASE_URL}/user/query"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"message": message}
    resp = requests.post(url, json=payload, headers=headers)
    try:
        print(resp.status_code, resp.json())
    except Exception:
        print(resp.status_code, resp.text)


if __name__ == "__main__":
    # Update to match an existing user or run register.py first
    username = "testuser"
    password = "asjdfkjasldfjs"
    token = login(username, password)
    if not token:
        exit(1)
    query_backend("i was born in 2003 june 30th day save this data for me and am 5 meters long , also at this time am having ugali save this data for me ", token)


