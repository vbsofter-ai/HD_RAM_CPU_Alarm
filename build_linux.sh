#!/bin/bash

# Ensure virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
  echo "يرجى تنشيط البيئة الافتراضية أولاً (source venv/bin/activate)"
  exit 1
fi

echo "جاري تجميع الكود لنسخة لينكس مستقلة (Linux Binary)..."
pyinstaller --noconfirm --onefile --windowed --name "HD_RAM_CPU_Alarm" main.py

echo "جاري تجهيز حزمة دبيان (DEB)..."
mkdir -p deb_package/DEBIAN
mkdir -p deb_package/usr/local/bin
mkdir -p deb_package/usr/share/applications

# Copy executable
cp dist/HD_RAM_CPU_Alarm deb_package/usr/local/bin/

# Create control file
cat <<EOT > deb_package/DEBIAN/control
Package: hd-ram-cpu-alarm
Version: 1.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Developer
Description: A professional CPU, RAM, and Disk monitor for Linux Mint
EOT

# Create Desktop Entry
cat <<EOT > deb_package/usr/share/applications/hd-ram-cpu-alarm.desktop
[Desktop Entry]
Name=System Resource Alarm
Comment=Monitor CPU, RAM, and Disk
Exec=/usr/local/bin/HD_RAM_CPU_Alarm
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Utility;
EOT

# Build Debian Package
dpkg-deb --build deb_package "HD_RAM_CPU_Alarm_1.0_amd64.deb"

echo "تم بنجاح! تم إنشاء الحزمة: HD_RAM_CPU_Alarm_1.0_amd64.deb"
