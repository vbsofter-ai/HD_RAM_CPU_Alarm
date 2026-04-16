import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import QTimer

import config as cfg
from monitor import SystemMonitor
from dashboard import Dashboard
from settings import SettingsDialog

class AppControl:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.config = cfg.load_config()

        self.dashboard = Dashboard()
        self.dashboard.show()

        self.monitor = SystemMonitor(self.config["update_interval_ms"])
        self.monitor.updated.connect(self.on_metrics_updated)

        self.setup_tray()
        self.last_warning_time = 0

    def setup_tray(self):
        self.tray = QSystemTrayIcon()
        
        # Create a simple icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("transparent"))
        painter = QPainter(pixmap)
        painter.setBrush(QColor("#00ff00"))
        painter.drawEllipse(2, 2, 28, 28)
        painter.end()
        icon = QIcon(pixmap)
        
        self.tray.setIcon(icon)
        self.tray.setVisible(True)

        menu = QMenu()
        
        toggle_dash_action = QAction("إظهار/إخفاء اللوحة - Show/Hide Dashboard", self.app)
        toggle_dash_action.triggered.connect(self.toggle_dashboard)
        menu.addAction(toggle_dash_action)

        settings_action = QAction("الإعدادات - Settings", self.app)
        settings_action.triggered.connect(self.open_settings)
        menu.addAction(settings_action)

        quit_action = QAction("خروج - Quit", self.app)
        quit_action.triggered.connect(self.app.quit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)

    def toggle_dashboard(self):
        if self.dashboard.isVisible():
            self.dashboard.hide()
        else:
            self.dashboard.show()

    def open_settings(self):
        dialog = SettingsDialog()
        if dialog.exec_():
            self.config = cfg.load_config()
            self.monitor.set_interval(self.config["update_interval_ms"])

    def on_metrics_updated(self, cpu, ram, disk):
        self.dashboard.update_metrics(cpu, ram, disk, self.config)
        
        if self.config["notifications_enabled"]:
            warnings = []
            if cpu >= self.config["cpu_threshold"]:
                warnings.append(f"CPU: {cpu:.1f}%")
            if ram >= self.config["ram_threshold"]:
                warnings.append(f"RAM: {ram:.1f}%")
            if disk >= self.config["disk_threshold"]:
                warnings.append(f"Disk: {disk:.1f}%")

            if warnings:
                self.show_notification(warnings)

    def show_notification(self, warnings):
        current_time = time.time()
        # limit to 1 warning per 30 seconds to avoid spam
        if current_time - self.last_warning_time > 30:
            message = "الاستهلاك مرتفع! - High Usage!\n" + "\n".join(warnings)
            os.system(f'notify-send "تنبيه النظام - System Warning" "{message}" -u critical')
            self.last_warning_time = current_time

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app_control = AppControl()
    app_control.run()
