import psutil
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class SystemMonitor(QObject):
    updated = pyqtSignal(dict) # Now emits a dict with detailed data

    def __init__(self, interval=1000):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_usage)
        self.timer.start(interval)

    def _format_size(self, bytes):
        """Turn bytes into a human readable string like 4.2 GB or 500 MB."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024 or unit == 'TB':
                return f"{bytes:.1f} {unit}"
            bytes /= 1024

    def fetch_usage(self):
        # CPU
        cpu_used = psutil.cpu_percent(interval=None)
        
        # RAM
        ram_data = psutil.virtual_memory()
        
        # Disk
        disk_data = psutil.disk_usage('/')
        
        # Temperatures
        temps = psutil.sensors_temperatures()
        cpu_temp = "N/A"
        ram_temp = "N/A"
        disk_temp = "N/A" # Default

        # Try to get CPU temp
        if 'coretemp' in temps and temps['coretemp']:
            cpu_temp = f"{temps['coretemp'][0].current:.1f}°C"
        elif 'dell_ddv' in temps: # Fallback for Dell
            for t in temps['dell_ddv']:
                if t.label == 'CPU':
                    cpu_temp = f"{t.current:.1f}°C"
                    break

        # Try to get RAM temp (Specific for Dell SODIMM)
        if 'dell_ddv' in temps:
            for t in temps['dell_ddv']:
                if t.label == 'SODIMM':
                    ram_temp = f"{t.current:.1f}°C"
                    break

        stats = {
            "cpu": {
                "percent": cpu_used,
                "used": f"{cpu_used:.1f}%",
                "free": f"{100-cpu_used:.1f}%",
                "temp": cpu_temp
            },
            "ram": {
                "percent": ram_data.percent,
                "used": self._format_size(ram_data.used),
                "free": self._format_size(ram_data.available),
                "total": self._format_size(ram_data.total),
                "temp": ram_temp
            },
            "disk": {
                "percent": disk_data.percent,
                "used": self._format_size(disk_data.used),
                "free": self._format_size(disk_data.free),
                "total": self._format_size(disk_data.total),
                "temp": disk_temp
            }
        }
        self.updated.emit(stats)

    def set_interval(self, interval):
        self.timer.setInterval(interval)
