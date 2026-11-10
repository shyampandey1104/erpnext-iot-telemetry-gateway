# 🏭 ERPNext Industrial IoT Telemetry Gateway

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MQTT](https://img.shields.io/badge/MQTT-v5.0-orange.svg?logo=mqtt)](https://mqtt.org)
[![ERPNext](https://img.shields.io/badge/ERPNext-Smart%20Manufacturing-blue.svg)](https://erpnext.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A real-time **Industrial IoT (IIoT) Sensor Gateway & Predictive Maintenance Bridge** for **ERPNext Smart Manufacturing**. Subscribes to shop-floor telemetry (temperature, vibration, power consumption, RPM, and piece count) over **MQTT / Modbus**, evaluates machine health against **ISO 10816** standards, and automatically triggers **Maintenance Visits** in ERPNext when anomalies occur.

---

## ⚡ Key Highlights

- 📡 **MQTT Telemetry Broker Ingestion**: Listens to multi-topic factory streams (`factory/{machine_id}/telemetry`).
- ⚠️ **Edge Rule Engine**: Real-time detection of bearing overheating (>85°C), anomalous mechanical vibration (>4.5 mm/s RMS), and electrical power surges.
- 🛠️ **Automated ERPNext Maintenance Dispatch**: Auto-creates unscheduled `Maintenance Visit` or breakdown `Work Order` records in ERPNext without human delay.
- 📈 **Real-Time Live Dashboard**: Embedded WebSocket + Chart.js dashboard showing live multi-machine temperature trends and status.
- 🧪 **Factory Floor Simulator**: Built-in simulator script generating realistic factory telemetry with periodic anomaly injection.

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│      Factory Floor Machines (CNC, Lathe, Molding)      │
│          Sensors: Temp, Vibration, Current, RPM         │
└───────────────────────────┬────────────────────────────┘
                            │ MQTT Telemetry Payload
                            ▼
┌────────────────────────────────────────────────────────┐
│           Eclipse Mosquitto / EMQX MQTT Broker         │
└───────────────────────────┬────────────────────────────┘
                            │ Topic: factory/+/telemetry
                            ▼
┌────────────────────────────────────────────────────────┐
│          ERPNext IoT Telemetry Gateway (Python)        │
│  • Async MQTT Consumer                                 │
│  • Edge Rule Engine (ISO 10816 Thresholds)             │
│  • WebSocket Broadcast to Live Dashboard               │
└───────────────────────────┬────────────────────────────┘
                            │ REST Whitelist
                            ▼
┌────────────────────────────────────────────────────────┐
│                   ERPNext Desk                         │
│  • Asset Telemetry Logs                                │
│  • Automated Maintenance Visit Creation                │
│  • Work Order Downtime Tracking                        │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Quickstart

### 1. Installation

```bash
git clone https://github.com/shyampandey1104/erpnext-iot-telemetry-gateway.git
cd erpnext-iot-telemetry-gateway
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env`:
```env
ERPNEXT_URL=https://your-site.frappe.cloud
ERPNEXT_API_KEY=your_api_key
ERPNEXT_API_SECRET=your_api_secret
MQTT_BROKER=localhost
MQTT_PORT=1883
```

### 3. Launch Gateway Dashboard

```bash
uvicorn gateway.web_dashboard:app --reload --port 8000
```
Open `http://localhost:8000` to view the live factory dashboard.

### 4. Run Machine Sensor Simulator

In a separate terminal, run the sensor generator:
```bash
python3 simulator/simulate_factory_sensors.py
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

Author: **Shyamkumar Bhupendra Pandey** ([@shyampandey1104](https://github.com/shyampandey1104))
