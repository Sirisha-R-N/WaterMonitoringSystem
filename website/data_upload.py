import time
import requests

# Your ThingSpeak Write API Key
API_KEY = "U8QCG8VY803R89UJ"

# Your list of values to upload
data_list = [
    {'field1': 11, 'field2': 0.2827, 'field3': 0.10},
    {'field1': 10.85, 'field2': 0.2789, 'field3': 0.15},
    {'field1': 10.5, 'field2': 0.2705, 'field3': 0.28},
    {'field1': 9.25, 'field2': 0.2383, 'field3': 0.54},   # First warning
    {'field1': 8.5, 'field2': 0.2190, 'field3': 0.35},
    {'field1': 7.75, 'field2': 0.1997, 'field3': 0.30},
    {'field1': 6, 'field2': 0.1546, 'field3': 0.60},       # Second warning
    {'field1': 5, 'field2': 0.1285, 'field3': 0.35},
    {'field1': 4, 'field2': 0.1028, 'field3': 0.40},
    {'field1': 3, 'field2': 0.0771, 'field3': 0.50},       # Water supply cut soon

    # Refill phase
    {'field1': 4, 'field2': 0.1028, 'field3': 0.00},
    {'field1': 5, 'field2': 0.1285, 'field3': 0.00},
    {'field1': 6, 'field2': 0.1546, 'field3': 0.00},
    {'field1': 7.5, 'field2': 0.1936, 'field3': 0.00},
    {'field1': 9, 'field2': 0.2317, 'field3': 0.00},
    {'field1': 10, 'field2': 0.2570, 'field3': 0.00},
    {'field1': 11, 'field2': 0.2827, 'field3': 0.00}

      # Water supply cut warning

    # Add more data points as needed
]

data_list = [
    {'field1': 3.93, 'field2': 0.2827, 'field3': 0.10}]
# ThingSpeak URL
url = "https://api.thingspeak.com/update?api_key=U8QCG8VY803R89UJ&field1=0&field2=0&field3=0"

# Upload data one by one with delay
for i, entry in enumerate(data_list):
    payload = {'api_key': API_KEY}
    payload.update(entry)  # Add fields to the payload

    response = requests.get(url, params=payload)

    if response.status_code == 200 and response.text != '0':
        print(f"[{i+1}] Data uploaded successfully: {entry}")
    else:
        print(f"[{i+1}] Failed to upload: {entry}, Response: {response.text}")

    # Wait at least 15 seconds before the next update (ThingSpeak limit)
    time.sleep(16)
