#!/bin/bash

# Ensure we’re running as root
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root (e.g., using sudo)."
  exit 1
fi

set -a
source variables.env
set +a

# Check if CURRENT_USER is set
if [ -z "$CURRENT_USER" ]; then
  echo "CURRENT_USER is not set in variables.env"
  exit 1
fi

if [[ "$(uname)" == "Darwin" ]]; then
  WEB_USER="$CURRENT_USER"
  WEB_GROUP="staff"
else
  WEB_USER="www-data"
  WEB_GROUP="www-data"
fi

echo "Using web user:group -> ${WEB_USER}:${WEB_GROUP}"

mkdir -p media static
if [ -f package-lock.json ]; then
  rm package-lock.json
fi

if [ -f static_files/css/daisyui.css ]; then
  rm static_files/css/daisyui.css
fi

touch package-lock.json
mkdir -p node_modules home .celery

# Apply correct ownership
chown -R "$WEB_USER":"$WEB_GROUP" package.json package-lock.json media node_modules home .celery
chown -R "$WEB_USER":"$WEB_GROUP" static

# static_files belongs to CURRENT_USER + web group (staff on mac)
chown "$CURRENT_USER":"$WEB_GROUP" static_files
chown "$CURRENT_USER":"$WEB_GROUP" static_files/css

chmod 775 static_files static_files/css
