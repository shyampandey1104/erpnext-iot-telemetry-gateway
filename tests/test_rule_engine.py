"""Unit tests for IoT Rule Engine anomaly evaluation."""

from gateway.rule_engine import RuleEngine, TelemetryReading


def test_normal_telemetry_reading():
    engine = RuleEngine(max_temp=85.0, max_vibration=4.5)
    reading = TelemetryReading(
        machine_id="MCH-01",
        asset_id="AST-001",
        workstation="Line-1",
        temperature_celsius=65.0,
        vibration_rms=1.5,
        power_kw=10.0,
        rpm=3000,
        cycle_count=100,
    )
    alerts = engine.evaluate(reading)
    assert len(alerts) == 0


def test_overheating_anomaly_trigger():
    engine = RuleEngine(max_temp=85.0, max_vibration=4.5)
    reading = TelemetryReading(
        machine_id="MCH-01",
        asset_id="AST-001",
        workstation="Line-1",
        temperature_celsius=98.5,  # Exceeds threshold!
        vibration_rms=1.5,
        power_kw=10.0,
        rpm=3000,
        cycle_count=101,
    )
    alerts = engine.evaluate(reading)
    assert len(alerts) == 1
    assert alerts[0].anomaly_type == "Overheating"
    assert alerts[0].severity == "Critical"


def test_vibration_anomaly_trigger():
    engine = RuleEngine(max_temp=85.0, max_vibration=4.5)
    reading = TelemetryReading(
        machine_id="MCH-02",
        asset_id="AST-002",
        workstation="Line-2",
        temperature_celsius=60.0,
        vibration_rms=6.2,  # Exceeds 4.5 mm/s!
        power_kw=12.0,
        rpm=1500,
        cycle_count=205,
    )
    alerts = engine.evaluate(reading)
    assert len(alerts) == 1
    assert alerts[0].anomaly_type == "High Vibration"
