# Agregar al final del archivo cli.py, antes del if __name__

@cli.command()
def dashboard():
    """Inicia el dashboard web"""
    from src.ui.dashboard import DashboardServer
    click.echo("🌐 Iniciando dashboard web...")
    server = DashboardServer()
    server.start()
    click.echo("Presiona Ctrl+C para detener")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\n✅ Dashboard detenido")

@cli.command()
@click.option('--input', '-i', help='Archivo de paquetes (JSON/CSV)')
@click.option('--format', '-f', type=click.Choice(['json', 'csv']), default='json')
def export(input, format):
    """Exporta análisis a JSON/CSV"""
    # Lógica de exportación
    click.echo(f"📁 Exportando a {format}...")

@cli.command()
def gui():
    """Inicia la interfaz gráfica"""
    from src.ui.gui import NetMindGUI
    click.echo("🖥️ Iniciando interfaz gráfica...")
    app = NetMindGUI()
    app.run()
