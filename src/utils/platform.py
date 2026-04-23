"""Utilidades multiplataforma"""
import platform
import sys

def get_platform():
    """Detecta el sistema operativo"""
    system = platform.system().lower()
    if system == 'windows':
        return 'windows'
    elif system == 'linux':
        return 'linux'
    else:
        return 'other'

def check_dependencies():
    """Verifica dependencias específicas por plataforma"""
    plat = get_platform()
    
    if plat == 'windows':
        print("⚠️  Windows detectado - Asegúrate de tener Npcap instalado")
        print("   Descarga desde: https://npcap.com")
    elif plat == 'linux':
        print("✅ Linux detectado - Verificando libpcap...")
        # Aquí iría verificación de libpcap
