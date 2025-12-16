# IoT & System Monitoring Solution

This project implements a fully containerized monitoring stack using **InfluxDB** and **Grafana**, designed to monitor system resources and simulate an IoT sensor network. It is built to be strictly compliant with the machine test requirements.

## ⚙️ Setup Instructions

### Prerequisites
* Docker Desktop / Docker Engine installed and running.
* Git.

### Installation & Execution
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Ajin-k-j/MachineTest.git
    ```

2.  **Start the Services**
    Run the following command from the project root. This will build the python images and start the container stack:
    ```bash
    # Note: We point to the compose file in the docker folder
    docker-compose --env-file .env -f docker/docker-compose.yml up -d --build
    ```

3.  **Verify Status**
    Ensure all 4 containers are running:
    ```bash
    docker ps
    ```

## 🖥️  Each Component

* **InfluxDB (Database):** Starts on port `8086`. Automatically provisions the `myorg` organization and `system_metrics` bucket using environment variables.
* **Grafana (Dashboard):** Starts on port `3000`. Automatically connects to InfluxDB and imports the dashboards via provisioning scripts.
* **System Monitor:** A background Python container that collects host CPU, Memory, and Disk usage every 5 seconds and pushes it to InfluxDB.
* **IoT Simulator:** A background Python container that generates realistic data for 3 sensors (Temperature, Humidity, Pressure) and pushes it using the InfluxDB Line Protocol.

## 🔐 Default Credentials

The following default credentials are pre-configured in the `.env` file for testing purposes:

| Service | URL | Username | Password |
| :--- | :--- | :--- | :--- |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | `admin` | `admin` |
| **InfluxDB** | [http://localhost:8086](http://localhost:8086) | `admin` | `adminpassword123` |


## 📈 Expected Output / Results

1.  **System Monitoring Dashboard:**
    * Navigate to **Dashboards > Machine Test: System Monitoring**.
    * You should see live gauges for **CPU**, **Memory**, and **Disk Usage**.
    * Graphs will update every 5 seconds.

2.  **IoT Sensor Monitoring Dashboard:**
    * Navigate to **Dashboards > Machine Test: Sensor_Monitoring**.
    * You will see live data streams for **Temperature** (15-35°C), **Humidity** (30-80%), and **Pressure** (980-1020 hPa).
    * Data is simulated for three distinct devices (`sensor_01`, `sensor_02`, `sensor_03`).

## 🧠 Assumptions & Design Decisions


1.  **Sensor Logic:**
    * To satisfy the requirement of "at least 3 different sensor types" while providing rich visualization, the simulation creates 3 smart devices (`sensor_01` to `03`), where *each* device is capable of measuring Temperature, Humidity, and Pressure simultaneously. This allows for comparative graphing in Grafana.

2.  **Automation Strategy:**
    * Instead of external shell scripts for setup, I leveraged **Docker Environment Variables** and **Grafana Provisioning**. This ensures the system is idempotent and ready immediately after `docker-compose up`, eliminating race conditions or manual configuration steps.

3. **Credentials & Source Control (.env):**
    * **Note:** In a production environment, `.env` files containing secrets are strictly ignored via `.gitignore`.
    * **Decision:** For this machine test, I have intentionally removed `.env` from `.gitignore` and committed it to the repository. This is done to ensure the reviewer can clone and run the project immediately ("plug-and-play") without needing to manually configure secrets or copy-paste credentials.