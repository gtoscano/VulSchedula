#!/bin/bash

set -a
source variables.env
set +a

# Check if CURRENT_USER is set
if [ -z "$CURRENT_USER" ]; then
  echo "CURRENT_USER is not set in variables.env"
  exit 1
fi

# Detect OS
OS="$(uname -s)"

case "$OS" in
  MINGW*|MSYS*|CYGWIN*|Windows_NT)
    PLATFORM="windows"
    ;;
  Darwin)
    PLATFORM="mac"
    ;;
  *)
    PLATFORM="linux"
    ;;
esac

echo "Detected platform: ${PLATFORM}"

# Create required directories and files on the host
mkdir -p media static node_modules home .celery data log
[ -f package-lock.json ] && rm package-lock.json
[ -f static_files/css/daisyui.css ] && rm static_files/css/daisyui.css
touch package-lock.json

if [ "$PLATFORM" = "windows" ]; then
  # Windows: run permission changes inside the Docker container
  # since Windows has no native chown/chmod support.
  echo "Running permission fixes inside Docker container..."

  SERVICE_NAME="${DOCKER_SERVICE_NAME:-web}"

  docker compose run --rm --no-deps "$SERVICE_NAME" bash -c "
    chown -R www-data:www-data package.json package-lock.json media node_modules home .celery static data log
    chown ${CURRENT_USER}:www-data static_files static_files/css 2>/dev/null || \
      chown www-data:www-data static_files static_files/css
    chmod 775 static_files static_files/css
  "
else
  # Ensure we’re running as root on Linux/Mac
  if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root (e.g., using sudo)."
    exit 1
  fi

  if [ "$PLATFORM" = "mac" ]; then
    WEB_USER="$CURRENT_USER"
    WEB_GROUP="staff"
  else
    WEB_USER="www-data"
    WEB_GROUP="www-data"
  fi

  echo "Using web user:group -> ${WEB_USER}:${WEB_GROUP}"

  # Apply correct ownership
  chown -R "$WEB_USER":"$WEB_GROUP" package.json package-lock.json media node_modules home .celery data log
  chown -R "$WEB_USER":"$WEB_GROUP" static

  # static_files belongs to CURRENT_USER + web group (staff on mac)
  chown "$CURRENT_USER":"$WEB_GROUP" static_files
  chown "$CURRENT_USER":"$WEB_GROUP" static_files/css

  chmod 775 static_files static_files/css
fi
