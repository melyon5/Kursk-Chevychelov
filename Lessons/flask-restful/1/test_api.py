import requests

BASE_URL = "http://127.0.0.1:5000/api/v2/users"

print(requests.get(BASE_URL).json())

payload = {
    "surname": "Ivanov",
    "name": "Ivan",
    "email": "ivanov@example.com",
    "password": "12345",
    "city_from": "Moscow"
}
resp = requests.post(BASE_URL, json=payload)
print(resp.json())
user_id = resp.json().get("user_id")

payload_missing = {
    "name": "Petrov",
    "email": "petrov@example.com",
    "password": "67890"
}
print(requests.post(BASE_URL, json=payload_missing).text)

if user_id:
    print(requests.get(f"{BASE_URL}/{user_id}").json())

print(requests.get(f"{BASE_URL}/999999").json())

if user_id:
    print(requests.delete(f"{BASE_URL}/{user_id}").json())

print(requests.delete(f"{BASE_URL}/999999").json())
