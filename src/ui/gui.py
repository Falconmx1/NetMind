"""Interfaz gráfica con Tkinter para NetMind"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from src.core.capture import PacketCapture
from src.core.exporter import ExportManager
from src.ai.advanced_models import NetworkAnomalyDetector
from src.ui.dashboard import DashboardServer

class NetMindGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NetMind - Herramienta de Red con IA 🧠")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2c3e50')
        
        self.capturer = PacketCapture()
        self.exporter = ExportManager()
        self.detector = NetworkAnomalyDetector()
        self.dashboard_server = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz gráfica"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#3498db', foreground='white', padding=10)
        style.configure('TLabel', background='#2c3e50', foreground='white', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title = ttk.Label(main_frame, text="🧠 NetMind - Análisis de Red con IA", style='Title.TLabel')
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Panel de control izquierdo
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Interfaz
        ttk.Label(control_frame, text="Interfaz de red:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.interface_entry = ttk.Entry(control_frame, width=20)
        self.interface_entry.grid(row=0, column=1, pady=5)
        self.interface_entry.insert(0, "eth0")
        
        # Botones
        ttk.Button(control_frame, text="🔍 Capturar Paquetes", command=self.start_capture).grid(row=1, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        ttk.Button(control_frame, text="🤖 Detectar Anomalías", command=self.detect_anomalies).grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        ttk.Button(control_frame, text="📊 Dashboard Web", command=self.open_dashboard).grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        ttk.Button(control_frame, text="💾 Exportar Resultados", command=self.export_results).grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        ttk.Button(control_frame, text="🗑️ Limpiar", command=self.clear_display).grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        
        # Panel de resultados derecho
        result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        result_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=60, height=35, font=('Consolas', 9))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Panel de estadísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas", padding="10")
        stats_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        self.stats_text = tk.Text(stats_frame, width=25, height=35, font=('Arial', 10), bg='#34495e', fg='white')
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    def start_capture(self):
        """Inicia la captura en un hilo separado"""
        def capture_thread():
            interface = self.interface_entry.get()
            self.log_message(f"🔍 Iniciando captura en {interface}...")
            packets = self.capturer.start_capture(interface=interface if interface != "eth0" else None, count=50)
            self.log_message(f"✅ Capturados {len(packets)} paquetes")
            self.packets = packets
            self.update_stats()
        
        threading.Thread(target=capture_thread, daemon=True).start()
    
    def detect_anomalies(self):
        """Detecta anomalías usando IA"""
        if not hasattr(self, 'packets') or not self.packets:
            self.log_message("⚠️ Primero captura algunos paquetes")
            return
        
        def detect_thread():
            self.log_message("🧠 Ejecutando detección de anomalías con IA...")
            results = self.detector.detect_all(self.packets)
            
            self.log_message(f"\n{'='*50}")
            self.log_message(f"📊 RESULTADOS DEL ANÁLISIS")
            self.log_message(f"{'='*50}")
            self.log_message(f"Total paquetes: {results['statistics']['total_packets']}")
            self.log_message(f"Anomalías detectadas: {len(results['anomalies'])}")
            self.log_message(f"⚠️ Alerta DDoS: {'SÍ' if results['ddos_alert'] else 'NO'}")
            
            self.log_message(f"\n📋 Clasificación de tráfico:")
            for protocol, count in results['classified_traffic'].items():
                self.log_message(f"  {protocol}: {count} paquetes")
            
            if results['anomalies']:
                self.log_message(f"\n⚠️ ANOMALÍAS DETECTADAS:")
                for anomaly in results['anomalies'][:10]:
                    self.log_message(f"  {anomaly.get('src')} → {anomaly.get('dst')} (Puerto: {anomaly.get('dport')})")
            
            self.anomalies = results['anomalies']
            self.analysis_results = results
            
        threading.Thread(target=detect_thread, daemon=True).start()
    
    def open_dashboard(self):
        """Abre el dashboard web"""
        if not self.dashboard_server:
            self.dashboard_server = DashboardServer()
            self.dashboard_server.start()
            self.log_message("🌐 Dashboard web iniciado en http://localhost:5000")
        else:
            self.log_message("⚠️ Dashboard ya está ejecutándose")
    
    def export_results(self):
        """Exporta resultados a JSON/CSV"""
        if not hasattr(self, 'packets') or not self.packets:
            self.log_message("⚠️ No hay datos para exportar")
            return
        
        anomalies = getattr(self, 'anomalies', [])
        stats = getattr(self, 'analysis_results', {}).get('statistics', {})
        
        result = self.exporter.export_report(self.packets, anomalies, stats)
        self.log_message(f"✅ Resultados exportados:\n  JSON: {result['json']}")
        if result['csv']:
            self.log_message(f"  CSV: {result['csv']}")
    
    def update_stats(self):
        """Actualiza el panel de estadísticas"""
        if hasattr(self, 'packets'):
            stats = f"""
📈 ESTADÍSTICAS DE RED
{'='*30}

Paquetes totales: {len(self.packets)}

IPs origen únicas: 
{len(set(p.get('src') for p in self.packets if p.get('src')))}

IPs destino únicas:
{len(set(p.get('dst') for p in self.packets if p.get('dst')))}

Puertos más comunes:
{self.get_common_ports()}

Tamaño promedio:
{sum(p.get('length',0) for p in self.packets)/len(self.packets):.0f} bytes
"""
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats)
    
    def get_common_ports(self):
        """Obtiene los puertos más comunes"""
        from collections import Counter
        ports = [p.get('dport', 0) for p in self.packets if p.get('dport')]
        common = Counter(ports).most_common(5)
        return '\n'.join([f"  {port}: {count}" for port, count in common])
    
    def log_message(self, message):
        """Agrega un mensaje al área de resultados"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
    
    def clear_display(self):
        """Limpia el área de resultados"""
        self.result_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        self.log_message("🧹 Pantalla limpiada")
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = NetMindGUI()
    app.run()
