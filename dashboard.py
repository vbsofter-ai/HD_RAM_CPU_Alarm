import os
import getpass
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt

class CircularProgress(QWidget):
    def __init__(self, title, color, parent=None):
        super().__init__(parent)
        self.title = title
        self.value = 0
        self.color = color
        self.used_str = ""
        self.free_str = ""
        self.total_str = ""
        self.temp_str = "N/A"
        self.setMinimumSize(110, 160)

    def set_data(self, val, used, free, total, temp):
        self.value = val
        self.used_str = used
        self.free_str = free
        self.total_str = total
        self.temp_str = temp
        self.update()

    def set_color(self, color):
        self.color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        width = rect.width()
        height = rect.height()
        
        # Draw Circle
        size = min(width, height - 70) - 10
        x = (width - size) / 2
        y = 5

        # Background Arc
        painter.setPen(QPen(QColor(40, 40, 40), 7, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(int(x), int(y), int(size), int(size), 0, 360 * 16)

        # Progress Arc
        painter.setPen(QPen(self.color, 7, Qt.SolidLine, Qt.RoundCap))
        span_angle = int(-self.value * 3.6 * 16)
        painter.drawArc(int(x), int(y), int(size), int(size), 90 * 16, span_angle)

        # Percentage Text
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(int(x), int(y), int(size), int(size), Qt.AlignCenter, f"{self.value:.0f}%")

        # Title
        painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
        painter.setPen(self.color)
        painter.drawText(0, int(y + size + 4), width, 16, Qt.AlignCenter, self.title)

        # Details
        painter.setFont(QFont("Segoe UI", 7))
        painter.setPen(QColor(200, 200, 200))
        
        offset = int(y + size + 22)
        painter.drawText(0, offset, width, 12, Qt.AlignCenter, f"المستخدم: {self.used_str}")
        painter.drawText(0, offset + 12, width, 12, Qt.AlignCenter, f"المتاح: {self.free_str}")
        painter.drawText(0, offset + 24, width, 12, Qt.AlignCenter, f"الإجمالي: {self.total_str}")
        
        # Temp
        painter.setPen(QColor("#FFA500") if self.temp_str != "N/A" else QColor(100, 100, 100))
        painter.setFont(QFont("Segoe UI", 8, QFont.Bold))
        painter.drawText(0, offset + 38, width, 14, Qt.AlignCenter, f"🌡 {self.temp_str}")


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        # Adding a background frame
        self.bg_widget = QWidget()
        self.bg_widget.setStyleSheet("background-color: rgba(25,25,25, 240); border-radius: 12px; border: 1px solid #333;")
        self.bg_layout = QHBoxLayout(self.bg_widget)
        self.bg_layout.setContentsMargins(10, 10, 10, 10)
        
        self.cpu_progress = CircularProgress("CPU", QColor("#00ff00"))
        self.ram_progress = CircularProgress("RAM", QColor("#00ff00"))
        self.disk_progress = CircularProgress("DISK", QColor("#00ff00"))

        self.bg_layout.addWidget(self.cpu_progress)
        self.bg_layout.addWidget(self.ram_progress)
        self.bg_layout.addWidget(self.disk_progress)
        
        main_layout.addWidget(self.bg_widget)
        self.resize(360, 200) # Increased height and width
        
    def update_metrics(self, stats, config):
        self._update_widget(self.cpu_progress, stats["cpu"], config["cpu_threshold"])
        self._update_widget(self.ram_progress, stats["ram"], config["ram_threshold"])
        self._update_widget(self.disk_progress, stats["disk"], config["disk_threshold"])

    def _update_widget(self, widget, data, threshold):
        value = data["percent"]
        widget.set_data(value, data["used"], data["free"], data.get("total", "N/A"), data["temp"])
        
        if value >= threshold:
            widget.set_color(QColor("#ff4444")) # Red
        elif value >= threshold * 0.8:
            widget.set_color(QColor("#ffaa00")) # Orange
        else:
            widget.set_color(QColor("#00ff66")) # Green

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
