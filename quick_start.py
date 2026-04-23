"""Script de inicio rápido para NetMind"""
from src.core.capture import PacketCapture
from src.ai.detector import AnomalyDetector

def main():
    print("""
    ╔══════════════════════════════════╗
    ║      NetMind - Red con IA 🧠     ║
    ║    Análisis inteligente de red   ║
    ╚══════════════════════════════════╝
    """)
    
    # Capturar tráfico normal para entrenar
    print("📡 Paso 1: Capturando tráfico normal...")
    capturer = PacketCapture()
    normal_packets = capturer.start_capture(count=50)
    
    # Entrenar modelo
    print("🤖 Paso 2: Entrenando IA...")
    detector = AnomalyDetector()
    detector.train(normal_packets)
    
    # Capturar tráfico para analizar
    print("🔍 Paso 3: Analizando nuevo tráfico...")
    test_packets = capturer.start_capture(count=30)
    
    # Detectar anomalías
    anomalies = detector.detect(test_packets)
    
    if anomalies:
        print(f"⚠️  ¡Se detectaron {len(anomalies)} anomalías!")
        for anomaly in anomalies:
            print(f"   Sospechoso: {anomaly['src']} -> {anomaly['dst']}")
    else:
        print("✅ Todo normal - No se detectaron anomalías")

if __name__ == "__main__":
    main()
