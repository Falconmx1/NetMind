"""Modelos avanzados de IA para detección de DDoS y clasificación"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.cluster import DBSCAN
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class DDoSDetector:
    """Detector específico de ataques DDoS"""
    
    def __init__(self):
        self.model = IsolationForest(contamination=0.2, random_state=42)
        self.threshold = 100  # Paquetes por segundo como umbral
        
    def extract_flow_features(self, packets):
        """Extrae características de flujo para detección DDoS"""
        features = []
        
        # Agrupar por flujo (src, dst, dport)
        flows = {}
        for pkt in packets:
            key = (pkt.get('src'), pkt.get('dst'), pkt.get('dport'))
            if key not in flows:
                flows[key] = []
            flows[key].append(pkt)
        
        for flow_packets in flows.values():
            if len(flow_packets) > 5:  # Flujos con suficientes paquetes
                feature = [
                    len(flow_packets),  # Número de paquetes
                    np.mean([p.get('length', 0) for p in flow_packets]),  # Tamaño promedio
                    np.std([p.get('length', 0) for p in flow_packets]),  # Desviación
                    len(set([p.get('sport', 0) for p in flow_packets]))  # Puertos fuente únicos
                ]
                features.append(feature)
        
        return np.array(features) if features else np.array([])
    
    def detect_ddos(self, packets, time_window=1.0):
        """Detecta posible ataque DDoS basado en frecuencia"""
        if not packets:
            return []
        
        # Calcular paquetes por segundo
        if len(packets) > 1:
            times = [p.get('time', 0) for p in packets]
            duration = max(times) - min(times)
            if duration > 0:
                pps = len(packets) / duration
                if pps > self.threshold:
                    print(f"⚠️ ALERTA DDoS: {pps:.2f} paquetes/segundo")
                    return packets  # Todos los paquetes son sospechosos
        
        # Usar Isolation Forest para detectar flujos anómalos
        features = self.extract_flow_features(packets)
        if len(features) > 0:
            self.model.fit(features)
            predictions = self.model.predict(features)
            return [p for p, pred in zip(packets, predictions) if pred == -1]
        
        return []

class TrafficClassifier:
    """Clasificador de tráfico por tipo de aplicación"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.protocol_map = {
            80: 'HTTP', 443: 'HTTPS', 53: 'DNS', 22: 'SSH',
            21: 'FTP', 25: 'SMTP', 3306: 'MySQL', 5432: 'PostgreSQL',
            6379: 'Redis', 27017: 'MongoDB'
        }
    
    def train(self, packets_with_labels):
        """Entrena el clasificador con datos etiquetados"""
        features = []
        labels = []
        
        for packet, label in packets_with_labels:
            feat = self._extract_classification_features(packet)
            features.append(feat)
            labels.append(label)
        
        if features:
            self.model.fit(features, labels)
            self.is_trained = True
            print("✅ Clasificador de tráfico entrenado")
    
    def classify(self, packet):
        """Clasifica un paquete individual"""
        # Clasificación simple por puerto primero
        dport = packet.get('dport', 0)
        if dport in self.protocol_map:
            return self.protocol_map[dport], 0.9
        
        # Si hay modelo entrenado, usarlo
        if self.is_trained:
            features = self._extract_classification_features(packet)
            proba = self.model.predict_proba([features])[0]
            class_idx = np.argmax(proba)
            return self.model.classes_[class_idx], max(proba)
        
        return 'Unknown', 0.0
    
    def _extract_classification_features(self, packet):
        """Extrae características para clasificación"""
        return [
            packet.get('length', 0),
            packet.get('sport', 0),
            packet.get('dport', 0),
            packet.get('protocol', 0),
            1 if packet.get('flags', {}).get('SYN', False) else 0,
            1 if packet.get('flags', {}).get('ACK', False) else 0,
        ]

class NetworkAnomalyDetector:
    """Detector completo de anomalías multicapa"""
    
    def __init__(self):
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.dbscan = DBSCAN(eps=0.5, min_samples=10)
        self.ddos_detector = DDoSDetector()
        self.classifier = TrafficClassifier()
        
    def detect_all(self, packets):
        """Ejecuta todos los detectores y consolida resultados"""
        results = {
            'anomalies': [],
            'ddos_alert': False,
            'classified_traffic': {},
            'statistics': {}
        }
        
        # 1. Detección básica con Isolation Forest
        if len(packets) > 10:
            features = self._extract_basic_features(packets)
            if len(features) > 0:
                predictions = self.isolation_forest.fit_predict(features)
                results['anomalies'] = [p for p, pred in zip(packets, predictions) if pred == -1]
        
        # 2. Detección DDoS
        ddos_packets = self.ddos_detector.detect_ddos(packets)
        if ddos_packets:
            results['ddos_alert'] = True
            results['anomalies'].extend(ddos_packets)
        
        # 3. Clasificación de tráfico
        for packet in packets[:50]:  # Limitar para rendimiento
            protocol, confidence = self.classifier.classify(packet)
            results['classified_traffic'][protocol] = results['classified_traffic'].get(protocol, 0) + 1
        
        # 4. Estadísticas
        results['statistics'] = {
            'total_packets': len(packets),
            'unique_sources': len(set(p.get('src') for p in packets if p.get('src'))),
            'unique_destinations': len(set(p.get('dst') for p in packets if p.get('dst'))),
            'protocol_distribution': Counter(str(p.get('protocol', 0)) for p in packets)
        }
        
        return results
    
    def _extract_basic_features(self, packets):
        """Extrae características básicas para detección"""
        features = []
        for pkt in packets:
            features.append([
                pkt.get('length', 0),
                pkt.get('sport', 0) % 1000,  # Normalizar
                pkt.get('dport', 0) % 1000,
                pkt.get('time', 0) % 1.0
            ])
        return np.array(features)
