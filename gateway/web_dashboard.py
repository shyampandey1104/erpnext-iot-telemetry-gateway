"""FastAPI Live Telemetry Dashboard & WebSocket Server."""

import json
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from gateway.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Real-time MQTT ingestion & WebSocket telemetry stream for ERPNext Assets.",
    version="1.0.0",
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass


manager = ConnectionManager()


@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep socket alive
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return """<!DOCTYPE html>
<html>
<head>
    <title>ERPNext Industrial IoT Real-time Telemetry</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 p-8 font-sans">
    <div class="max-w-6xl mx-auto">
        <header class="flex justify-between items-center mb-8 border-b border-slate-800 pb-4">
            <div>
                <h1 class="text-2xl font-bold text-white">🏭 ERPNext Smart Factory IoT Telemetry</h1>
                <p class="text-xs text-slate-400 mt-1">Real-time MQTT Sensor Gateway • Asset Health Monitor</p>
            </div>
            <div id="conn-badge" class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                ● Live Streaming
            </div>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <div class="text-xs text-slate-400 uppercase font-bold">CNC Milling (MCH-01)</div>
                <div id="temp-mch-01" class="text-3xl font-mono font-bold text-emerald-400 mt-2">-- °C</div>
                <div id="vib-mch-01" class="text-xs text-slate-400 mt-1">Vibration: -- mm/s</div>
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <div class="text-xs text-slate-400 uppercase font-bold">Injection Molding (MCH-02)</div>
                <div id="temp-mch-02" class="text-3xl font-mono font-bold text-amber-400 mt-2">-- °C</div>
                <div id="vib-mch-02" class="text-xs text-slate-400 mt-1">Vibration: -- mm/s</div>
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <div class="text-xs text-slate-400 uppercase font-bold">Hydraulic Press (MCH-03)</div>
                <div id="temp-mch-03" class="text-3xl font-mono font-bold text-blue-400 mt-2">-- °C</div>
                <div id="vib-mch-03" class="text-xs text-slate-400 mt-1">Vibration: -- mm/s</div>
            </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h2 class="text-sm font-bold text-white mb-4">Live Telemetry Trend (Temperature °C)</h2>
            <canvas id="telemetryChart" height="90"></canvas>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('telemetryChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    { label: 'MCH-01 (CNC Milling)', borderColor: '#10b981', data: [], tension: 0.3 },
                    { label: 'MCH-02 (Injection Molding)', borderColor: '#f59e0b', data: [], tension: 0.3 },
                    { label: 'MCH-03 (Hydraulic Press)', borderColor: '#3b82f6', data: [], tension: 0.3 }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } },
                    y: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' }, min: 40, max: 110 }
                }
            }
        });

        // WebSocket connection
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const ws = new WebSocket(`${protocol}//${window.location.host}/ws/telemetry`);

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const now = new Date().toLocaleTimeString();

            if (data.machine_id === 'MCH-01') {
                document.getElementById('temp-mch-01').innerText = `${data.temperature_celsius.toFixed(1)} °C`;
                document.getElementById('vib-mch-01').innerText = `Vibration: ${data.vibration_rms.toFixed(2)} mm/s`;
            } else if (data.machine_id === 'MCH-02') {
                document.getElementById('temp-mch-02').innerText = `${data.temperature_celsius.toFixed(1)} °C`;
                document.getElementById('vib-mch-02').innerText = `Vibration: ${data.vibration_rms.toFixed(2)} mm/s`;
            } else if (data.machine_id === 'MCH-03') {
                document.getElementById('temp-mch-03').innerText = `${data.temperature_celsius.toFixed(1)} °C`;
                document.getElementById('vib-mch-03').innerText = `Vibration: ${data.vibration_rms.toFixed(2)} mm/s`;
            }

            if (chart.data.labels.length > 20) {
                chart.data.labels.shift();
                chart.data.datasets.forEach(d => d.data.shift());
            }
            chart.data.labels.push(now);
            const idx = data.machine_id === 'MCH-01' ? 0 : data.machine_id === 'MCH-02' ? 1 : 2;
            chart.data.datasets[idx].data.push(data.temperature_celsius);
            chart.update();
        };
    </script>
</body>
</html>"""
