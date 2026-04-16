from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox, QPushButton, QFormLayout
from PyQt5.QtCore import Qt
import config as cfg

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("الإعدادات - Settings")
        self.resize(300, 200)
        self.config = cfg.load_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        # CPU Threshold
        self.cpu_slider = self._create_slider(self.config["cpu_threshold"])
        form_layout.addRow(QLabel("CPU Threshold %:"), self.cpu_slider)

        # RAM Threshold
        self.ram_slider = self._create_slider(self.config["ram_threshold"])
        form_layout.addRow(QLabel("RAM Threshold %:"), self.ram_slider)

        # Disk Threshold
        self.disk_slider = self._create_slider(self.config["disk_threshold"])
        form_layout.addRow(QLabel("Disk Threshold %:"), self.disk_slider)

        # Notifications
        self.notif_checkbox = QCheckBox("Enable Notifications")
        self.notif_checkbox.setChecked(self.config["notifications_enabled"])
        form_layout.addRow(QLabel("Notifications:"), self.notif_checkbox)

        layout.addLayout(form_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _create_slider(self, value):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(10)
        slider.setMaximum(100)
        slider.setValue(value)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        return slider

    def save_settings(self):
        self.config["cpu_threshold"] = self.cpu_slider.value()
        self.config["ram_threshold"] = self.ram_slider.value()
        self.config["disk_threshold"] = self.disk_slider.value()
        self.config["notifications_enabled"] = self.notif_checkbox.isChecked()
        cfg.save_config(self.config)
        self.accept()
