from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("", views.chat_room, name="room"),
    path("send/", views.send_message, name="send"),
    path("messages/", views.get_messages, name="messages"),
    path("online/", views.online_users, name="online"),
]
