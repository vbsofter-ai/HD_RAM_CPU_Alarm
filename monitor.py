import psutil
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class SystemMonitor(QObject):
    updated = pyqtSignal(float, float, float) # cpu, ram, disk

    def __init__(self, interval=1000):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_usage)
        self.timer.start(interval)

    def fetch_usage(self):
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        self.updated.emit(cpu, ram, disk)

    def set_interval(self, interval):
        self.timer.setInterval(interval)
