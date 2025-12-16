import time
import random
import requests
import os
import sys

# Configuration
INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
ORG = os.getenv("INFLUX_ORG", "myorg")
BUCKET = os.getenv("INFLUX_BUCKET", "system_metrics")
TOKEN = os.getenv("INFLUX_TOKEN")

# Set precision to nanoseconds for strict line protocol compliance
WRITE_URL = f"{INFLUX_URL}/api/v2/write?org={ORG}&bucket={BUCKET}&precision=ns"

def generate_value(sensor_type):
    """Generates random values within realistic ranges."""
    if sensor_type == "temperature":
        return round(random.uniform(15.0, 35.0), 2)  # 15-35 C
    elif sensor_type == "humidity":
        return round(random.uniform(30.0, 80.0), 2)  # 30-80%
    elif sensor_type == "pressure":
        return round(random.uniform(980.0, 1020.0), 2)  # 980-1020 hPa
    return 0.0

def send_data():
    sensor_types = ["temperature", "humidity", "pressure"]
    sensor_ids = ["sensor_01", "sensor_02", "sensor_03"]
    
    lines = []
    # Capture current time in nanoseconds
    ns_timestamp = time.time_ns()

    for s_id in sensor_ids:
        for s_type in sensor_types:
            val = generate_value(s_type)
            
            # Format: measurement,tag_set field_set timestamp
            # Matches example: temperature,sensor_id=sensor_01 value=23.5 16383...
            line = f"{s_type},sensor_id={s_id},location=factory_floor value={val} {ns_timestamp}"
            lines.append(line)

    data = "\n".join(lines)
    
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "text/plain; charset=utf-8"
    }

    try:
        response = requests.post(WRITE_URL, data=data, headers=headers)
        if response.status_code != 204:
            print(f"Error sending data: {response.status_code} - {response.text}")
        else:
            print(f"Successfully pushed {len(lines)} metrics.")
            
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    print("Starting IoT Sensor Simulator...")
    
    if not TOKEN:
        print("Error: INFLUX_TOKEN environment variable is missing.")
        sys.exit(1)

    while True:
        send_data()
        time.sleep(5)