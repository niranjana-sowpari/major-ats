from django.urls import path
from . import views

urlpatterns = [
path('<str:name>', views.index , name = "index"),
path("", views.home, name = "home"),
path("form/", views.form , name = "form"),
path("jds/", views.web_scrap_jd , name = "jds"),
path("df/", views.dataframe, name = "df"),
path("final/", views.final , name = "final")
]