# HD_RAM_CPU_Alarm 🚨

[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-PyQt5-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey.svg)](#)

A professional system resource monitor for Linux (especially Linux Mint) and Windows. It provides real-time tracking of CPU, RAM, and Disk usage with customizable threshold alerts and desktop notifications.

---

## 🌍 اللغات المدعومة / Supported Languages
- **العربية**
- **English**

---

## ✨ المميزات (Features)

### 🇸🇦 العربية
- **مراقبة فورية**: عرض استهلاك المعالج (CPU)، الذاكرة العشوائية (RAM)، والهارد ديسك (Disk) بشكل دائري أنيق.
- **التنبيهات الذكية**: تغيير ألوان المؤشرات تلقائياً (أخضر -> برتقالي -> أحمر) بناءً على مستوى الاستهلاك.
- **مراقبة درجة الحرارة**: عرض درجات حرارة الأنوية (CPU) والرامات (RAM) في الوقت الفعلي.
- **إشعارات سطح المكتب**: إرسال تنبيهات عندما يتخطى الاستهلاك الحدود المسموح بها.
- **إعدادات متقدمة**: التحكم في مستويات التنبيه وفترة التحديث (ms).
- **سهولة الوصول**: أيقونة في شريط النظام (System Tray) للتحكم السريع والإخفاء/الإظهار.

### 🇺🇸 English
- **Real-time Monitoring**: Visual display of CPU, RAM, and Disk usage using sleek circular indicators.
- **Used vs Free**: Displays both "Used" (المستخدم) and "Free" (المحرر) capacity for all resources.
- **Temperature Monitoring**: Visualizes real-time core temperatures for CPU and RAM.
- **Smart Alerts**: Automatic indicator color changes (Green -> Orange -> Red) based on usage thresholds.
- **Desktop Notifications**: Instant alerts when resource usage exceeds predefined limits.
- **Advanced Settings**: Customize alert thresholds and update intervals (ms).
- **System Tray Integration**: Quick access via tray icon to toggle dashboard visibility or exit.
- **Identity Info**: Displays current User and Editor (Atef Ment) in the dashboard footer.

---

## 🚀 كيفية التشغيل (How to Run)

### 📋 المتطلبات (Requirements)
Make sure you have Python 3.12+ installed.

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd HD_RAM_CPU_Alarm
   ```

2. **Setup virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application**:
   ```bash
   python3 main.py
   ```

---

## 🛠️ بناء التطبيق (Building from Source)

### 🐧 Linux (Debian/Ubuntu/Mint)
To build a standalone binary and a `.deb` package:
1. Activate venv: `source venv/bin/activate`
2. Run the build script:
   ```bash
   chmod +x build_linux.sh
   ./build_linux.sh
   ```
*Result: An executable in `dist/` and a `.deb` package in the root folder.*

### 🪟 Windows
To build a standalone `.exe` file:
1. Run the batch file in Command Prompt or PowerShell:
   ```cmd
   build_windows.bat
   ```
*Result: A standalone `HD_RAM_CPU_Alarm.exe` in the `dist/` folder.*

---

## 👤 المطور والمحرر (Developer & Editor)
- **Editor (المحرر)**: Atef Ment
- **User (المستخدم)**: Dynamically detected from system.

---

## 📝 الترخيص (License)
This project is open-source and free to use.
