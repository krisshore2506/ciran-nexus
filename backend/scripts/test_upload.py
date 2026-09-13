import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Simple test script to verify API
url = "http://localhost:8000/api/upload"

sample_text = "Ravi Kumar contacted Mohan Das using phone XXXXX1234."
file_name = "test_case.txt"
with open(file_name, "w") as f:
    f.write(sample_text)

print(f"Uploading {file_name}...")
with open(file_name, "rb") as f:
    m = MultipartEncoder(
        fields={'file': (file_name, f, 'text/plain')}
    )
    headers = {'Content-Type': m.content_type}
    try:
        response = requests.post(url, data=m, headers=headers)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except Exception as e:
        print(f"Failed to connect to API: {e}")

os.remove(file_name)
