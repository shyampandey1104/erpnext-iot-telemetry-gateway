"""Configuration for ERPNext IoT Telemetry Gateway."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ERPNext Industrial IoT Telemetry Gateway"
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_TOPIC: str = "factory/+/telemetry"
    MQTT_CLIENT_ID: str = "erpnext_telemetry_gateway"

    # ERPNext settings
    ERPNEXT_URL: str = "http://localhost:8000"
    ERPNEXT_API_KEY: str = "admin_api_key"
    ERPNEXT_API_SECRET: str = "admin_api_secret"

    # Industrial Thresholds for Auto-Maintenance Visit
    MAX_TEMP_CELSIUS: float = 85.0
    MAX_VIBRATION_RMS: float = 4.5  # mm/s
    MAX_POWER_KW: float = 25.0

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
