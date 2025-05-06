import http.client
import json

data = {
    "email": "user2@example.com",
    "password": "pass1234",
    "name": "Rahul"
}

json_data = json.dumps(data)

conn = http.client.HTTPConnection("localhost:5000")

headers = {'Content-Type': 'application/json'}
conn.request("POST", "/register", body=json_data, headers=headers)

response = conn.getresponse()
print(f"Status Code: {response.status}")
print("Response Body:")
print(response.read().decode())