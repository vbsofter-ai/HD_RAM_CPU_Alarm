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
        disk_path = getattr(self, 'disk_path', '/')
        try:
            disk_data = psutil.disk_usage(disk_path)
        except:
            disk_data = psutil.disk_usage('/')
        
        # Temperatures
        temps = psutil.sensors_temperatures()
        cpu_temp = "N/A"
        ram_temp = "N/A"
        disk_temp = "N/A"

        # Improved logic for CPU temp
        for name, entries in temps.items():
            name_l = name.lower()
            if any(k in name_l for k in ['coretemp', 'cpu', 'pkg', 'soc', 'dell_ddv']):
                for entry in entries:
                    label_l = entry.label.lower()
                    if any(k in label_l for k in ['package', 'id 0', 'die', 'avg', 'cpu']) or not entry.label:
                        cpu_temp = f"{entry.current:.0f}°C"
                        break
                if cpu_temp != "N/A": break
        
        # Improved logic for RAM temp
        for name, entries in temps.items():
            for entry in entries:
                label_l = entry.label.lower()
                if any(k in label_l for k in ['sodimm', 'ram', 'dimm', 'mem']):
                    ram_temp = f"{entry.current:.0f}°C"
                    break
            if ram_temp != "N/A": break

        # Improved logic for Disk temp
        for name, entries in temps.items():
            name_l = name.lower()
            if any(k in name_l for k in ['nvme', 'ssd', 'disk', 'sata']):
                for entry in entries:
                    disk_temp = f"{entry.current:.0f}°C"
                    break
            if disk_temp != "N/A": break

        stats = {
            "cpu": {
                "percent": cpu_used,
                "used": f"{cpu_used:.0f}%",
                "free": f"{100-cpu_used:.0f}%",
                "total": f"{psutil.cpu_count()} Cores",
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
