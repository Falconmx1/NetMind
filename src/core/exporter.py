"""Módulo para exportar resultados a JSON y CSV"""
import json
import csv
import os
from datetime import datetime
from pathlib import Path

class ExportManager:
    def __init__(self, output_dir="exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def export_json(self, data, filename=None):
        """Exporta datos a formato JSON"""
        if filename is None:
            filename = f"netmind_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.output_dir / filename
        
        # Convertir datos a formato serializable
        serializable_data = self._make_serializable(data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Datos exportados a JSON: {filepath}")
        return str(filepath)
    
    def export_csv(self, data, filename=None):
        """Exporta datos a formato CSV"""
        if filename is None:
            filename = f"netmind_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = self.output_dir / filename
        
        if not data:
            print("⚠️ No hay datos para exportar")
            return None
            
        # Obtener todas las claves posibles
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                # Limpiar datos no serializables
                clean_item = {k: str(v) if not isinstance(v, (str, int, float, bool)) else v 
                             for k, v in item.items()}
                writer.writerow(clean_item)
        
        print(f"✅ Datos exportados a CSV: {filepath}")
        return str(filepath)
    
    def export_report(self, packets, anomalies, stats):
        """Exporta un reporte completo con todos los datos"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        report = {
            'metadata': {
                'timestamp': timestamp,
                'total_packets': len(packets),
                'anomalies_detected': len(anomalies),
                'anomaly_percentage': (len(anomalies) / len(packets) * 100) if packets else 0
            },
            'statistics': stats,
            'anomalies': anomalies,
            'all_packets': packets[:100]  # Limitar a 100 para no hacer archivo enorme
        }
        
        # Exportar JSON
        json_file = self.export_json(report, f"report_{timestamp}.json")
        
        # Exportar anomalías a CSV
        if anomalies:
            csv_file = self.export_csv(anomalies, f"anomalies_{timestamp}.csv")
        
        return {'json': json_file, 'csv': csv_file if anomalies else None}
    
    def _make_serializable(self, obj):
        """Convierte objetos no serializables a tipos serializables"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, (datetime,)):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return str(obj)
        else:
            return obj
