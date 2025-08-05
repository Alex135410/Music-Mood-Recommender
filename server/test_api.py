import requests

url = 'http://127.0.0.1:5000/predict'
text_input = {"text": "I feel very anxious and nervous"}

response = requests.post(url, json=text_input)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
