"""Dashboard web simple para NetMind"""
import json
from flask import Flask, render_template_string, jsonify
from threading import Thread
import webbrowser
import os

app = Flask(__name__)

# Template HTML para el dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NetMind Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            color: #666;
            margin-bottom: 10px;
        }
        .stat-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .anomaly-list {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .anomaly-item {
            border-left: 4px solid #ff4757;
            padding: 10px;
            margin: 10px 0;
            background: #f8f9fa;
        }
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 20px;
        }
        .refresh-btn:hover {
            background: #764ba2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 NetMind Dashboard</h1>
            <p>Análisis de red con Inteligencia Artificial</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Paquetes Totales</h3>
                <div class="value" id="totalPackets">0</div>
            </div>
            <div class="stat-card">
                <h3>Anomalías Detectadas</h3>
                <div class="value" id="anomalies">0</div>
            </div>
            <div class="stat-card">
                <h3>Protocolos Únicos</h3>
                <div class="value" id="protocols">0</div>
            </div>
        </div>
        
        <div class="anomaly-list">
            <h2>⚠️ Anomalías Detectadas</h2>
            <div id="anomaliesList"></div>
        </div>
        
        <button class="refresh-btn" onclick="refreshData()">🔄 Actualizar</button>
    </div>
    
    <script>
        async function refreshData() {
            const response = await fetch('/api/data');
            const data = await response.json();
            
            document.getElementById('totalPackets').textContent = data.total_packets;
            document.getElementById('anomalies').textContent = data.anomalies_count;
            document.getElementById('protocols').textContent = data.unique_protocols;
            
            const anomaliesList = document.getElementById('anomaliesList');
            anomaliesList.innerHTML = '';
            
            data.anomalies.forEach(anomaly => {
                const div = document.createElement('div');
                div.className = 'anomaly-item';
                div.innerHTML = `
                    <strong>${anomaly.src}</strong> → <strong>${anomaly.dst}</strong><br>
                    Protocolo: ${anomaly.protocol || 'Unknown'} | Puertos: ${anomaly.sport || '?'} → ${anomaly.dport || '?'}<br>
                    Tamaño: ${anomaly.length} bytes
                `;
                anomaliesList.appendChild(div);
            });
        }
        
        refreshData();
        setInterval(refreshData, 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/data')
def api_data():
    """Endpoint para obtener datos en tiempo real"""
    from src.core.capture import PacketCapture
    # Aquí iría la lógica para obtener datos reales
    # Por ahora devolvemos datos de ejemplo
    return jsonify({
        'total_packets': 1234,
        'anomalies_count': 5,
        'unique_protocols': 3,
        'anomalies': [
            {'src': '192.168.1.100', 'dst': '10.0.0.5', 'protocol': 'TCP', 'sport': 54321, 'dport': 80, 'length': 1500},
            {'src': '192.168.1.102', 'dst': '8.8.8.8', 'protocol': 'UDP', 'sport': 12345, 'dport': 53, 'length': 64}
        ]
    })

class DashboardServer:
    def __init__(self, port=5000):
        self.port = port
        self.server = None
        
    def start(self):
        """Inicia el servidor del dashboard"""
        def run_server():
            app.run(host='127.0.0.1', port=self.port, debug=False, use_reloader=False)
        
        thread = Thread(target=run_server, daemon=True)
        thread.start()
        webbrowser.open(f'http://localhost:{self.port}')
        print(f"🌐 Dashboard web iniciado en http://localhost:{self.port}")
