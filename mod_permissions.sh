#!/bin/bash
# Ensure we’re running as root
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root (e.g., using sudo)."
  exit 1
fi
# 33 is the traditional www-data's UserID

mkdir -p media static
chown -R 33:33 celerybeat-schedule media scripts
chown -R 33:33 static
chown 33:33 static_files
chown 33:33 static_files/css
chmod 775 static_files static_files/css
