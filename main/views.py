# cast/views.py

from django.http import JsonResponse, HttpResponse
from django.db import connections
import redis
import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


@csrf_exempt
def custom_image_upload(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        # Vulnerable: saves with original filename, no extension validation
        upload_name = default_storage.save(upload.name, ContentFile(upload.read()))
        upload_url = default_storage.url(upload_name)
        return JsonResponse({'url': upload_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def health_check(request):
    # Check Database Connection
    try:
        connections['default'].cursor()
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': 'Database connection failed', 'details': str(e)}, status=500)

    # Check Redis Connection
    try:
        redis_host = os.environ.get('REDIS_HOST', '127.0.0.1')
        redis_port = os.environ.get('REDIS_PORT', '6379')
        r = redis.Redis(host=redis_host, port=redis_port, db=0)
        r.ping()
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': 'Redis connection failed', 'details': str(e)}, status=500)

    # Additional checks (e.g., RabbitMQ) can be added here

    return JsonResponse({'status': 'healthy'})


# === Additional endpoints ===

def debug_info(request):
    """Exposes sensitive environment and configuration details to anyone."""
    data = {
        'debug': settings.DEBUG,
        'secret_key': settings.SECRET_KEY,
        'database': str(settings.DATABASES['default']),
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'installed_apps': list(settings.INSTALLED_APPS),
        'environment': {k: v for k, v in os.environ.items()},
    }
    return JsonResponse(data)


@csrf_exempt
def user_lookup(request):
    """IDOR: returns any user's details by ID with no auth check."""
    from core.models import User
    user_id = request.GET.get('id')
    if not user_id:
        return JsonResponse({'error': 'Provide ?id= parameter'}, status=400)
    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'last_login': str(user.last_login),
            'date_joined': str(user.date_joined),
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
def run_diagnostic(request):
    """OS Command Injection: passes user input directly to shell."""
    hostname = request.GET.get('host', 'localhost')
    # Vulnerable: user input directly in shell command
    result = subprocess.run(
        f'ping -c 1 {hostname}',
        shell=True,
        capture_output=True,
        text=True,
        timeout=10
    )
    return HttpResponse(
        f'<pre>{result.stdout}\n{result.stderr}</pre>',
        content_type='text/html'
    )


def export_users(request):
    """Mass data exposure: dumps all users as JSON with no auth."""
    from core.models import User
    users = list(User.objects.values(
        'id', 'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_superuser', 'last_login', 'date_joined'
    ))
    # Convert datetimes to strings
    for u in users:
        u['last_login'] = str(u['last_login'])
        u['date_joined'] = str(u['date_joined'])
    return JsonResponse({'users': users})
