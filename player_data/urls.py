from django.urls import path
from . import views

urlpatterns = [
    path("", views.player_data, name="player_data"),
    path("toggle_test", views.toggle_test, name="toggle_test"),
]
