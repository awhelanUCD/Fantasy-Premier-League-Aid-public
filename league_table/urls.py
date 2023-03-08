from django.urls import path
from . import views


urlpatterns = [
#path("enterLeageuID", views.league_form, name="league_form"),
    path("league_table_test", views.league_table, name="league_table_test"),
    path("", views.league_table_submit, name="league_table"),
]
