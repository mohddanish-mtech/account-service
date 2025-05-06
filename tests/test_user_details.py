import http.client

user_id = 2

conn = http.client.HTTPConnection("localhost:5000")
conn.request("GET", f"/user/{user_id}")

response = conn.getresponse()
print(f"Status Code: {response.status}")
print("Response Body:")
print(response.read().decode())