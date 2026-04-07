from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("menu/", views.menu_view, name="menu"),
    path("", include("usuarios.urls")),
    path("cursos/", include("cursos.urls")),
    path("laboratorios/", include("laboratorios.urls")),
]


