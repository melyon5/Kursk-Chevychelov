import requests

USERS_URL = "http://127.0.0.1:5000/api/v2/users"
JOBS_URL = "http://127.0.0.1:5000/api/v2/jobs"

print(requests.get(USERS_URL).json())
print(requests.get(JOBS_URL).json())

user_payload = {
    "surname": "Ivanov",
    "name": "Ivan",
    "email": "ivanov@example.com",
    "password": "12345",
    "city_from": "Moscow"
}
user_resp = requests.post(USERS_URL, json=user_payload)
print(user_resp.json())
user_id = user_resp.json().get("user_id")

job_payload = {
    "job_title": "Test Job",
    "work_size": 10,
    "collaborators": "2,3",
    "is_finished": False,
    "team_leader": 1
}
job_resp = requests.post(JOBS_URL, json=job_payload)
print(job_resp.json())
job_id = job_resp.json().get("job_id")

if user_id:
    print(requests.get(f"{USERS_URL}/{user_id}").json())
    print(requests.delete(f"{USERS_URL}/{user_id}").json())
print(requests.get(f"{USERS_URL}/999999").json())

if job_id:
    update_payload = {
        "job_title": "Updated Job",
        "work_size": 12,
        "collaborators": "2,3,4",
        "is_finished": True,
        "team_leader": 1
    }
    print(requests.put(f"{JOBS_URL}/{job_id}", json=update_payload).json())
    print(requests.get(f"{JOBS_URL}/{job_id}").json())
    print(requests.delete(f"{JOBS_URL}/{job_id}").json())
print(requests.get(f"{JOBS_URL}/999999").json())
print(requests.delete(f"{JOBS_URL}/999999").json())
