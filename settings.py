from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox, 
    QPushButton, QFormLayout, QGroupBox, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import config as cfg

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("الإعدادات - Settings")
        self.setMinimumWidth(350)
        self.config = cfg.load_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Title
        title = QLabel("إعدادات التنبيهات - Alert Thresholds")
        title_font = QFont("Arial", 12, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Group box for professional look
        group_box = QGroupBox("مستويات التحذير (Thresholds %)")
        group_layout = QFormLayout()
        group_layout.setSpacing(15)

        # CPU
        self.cpu_label = QLabel(f"{self.config['cpu_threshold']}%")
        self.cpu_slider = self._create_slider(self.config["cpu_threshold"], self.cpu_label)
        cpu_row = QHBoxLayout()
        cpu_row.addWidget(self.cpu_slider)
        cpu_row.addWidget(self.cpu_label)
        group_layout.addRow(QLabel("CPU:"), cpu_row)

        # RAM
        self.ram_label = QLabel(f"{self.config['ram_threshold']}%")
        self.ram_slider = self._create_slider(self.config["ram_threshold"], self.ram_label)
        ram_row = QHBoxLayout()
        ram_row.addWidget(self.ram_slider)
        ram_row.addWidget(self.ram_label)
        group_layout.addRow(QLabel("RAM:"), ram_row)

        # Disk
        self.disk_label = QLabel(f"{self.config['disk_threshold']}%")
        self.disk_slider = self._create_slider(self.config["disk_threshold"], self.disk_label)
        disk_row = QHBoxLayout()
        disk_row.addWidget(self.disk_slider)
        disk_row.addWidget(self.disk_label)
        group_layout.addRow(QLabel("Disk:"), disk_row)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        # Settings
        self.notif_checkbox = QCheckBox("تفعيل اشعارات سطح المكتب (Enable Notifications)")
        self.notif_checkbox.setChecked(self.config.get("notifications_enabled", True))
        layout.addWidget(self.notif_checkbox)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("حفظ (Save)")
        save_btn.setStyleSheet("padding: 8px; font-weight: bold; background-color: #2e8b57; color: white; border-radius: 4px;")
        save_btn.clicked.connect(self.save_settings)
        
        cancel_btn = QPushButton("إلغاء (Cancel)")
        cancel_btn.setStyleSheet("padding: 8px; border: 1px solid #aaa; border-radius: 4px;")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _create_slider(self, value, label_widget):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(10)
        slider.setMaximum(100)
        slider.setValue(value)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        slider.valueChanged.connect(lambda val: label_widget.setText(f"{val}%"))
        return slider

    def save_settings(self):
        self.config["cpu_threshold"] = self.cpu_slider.value()
        self.config["ram_threshold"] = self.ram_slider.value()
        self.config["disk_threshold"] = self.disk_slider.value()
        self.config["notifications_enabled"] = self.notif_checkbox.isChecked()
        cfg.save_config(self.config)
        self.accept()
