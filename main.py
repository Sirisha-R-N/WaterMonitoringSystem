import RPi.GPIO as GPIO 
import time 
import requests 
import math 
THINGSPEAK_API_KEY = "UCIWIE9EV2HQ8VD8"  # Replace with your API key 
THINGSPEAK_URL = 
"https://api.thingspeak.com/update?api_key=UCIWIE9EV2HQ8VD8&field1=0" 
TRIG = 23  # GPIO Pin for Trigger 
ECHO = 24  # GPIO Pin for Echo 
TANK_HEIGHT = 11  # Tank height in cm 
TANK_RADIUS = 3  # Tank radius in cm 
FLOW_SENSOR = 13  # GPIO Pin for Flow Sensor 
PULSES_PER_ML = 10  # Example: 10 pulses = 1 ml (adjust based on your sensor) 
threshold_volume = 1  # Example threshold volume in mL 
warning_count = 0  # Counter to track warnings 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(TRIG, GPIO.OUT) 
GPIO.setup(ECHO, GPIO.IN) 
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
def measure_water_level(): 
"""Measures the water level using HC-SR04 sensor.""" 
GPIO.output(TRIG, True) 
time.sleep(0.00001) 
GPIO.output(TRIG, False) 
timeout = time.time() + 2 
pulse_start, pulse_end = 0, 0 
while GPIO.input(ECHO) == 0: 
pulse_start = time.time() 
if pulse_start > timeout: 
return None   
while GPIO.input(ECHO) == 1: 
pulse_end = time.time() 
if pulse_end > timeout: 
return None   
pulse_duration = pulse_end - pulse_start 
distance = (pulse_duration * 34300) / 2 
water_level = max(0, TANK_HEIGHT - distance) 
return round(water_level, 2) if 0 <= water_level <= TANK_HEIGHT else None 
def convert_to_liters(water_level): 
"""Converts water level to volume (liters) for a cylindrical tank.""" 
if TANK_RADIUS <= 0 or water_level <= 0: 
return None 
volume = math.pi * (TANK_RADIUS ** 2) * water_level / 1000 
return round(volume, 4) 
def calculate_volume(pulses): 
"""Calculate volume in mL based on the number of pulses.""" 
return pulses / PULSES_PER_ML 
def upload_to_thingspeak(water_level, volume_liters, total_volume): 
"""Uploads water level, tank volume, and flow sensor volume to ThingSpeak.""" 
    payload = { 
        "api_key": THINGSPEAK_API_KEY, 
        "field1": water_level, 
        "field2": volume_liters, 
        "field3": total_volume  # Flow sensor total volume in m 
 } 
    try: 
        response = requests.get(THINGSPEAK_URL, params=payload, timeout=5) 
        if response.status_code == 200: 
            print(f"Data Uploaded") 
        else: 
            print(f"Failed to upload data, Status Code: {response.status_code}") 
    except requests.exceptions.RequestException as e: 
        print(f" Request failed: {e}") 
try: 
    pulses = 0 
    total_volume = 0 
    while True: 
        # Measure water level 
        water_level = measure_water_level() 
        if water_level is None: 
            print("Skipping invalid sensor reading...") 
        else: 
            volume_liters = convert_to_liters(water_level) 
            print(f"Water Level: {water_level} cm | Tank Volume: {volume_liters} L") 
        sensor_state = GPIO.input(FLOW_SENSOR) 
        print(f"Flow Sensor State: {sensor_state}") 
        if sensor_state == 0: 
            pulses += 1 
        time.sleep(1)  # Wait for 1 second 
        if pulses > 0: 
            volume_ml = calculate_volume(pulses) 
            total_volume += volume_ml 
            print(f"Flow rate this second: {volume_ml} mL | Total Water consumed: 
{total_volume} mL") 
            if total_volume > threshold_volume: 
                warning_count += 1 
                if warning_count == 1: 
                    print("High water consumption - First warning issued") 
                elif warning_count == 2: 
                    print("High water consumption - Second warning issued") 
                elif warning_count == 3: 
                    print("Water supply will be cut soon") 

GPIO.cleanup() 
break 
pulses = 0  # Reset pulse counter 
upload_to_thingspeak(water_level, total_volume, volume_ml) 
time.sleep(5)  # ThingSpeak allows updates every 15 sec 
except KeyboardInterrupt: 
print("\nExiting... Cleaning up GPIO") 
GPIO.cleanup()
