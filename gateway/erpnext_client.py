"""ERPNext REST dispatcher for IoT Telemetry and Predictive Maintenance."""

import logging
from typing import Any, Dict, Optional
import httpx
from gateway.config import settings
from gateway.rule_engine import AnomalyAlert, TelemetryReading

logger = logging.getLogger(__name__)


class ERPNextIoTDispatcher:
    def __init__(self):
        self.base_url = settings.ERPNEXT_URL.rstrip("/")
        self.headers = {
            "Authorization": f"token {settings.ERPNEXT_API_KEY}:{settings.ERPNEXT_API_SECRET}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def log_telemetry(self, reading: TelemetryReading) -> bool:
        """Post telemetry batch to ERPNext IoT Log DocType."""
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                payload = {
                    "doctype": "Asset Telemetry Log",
                    "asset": reading.asset_id,
                    "machine_id": reading.machine_id,
                    "temperature": reading.temperature_celsius,
                    "vibration": reading.vibration_rms,
                    "power_consumption": reading.power_kw,
                    "rpm": reading.rpm,
                    "cycle_count": reading.cycle_count,
                }
                res = await client.post(
                    f"{self.base_url}/api/resource/Asset Telemetry Log",
                    headers=self.headers,
                    json=payload,
                )
                return res.status_code in (200, 201)
            except Exception as e:
                logger.error(f"Failed to log telemetry to ERPNext: {e}")
                return False

    async def create_maintenance_visit(self, alert: AnomalyAlert) -> Optional[str]:
        """Auto-create ERPNext Maintenance Visit or Work Order upon critical breach."""
        async with httpx.AsyncClient(timeout=8.0) as client:
            try:
                payload = {
                    "doctype": "Maintenance Visit",
                    "maintenance_type": "Unscheduled",
                    "customer": "Internal Plant Operations",
                    "completion_status": "Partially Completed",
                    "description": f"AUTOMATED IOT ALERT [{alert.severity}]: {alert.message}",
                    "purposes": [
                        {
                            "item_code": alert.asset_id,
                            "maintenance_type": "Breakdown",
                            "work_done": f"Diagnose anomaly: {alert.anomaly_type} (value: {alert.value}, threshold: {alert.threshold})",
                        }
                    ],
                }
                res = await client.post(
                    f"{self.base_url}/api/resource/Maintenance Visit",
                    headers=self.headers,
                    json=payload,
                )
                if res.status_code in (200, 201):
                    doc_name = res.json().get("data", {}).get("name")
                    logger.info(f"Successfully auto-created ERPNext Maintenance Visit: {doc_name}")
                    return doc_name
            except Exception as e:
                logger.error(f"Failed to create Maintenance Visit in ERPNext: {e}")
        return None
