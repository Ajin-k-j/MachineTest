import time
import psutil
import requests
import os
import sys

# Configuration from Environment Variables
INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
ORG = os.getenv("INFLUX_ORG", "myorg")
BUCKET = os.getenv("INFLUX_BUCKET", "system_metrics")
TOKEN = os.getenv("INFLUX_TOKEN")

# The Write API Endpoint
WRITE_URL = f"{INFLUX_URL}/api/v2/write?org={ORG}&bucket={BUCKET}&precision=s"

def get_system_metrics():
    """Collects CPU, RAM, and Disk metrics."""
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Memory
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    
    # Disk I/O (Read/Write bytes since boot)
    disk = psutil.disk_io_counters()
    # We will just report disk usage percentage
    disk_usage = psutil.disk_usage('/').percent

    return cpu_percent, mem_percent, disk_usage

def send_to_influx(cpu, mem, disk):
    """Sends metrics using InfluxDB Line Protocol."""
    # Line Protocol Format: measurement,tag=value field=value timestamp
    # We leave timestamp empty to let InfluxDB assign the server time.
    
    # Metric 1: CPU
    line_cpu = f"system_stats,host=docker_container cpu_usage={cpu}"
    
    # Metric 2: Memory
    line_mem = f"system_stats,host=docker_container mem_usage={mem}"
    
    # Metric 3: Disk
    line_disk = f"system_stats,host=docker_container disk_usage={disk}"

    data = f"{line_cpu}\n{line_mem}\n{line_disk}"

    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "text/plain; charset=utf-8"
    }

    try:
        response = requests.post(WRITE_URL, data=data, headers=headers)
        if response.status_code == 204:
            print(f"Sent: CPU={cpu}%, MEM={mem}%, DISK={disk}%")
        else:
            print(f"Error sending data: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    print("Starting System Monitor...")
    # Verify Token exists
    if not TOKEN:
        print("Error: INFLUX_TOKEN env var is missing.")
        sys.exit(1)

    while True:
        cpu, mem, disk = get_system_metrics()
        send_to_influx(cpu, mem, disk)
        # Wait 5 seconds before next reading
        time.sleep(5)