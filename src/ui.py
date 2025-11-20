# src/ui.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.weather import get_weather
from src.system_monitor import get_system_status

console = Console()

def print_header():
    """Print application header"""
    console.print(Panel(
        "[bold magenta]🚀 Debian Embedded Assistant (DEA)[/bold magenta]\n"
        "[dim]Voice & Text Task Manager for Debian 12[/dim]",
        title="[bold cyan]Welcome[/bold cyan]",
        border_style="magenta"
    ))

def print_weather():
    """Display weather information"""
    weather = get_weather()
    console.print(Panel(
        f"[blue]{weather}[/blue]",
        title="Weather",
        border_style="blue"
    ))

def print_system_status():
    """Display system status"""
    status = get_system_status()
    table = Table(title="🔧 System Status", show_header=False)
    table.add_column("Metric", style="cyan", width=15)
    table.add_column("Value", style="magenta")

    table.add_row("CPU", f"{status['cpu']:.1f}%")
    table.add_row("Memory", status['memory'])
    table.add_row("Battery", status['battery'])
    table.add_row("Disk", status['disk'])
    table.add_row("Brightness", status['brightness'])

    console.print(table)

def print_menu():
    """Print available commands"""
    console.print("\n[bold cyan]Available Commands:[/bold cyan]")
    commands = [
        ("dictation", "Record voice input and add as task"),
        ("show tasks", "List all tasks"),
        ("add task [text]", "Add a task manually"),
        ("say [text]", "Test text-to-speech"),
        ("test piper", "Test Piper TTS specifically"),
        ("test espeak", "Test espeak TTS specifically"),
        ("download voice", "Download Piper voice model"),
        ("volume up/down", "Adjust system volume"),
        ("brightness up/down", "Adjust screen brightness"),
        ("mute/unmute", "Mute/unmute audio"),
        ("weather", "Show current weather"),
        ("status", "Show system status"),
        ("notes", "Open notes editor"),
        ("calendar", "Show calendar"),
        ("help", "Show this menu"),
        ("exit", "Quit assistant")
    ]

    for cmd, desc in commands:
        console.print(f"  [green]{cmd:20s}[/green] → {desc}")
