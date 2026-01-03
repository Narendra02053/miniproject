
import requests
import json

try:
    url = "http://127.0.0.1:8000/api/auth/login"
    payload = {"email": "debug_test@example.com", "password": "password123"}
    headers = {"Content-Type": "application/json"}
    
    print(f"Sending POST to {url}...")
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print("Response Headers:")
    print(json.dumps(dict(response.headers), indent=2))
    print("Response Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
        
except Exception as e:
    print(f"An error occurred: {e}")
