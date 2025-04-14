import requests

THINGSPEAK_WRITE_API_KEY = "U8QCG8VY803R89UJ"  # Replace with your actual ThingSpeak Write API Key
THINGSPEAK_URL = "https://api.thingspeak.com/update?api_key=U8QCG8VY803R89UJ&field1=0&field2=0&field3=0"

params = {
    "api_key": THINGSPEAK_WRITE_API_KEY,
    "field1": 20 ,# Example: Sending water level as 50
    "field2": 0.2,
    "field3": 0.1
}

response = requests.get(THINGSPEAK_URL, params=params)

if response.status_code == 200 and response.text != "0":
    print("Data successfully sent to ThingSpeak!")
else:
    print("Failed to send data. Response:", response.text)
