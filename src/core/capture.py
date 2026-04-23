"""Módulo de captura de paquetes multiplataforma"""
from scapy.all import sniff, IP, TCP, UDP
import time

class PacketCapture:
    def __init__(self):
        self.packets = []
        
    def packet_callback(self, packet):
        """Procesa cada paquete capturado"""
        if IP in packet:
            packet_info = {
                'src': packet[IP].src,
                'dst': packet[IP].dst,
                'protocol': packet[IP].proto,
                'time': time.time(),
                'length': len(packet)
            }
            
            if TCP in packet:
                packet_info['sport'] = packet[TCP].sport
                packet_info['dport'] = packet[TCP].dport
            elif UDP in packet:
                packet_info['sport'] = packet[UDP].sport
                packet_info['dport'] = packet[UDP].dport
                
            self.packets.append(packet_info)
            print(f"Capturado: {packet_info['src']} -> {packet_info['dst']} ({packet_info['length']} bytes)")
    
    def start_capture(self, interface=None, count=100):
        """Inicia la captura de paquetes"""
        print(f"Iniciando captura en {interface or 'todas las interfaces'}...")
        sniff(iface=interface, prn=self.packet_callback, count=count)
        return self.packets
