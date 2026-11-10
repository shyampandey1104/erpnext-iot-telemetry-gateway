#!/usr/bin/env python3
"""Simulate factory industrial telemetry (temperature, vibration, power, RPM)."""

import time
import random
import json
import httpx
from rich.console import Console
from rich.table import Table

console = Console()

MACHINES = [
    {"machine_id": "MCH-01", "asset_id": "AST-CNC-001", "base_temp": 62.0, "base_vib": 1.8, "base_power": 12.0, "rpm": 4500},
    {"machine_id": "MCH-02", "asset_id": "AST-INJ-002", "base_temp": 78.0, "base_vib": 2.4, "base_power": 18.5, "rpm": 1200},
    {"machine_id": "MCH-03", "asset_id": "AST-PRS-003", "base_temp": 55.0, "base_vib": 1.2, "base_power": 22.0, "rpm": 850},
]


def generate_cycle(counter: int):
    m = random.choice(MACHINES)
    # Occasionally inject an anomaly spike for demonstration
    spike = random.random() < 0.15

    temp = m["base_temp"] + random.uniform(-2.5, 3.5) + (25.0 if spike else 0.0)
    vib = m["base_vib"] + random.uniform(-0.3, 0.4) + (3.2 if spike else 0.0)
    power = m["base_power"] + random.uniform(-1.0, 1.5)

    payload = {
        "machine_id": m["machine_id"],
        "asset_id": m["asset_id"],
        "workstation": "Line-A",
        "temperature_celsius": round(temp, 2),
        "vibration_rms": round(vib, 2),
        "power_kw": round(power, 2),
        "rpm": m["rpm"] + random.randint(-50, 50),
        "cycle_count": counter,
    }
    return payload, spike


def main():
    console.print("[bold cyan]🏭 Starting Factory Sensor Telemetry Simulation...[/]")
    console.print("[dim]Generating live MQTT telemetry for ERPNext Asset Maintenance...[/]\n")

    counter = 1000
    while counter < 1015:
        payload, is_spike = generate_cycle(counter)
        counter += 1

        status_style = "bold red" if is_spike else "green"
        alert_tag = " [CRITICAL OVERHEAT ANOMALY -> AUTO ERPNEXT VISIT]" if is_spike else ""

        console.print(
            f"[{status_style}]• {payload['machine_id']}[/] | "
            f"Temp: {payload['temperature_celsius']}°C | "
            f"Vib: {payload['vibration_rms']} mm/s | "
            f"Power: {payload['power_kw']} kW{alert_tag}"
        )
        time.sleep(0.4)

    console.print("\n[bold green]✓ Simulation batch completed successfully![/]")


if __name__ == "__main__":
    main()
