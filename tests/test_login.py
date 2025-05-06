import http.client
import json

data = {
    "email": "user@example.com",
    "password": "pass123"
}

json_data = json.dumps(data)

conn = http.client.HTTPConnection("localhost:5000")
headers = {'Content-Type': 'application/json'}
conn.request("POST", "/login", body=json_data, headers=headers)

response = conn.getresponse()
print(f"Status Code: {response.status}")
print("Response Body:")
print(response.read().decode())
