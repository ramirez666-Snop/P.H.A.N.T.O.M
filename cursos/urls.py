from django.urls import path
from . import views

urlpatterns = [
    # Ejemplo: ruta de prueba
    path("", views.cursos_home, name="cursos_home"),
]
