#!/bin/bash
# Ensure we’re running as root
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root (e.g., using sudo)."
  exit 1
fi

chown -R www-data:www-data celerybeat-schedule media scripts
chown -R www-data:www-data static
chown gtoscano:www-data static_files
chown gtoscano:www-data static_files/css
chmod 775 static_files static_files/css
