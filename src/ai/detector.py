"""Módulo de detección de anomalías con IA"""
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def extract_features(self, packets):
        """Extrae características numéricas de los paquetes"""
        features = []
        for pkt in packets:
            feature = [
                pkt.get('length', 0),
                pkt.get('sport', 0),
                pkt.get('dport', 0),
                pkt.get('time', 0)
            ]
            features.append(feature)
        return np.array(features)
    
    def train(self, packets):
        """Entrena el modelo con tráfico normal"""
        features = self.extract_features(packets)
        features_scaled = self.scaler.fit_transform(features)
        self.model.fit(features_scaled)
        self.is_trained = True
        print("✅ Modelo entrenado correctamente")
        
    def detect(self, packets):
        """Detecta anomalías en nuevos paquetes"""
        if not self.is_trained:
            raise Exception("El modelo no ha sido entrenado")
            
        features = self.extract_features(packets)
        features_scaled = self.scaler.transform(features)
        predictions = self.model.predict(features_scaled)
        
        # -1 = anomalía, 1 = normal
        anomalies = [pkt for pkt, pred in zip(packets, predictions) if pred == -1]
        return anomalies
