import requests
res = requests.post("http://127.0.0.1:8000/api/register", json={
    "name": "Live Test User 3",
    "email": "live3@test.com",
    "password": "mypassword"
})
print("STATUS:", res.status_code)
print("TEXT:", res.text)
