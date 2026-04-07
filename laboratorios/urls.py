from django.urls import path
from . import views

urlpatterns = [
    path("", views.laboratorios_home, name="laboratorios_home"),
]
