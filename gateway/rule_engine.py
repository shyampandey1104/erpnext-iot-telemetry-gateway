"""Rule engine evaluating industrial telemetry for predictive maintenance."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class TelemetryReading(BaseModel):
    machine_id: str
    asset_id: str
    workstation: str
    temperature_celsius: float
    vibration_rms: float  # mm/s
    power_kw: float
    rpm: int
    cycle_count: int
    timestamp: Optional[str] = None


class AnomalyAlert(BaseModel):
    machine_id: str
    asset_id: str
    anomaly_type: str
    severity: str  # Critical, Warning, Info
    value: float
    threshold: float
    message: str


class RuleEngine:
    def __init__(self, max_temp: float = 85.0, max_vibration: float = 4.5, max_power: float = 25.0):
        self.max_temp = max_temp
        self.max_vibration = max_vibration
        self.max_power = max_power

    def evaluate(self, reading: TelemetryReading) -> List[AnomalyAlert]:
        """Scan reading against industrial threshold parameters."""
        alerts: List[AnomalyAlert] = []

        # Temperature check
        if reading.temperature_celsius > self.max_temp:
            alerts.append(
                AnomalyAlert(
                    machine_id=reading.machine_id,
                    asset_id=reading.asset_id,
                    anomaly_type="Overheating",
                    severity="Critical" if reading.temperature_celsius > (self.max_temp + 10) else "Warning",
                    value=reading.temperature_celsius,
                    threshold=self.max_temp,
                    message=f"Machine {reading.machine_id} bearing temperature {reading.temperature_celsius}°C exceeded safety threshold {self.max_temp}°C",
                )
            )

        # Vibration analysis (ISO 10816 machinery vibration standard)
        if reading.vibration_rms > self.max_vibration:
            alerts.append(
                AnomalyAlert(
                    machine_id=reading.machine_id,
                    asset_id=reading.asset_id,
                    anomaly_type="High Vibration",
                    severity="Critical",
                    value=reading.vibration_rms,
                    threshold=self.max_vibration,
                    message=f"Machine {reading.machine_id} abnormal vibration {reading.vibration_rms} mm/s detected (misalignment or bearing wear)",
                )
            )

        # Power surge / over-current
        if reading.power_kw > self.max_power:
            alerts.append(
                AnomalyAlert(
                    machine_id=reading.machine_id,
                    asset_id=reading.asset_id,
                    anomaly_type="Power Surge",
                    severity="Warning",
                    value=reading.power_kw,
                    threshold=self.max_power,
                    message=f"Excessive load: {reading.power_kw} kW exceeding motor rating {self.max_power} kW",
                )
            )

        return alerts
