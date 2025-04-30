#!/bin/bash
# Ensure we’re running as root
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root (e.g., using sudo)."
  exit 1
fi
# Get the Docker group ID
DOCKER_GID=$(getent group docker | cut -d: -f3)

# Add or update DOCKER_GID in the variables.env file
if grep -q "^DOCKER_GID=" variables.env; then
  sed -i "s/^DOCKER_GID=.*/DOCKER_GID=$DOCKER_GID/" variables.env
else
  echo "DOCKER_GID=$DOCKER_GID" >>variables.env
fi

set -o allexport
source variables.env
set +o allexport

bash mod_permissions.sh

# Start the Docker Compose stack
docker compose down
docker compose build
docker compose up --scale web=3 --scale celery=5 -d
