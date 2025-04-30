from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # Index Views
    path("", views.HomeView.as_view(), name="home"),
]
