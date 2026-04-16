from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt

class CircularProgress(QWidget):
    def __init__(self, title, color, parent=None):
        super().__init__(parent)
        self.title = title
        self.value = 0
        self.color = color
        self.setMinimumSize(100, 100)

    def set_value(self, val):
        self.value = val
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
        size = min(width, height) - 20
        x = (width - size) / 2
        y = (height - size) / 2

        # Draw background circle
        painter.setPen(QPen(QColor(50, 50, 50), 10, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(int(x), int(y), int(size), int(size), 0, 360 * 16)

        # Draw progress circle
        painter.setPen(QPen(self.color, 10, Qt.SolidLine, Qt.RoundCap))
        # angle goes from 0 to 360*16 (in 1/16ths of a degree)
        span_angle = int(-self.value * 3.6 * 16)
        painter.drawArc(int(x), int(y), int(size), int(size), 90 * 16, span_angle)

        # Draw text
        painter.setPen(QColor(200, 200, 200))
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(int(x), int(y), int(size), int(size) - 20, Qt.AlignCenter, f"{self.value:.1f}%")

        painter.setFont(QFont("Arial", 10))
        painter.drawText(int(x), int(y) + 20, int(size), int(size), Qt.AlignCenter, self.title)


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # Adding a background frame
        self.bg_widget = QWidget()
        self.bg_widget.setStyleSheet("background-color: rgba(30,30,30, 200); border-radius: 15px;")
        bg_layout = QHBoxLayout(self.bg_widget)
        
        self.cpu_progress = CircularProgress("CPU", QColor("#00ff00"))
        self.ram_progress = CircularProgress("RAM", QColor("#00ff00"))
        self.disk_progress = CircularProgress("DISK", QColor("#00ff00"))

        bg_layout.addWidget(self.cpu_progress)
        bg_layout.addWidget(self.ram_progress)
        bg_layout.addWidget(self.disk_progress)

        layout.addWidget(self.bg_widget)
        self.resize(350, 150)
        
    def update_metrics(self, cpu, ram, disk, config):
        self._update_widget(self.cpu_progress, cpu, config["cpu_threshold"])
        self._update_widget(self.ram_progress, ram, config["ram_threshold"])
        self._update_widget(self.disk_progress, disk, config["disk_threshold"])

    def _update_widget(self, widget, value, threshold):
        widget.set_value(value)
        if value >= threshold:
            widget.set_color(QColor("#ff0000")) # Red
        elif value >= threshold * 0.8:
            widget.set_color(QColor("#ffa500")) # Orange
        else:
            widget.set_color(QColor("#00ff00")) # Green

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
