from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("list/", views.UserListView.as_view(), name="list"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("<uuid:poll_id>/", views.DetailView.as_view(), name="details"),
    path(
        "vote/<int:slot_id>/", views.vote, name="vote"
    ),  # Function-based for simplicity
    path("close/<uuid:poll_id>/<int:slot_id>/", views.close_poll, name="close_poll"),
    path("download_ics/<uuid:poll_id>/", views.download_ics, name="download_ics"),
]
