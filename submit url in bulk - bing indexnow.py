import requests
import json

# Replace with your actual domain and key
YOUR_DOMAIN = "www.example.com"
YOUR_KEY = "a1b2c3d4e5f67890"

# List of URLs to submit up to 1000 urls
urls_to_submit = [
    "https://www.example.com/url1",
    "https://www.example.com/folder/url2",
    "https://www.example.com/another-url"
]

# Construct the JSON payload
payload = {
    "host": YOUR_DOMAIN,
    "key": YOUR_KEY,
    "urlList": urls_to_submit
}

# Set the request headers
headers = {
    "Content-Type": "application/json; charset=utf-8"
}

# Send the POST request
response = requests.post("https://www.bing.com/indexnow", json=payload, headers=headers)

# Check the response
if response.status_code == 200:
    print("Bulk URL submission successful.")
else:
    print(f"Error during submission. Status code: {response.status_code}")
    print(response.text)
