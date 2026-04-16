import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

response = client.post("/api/register", json={
    "name": "Live Test User",
    "email": "live1@test.com",
    "password": "mypassword"
})

print("Status Code:", response.status_code)
print("Response:", response.text)
