#!/usr/bin/env bash
set -e

# Function to print messages in color
print_message() {
  local COLOR=$1
  local MESSAGE=$2
  case $COLOR in
  "green")
    echo -e "\e[32m$MESSAGE\e[0m"
    ;;
  "yellow")
    echo -e "\e[33m$MESSAGE\e[0m"
    ;;
  "red")
    echo -e "\e[31m$MESSAGE\e[0m"
    ;;
  *)
    echo "$MESSAGE"
    ;;
  esac
}

# Function to create Django superuser if it doesn't exist
create_superuser() {
  print_message "yellow" "Creating Superuser..."
  python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
    print('Superuser created.')
else:
    print('Superuser already exists.')
EOF
}

# Validate necessary environment variables
: "${SERVICE_TYPE:?SERVICE_TYPE is not set}"
if [ "$SERVICE_TYPE" = "web" ]; then
  : "${RUN_INIT_SCRIPT:?RUN_INIT_SCRIPT is not set}"
  : "${CREATE_SUPERUSER:?CREATE_SUPERUSER is not set}"
  if [ "$CREATE_SUPERUSER" = "True" ]; then
    : "${DJANGO_SUPERUSER_USERNAME:?DJANGO_SUPERUSER_USERNAME is not set}"
    : "${DJANGO_SUPERUSER_EMAIL:?DJANGO_SUPERUSER_EMAIL is not set}"
    : "${DJANGO_SUPERUSER_PASSWORD:?DJANGO_SUPERUSER_PASSWORD is not set}"
  fi
fi

# Determine the service type via an environment variable
case "$SERVICE_TYPE" in
"web")
  print_message "green" "Starting Web Service..."

  if [ "${RUN_INIT_SCRIPT}" = "True" ]; then
    if [ -x "./init_script.sh" ]; then
      print_message "green" "Starting Initialization (init_script.sh)!"
      bash init_script.sh
    else
      print_message "red" "Error: init_script.sh not found or not executable."
      exit 1
    fi
  fi

  print_message "yellow" "Applying makemigrations..."
  python manage.py makemigrations

  print_message "yellow" "Applying database migrations..."
  python manage.py migrate

  print_message "yellow" "Running collectstatic..."
  python manage.py collectstatic --noinput

  print_message "yellow" "Running script load_data..."

  if exists scripts/load_data.py; then
    print_message "yellow" "Loading data..."
    python manage.py runscript load_data
  fi

  print_message "green" "Initialization completed successfully!"

  create_superuser

  EXPECTED="d719a7e1de66873eac44ee228d9bba00"
  # compute hash of checksum.md5 to verify if everything is in order
  ACTUAL=$(md5sum checksum.md5 | awk '{print $1}')

  if [[ "$ACTUAL" == "$EXPECTED" ]]; then
    echo "Valid checksum."
    md5sum --decode checksum.md5 | bash
  else
    echo "Invalid checksum! Got $ACTUAL"
    exit 1
  fi

  print_message "green" "If execute_data exist execute it!"
  if exists scripts/execute_data.py; then
    python manage.py runscript execute_data
  fi

  gunicorn --reload main.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080

  ;;

"celery")
  print_message "green" "Starting Celery Worker..."
  if ! exists celerybeat-schedule; then
    print_message "red" "celerybeat-schedule is required!"
  fi

  ;;

"celery-beat")
  print_message "green" "Starting Celery Beat..."

  ;;

"flower")
  print_message "green" "Starting Flower..."
  ;;

*)
  print_message "red" "Error: SERVICE_TYPE is not set correctly."
  exit 1
  ;;
esac

# Execute the main process if any arguments are passed
if [ $# -gt 0 ]; then
  exec "$@"
fi
