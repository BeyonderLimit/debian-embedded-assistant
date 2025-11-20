# src/system_monitor.py
import psutil
import subprocess
from rich.console import Console

console = Console()

def get_cpu_usage():
    """Get CPU usage percentage"""
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """Get memory usage"""
    mem = psutil.virtual_memory()
    return {
        "percent": mem.percent,
        "used_gb": mem.used / (1024**3),
        "total_gb": mem.total / (1024**3)
    }

def get_battery():
    """Get battery status"""
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "charging": battery.power_plugged,
                "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
            }
    except:
        pass
    return None

def get_disk_usage():
    """Get disk usage"""
    disk = psutil.disk_usage("/")
    return {
        "percent": disk.percent,
        "used_gb": disk.used / (1024**3),
        "total_gb": disk.total / (1024**3)
    }

def get_brightness():
    """Get screen brightness (if available)"""
    try:
        # Try multiple methods
        methods = [
            "xbacklight -get",
            "brightnessctl g",
            "cat /sys/class/backlight/*/brightness 2>/dev/null | head -n1"
        ]
        for method in methods:
            try:
                result = subprocess.run(
                    method,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except:
                continue
    except:
        pass
    return "N/A"

def get_system_status():
    """Get comprehensive system status"""
    mem = get_memory_usage()
    disk = get_disk_usage()
    battery = get_battery()

    return {
        "cpu": get_cpu_usage(),
        "memory": f"{mem['percent']:.1f}% ({mem['used_gb']:.1f}/{mem['total_gb']:.1f} GB)",
        "battery": f"{battery['percent']}% ({'Charging' if battery['charging'] else 'Discharging'})" if battery else "N/A",
        "disk": f"{disk['percent']:.1f}% ({disk['used_gb']:.1f}/{disk['total_gb']:.1f} GB)",
        "brightness": get_brightness()
    }
