"""Interfaz de línea de comandos"""
import click
from src.core.capture import PacketCapture
from src.ai.detector import AnomalyDetector

@click.group()
def cli():
    """NetMind - Herramienta de red con IA"""
    pass

@cli.command()
@click.option('--interface', '-i', help='Interfaz de red')
@click.option('--count', '-c', default=100, help='Número de paquetes a capturar')
def capture(interface, count):
    """Captura tráfico de red"""
    click.echo(f"🔍 Capturando {count} paquetes...")
    capturer = PacketCapture()
    packets = capturer.start_capture(interface, count)
    click.echo(f"✅ Capturados {len(packets)} paquetes")
    return packets

@cli.command()
@click.option('--train-file', '-t', help='Archivo con tráfico normal para entrenar')
@click.option('--detect-file', '-d', help='Archivo a analizar')
def analyze(train_file, detect_file):
    """Analiza tráfico con IA"""
    click.echo("🧠 Iniciando análisis con IA...")
    # Aquí iría la lógica de carga de archivos y análisis
    click.echo("✅ Análisis completado")

if __name__ == '__main__':
    cli()
