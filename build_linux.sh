#!/bin/bash

# Ensure virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
  echo "يرجى تنشيط البيئة الافتراضية أولاً (source venv/bin/activate)"
  exit 1
fi

APP_NAME="HD_RAM_CPU_Alarm"
DISPLAY_NAME="HD RAM CPU Alarm"

echo "جاري تجميع الكود لنسخة لينكس مستقلة (Linux Binary)..."
pyinstaller --noconfirm --onefile --windowed --name "$APP_NAME" main.py

echo "جاري تجهيز حزمة دبيان (DEB)..."
mkdir -p deb_package/DEBIAN
mkdir -p deb_package/usr/local/bin
mkdir -p deb_package/usr/share/applications
mkdir -p deb_package/usr/share/pixmaps

# Copy executable
cp "dist/$APP_NAME" deb_package/usr/local/bin/

# Create control file
cat <<EOT > deb_package/DEBIAN/control
Package: hd-ram-cpu-alarm
Version: 1.1
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Atef Ment <atef@example.com>
Description: A professional CPU, RAM, and Disk monitor with Temperature tracking.
 Professional dashboard for real-time system monitoring.
EOT

# Create Desktop Entry
cat <<EOT > deb_package/usr/share/applications/hd-ram-cpu-alarm.desktop
[Desktop Entry]
Name=$DISPLAY_NAME
Comment=Monitor CPU, RAM, Disk and Temperature
Exec=/usr/local/bin/$APP_NAME
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Utility;
Keywords=monitor;cpu;ram;disk;temperature;
StartupNotify=true
EOT

# Build Debian Package
dpkg-deb --build deb_package "${APP_NAME}_1.1_amd64.deb"

echo "تم بنجاح! تم إنشاء الحزمة: ${APP_NAME}_1.1_amd64.deb"
