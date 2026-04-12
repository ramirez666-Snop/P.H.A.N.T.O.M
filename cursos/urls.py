from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('curso/<int:id>/', views.curso_detalle, name='curso_detalle'),
]