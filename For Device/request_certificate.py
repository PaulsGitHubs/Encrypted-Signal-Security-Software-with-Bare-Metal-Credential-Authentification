import requests
import json

def request_certificate(device_id, password):
    server_url = "http://your_server_address:8080/generate_certificate"
    payload = {
        "device_id": device_id,
        "password": password
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(server_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("Certificate generation successful.")
        certificate = json.loads(response.text).get("certificate")
        print("Received certificate: ", certificate)
    else:
        print("Failed to generate certificate.")

# The device_id and password would be stored securely on the microcontroller
device_id = "DeviceID_12345"
password = "SecurePassword"

request_certificate(device_id, password)
