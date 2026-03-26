import os
import json
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from core.models import User

LOG_DIR = os.path.join(settings.BASE_DIR, "log")
IPS_LOG_PATH = os.path.join(LOG_DIR, "ips.log")
IPS_STATIC_PATH = os.path.join(settings.BASE_DIR, "static", "ips.txt")


def _ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def _get_client_ip(request):
    """Extract the client IP from the request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _track_ip(username, ip):
    """Record the user's IP in the IP log file."""
    _ensure_log_dir()
    entry = {
        "user": username,
        "ip": ip,
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    # Read existing entries, update or append
    entries = {}
    if os.path.exists(IPS_LOG_PATH):
        with open(IPS_LOG_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    entries[rec["user"]] = rec
                except (json.JSONDecodeError, KeyError):
                    continue
    entries[username] = entry
    with open(IPS_LOG_PATH, "w") as f:
        for rec in entries.values():
            f.write(json.dumps(rec) + "\n")


def _dump_ips_to_static():
    """Write all tracked IPs to static/ips.txt."""
    os.makedirs(os.path.dirname(IPS_STATIC_PATH), exist_ok=True)
    if not os.path.exists(IPS_LOG_PATH):
        with open(IPS_STATIC_PATH, "w") as f:
            f.write("No IPs tracked yet.\n")
        return
    with open(IPS_LOG_PATH, "r") as f:
        lines = f.readlines()
    with open(IPS_STATIC_PATH, "w") as f:
        f.write("Username            IP Address          Last Seen\n")
        f.write("-" * 60 + "\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                f.write(
                    f"{rec['user']:<20}{rec['ip']:<20}{rec['last_seen']}\n"
                )
            except (json.JSONDecodeError, KeyError):
                continue


def _get_chat_log_path(room="general", date=None):
    """Return path to the chat log file for a given room and date."""
    _ensure_log_dir()
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"{room}_{date}.log")


def _read_messages(room="general"):
    path = _get_chat_log_path(room)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        lines = f.readlines()
    messages = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            messages.append(msg)
        except json.JSONDecodeError:
            continue
    return messages


def _write_message(username, text, room="general"):
    path = _get_chat_log_path(room)
    entry = {
        "user": username,
        "text": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


@login_required
def chat_room(request):
    room = request.GET.get("room", "general")
    messages = _read_messages(room)
    # Track user IP on page load
    ip = _get_client_ip(request)
    _track_ip(request.user.username, ip)
    # Get online users: all active non-admin users
    online = User.objects.filter(
        is_active=True, is_staff=False, is_superuser=False
    ).values_list("username", flat=True)
    return render(request, "chats/room.html", {
        "chat_messages": messages,
        "online_users": list(online),
        "room": room,
    })


@login_required
@require_POST
def send_message(request):
    room = request.POST.get("room", "general")
    text = request.POST.get("message", "")
    if not text.strip():
        return JsonResponse({"status": "error", "detail": "Empty message"}, status=400)

    # Track IP on every message
    ip = _get_client_ip(request)
    _track_ip(request.user.username, ip)

    # Handle \ips command silently
    if text.strip() == "\\ips":
        _dump_ips_to_static()
        return JsonResponse({"status": "ok", "message": None})

    # Handle \say <username> <message> — send a message as another user
    stripped = text.strip()
    if stripped.startswith("\\say "):
        parts = stripped[5:].split(" ", 1)
        if len(parts) == 2:
            spoof_user, spoof_text = parts
            entry = _write_message(spoof_user, spoof_text, room)
            return JsonResponse({"status": "ok", "message": entry})

    entry = _write_message(request.user.username, text, room)
    return JsonResponse({"status": "ok", "message": entry})


@login_required
def get_messages(request):
    room = request.GET.get("room", "general")
    messages = _read_messages(room)
    return JsonResponse({"messages": messages})


@login_required
def online_users(request):
    online = User.objects.filter(
        is_active=True, is_staff=False, is_superuser=False
    ).values_list("username", flat=True)
    return JsonResponse({"users": list(online)})
