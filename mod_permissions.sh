#!/bin/bash
set -e

# Ensure we’re running as root
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root (e.g., using sudo)." >&2
  exit 1
fi

# Create directories if they don’t exist
mkdir -p media static

# Ownership
chown -R 33:33 celerybeat-schedule media scripts static
chown 33:33 static_files static_files/css

# Default permissions for the other dirs
chmod 775 static_files static_files/css

# macOS-only tweak
if [[ "$(uname)" == "Darwin" ]]; then
  # Grant wide-open permissions on “static” so the built-in macOS web stack
  # (or Docker-for-Mac volume mounts) can write to it without UID/GID mismatch
  chmod 777 static
fi
