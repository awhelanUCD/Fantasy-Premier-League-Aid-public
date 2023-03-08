from django.urls import path
from . import views


urlpatterns = [
  path("", views.live_gameweek_form, name="live_gameweek"),
]
