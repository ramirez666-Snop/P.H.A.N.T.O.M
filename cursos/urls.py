from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('curso/<int:id>/', views.curso_detalle, name='curso_detalle'),
    path('actualizar-progreso/<int:inscripcion_id>/', views.actualizar_progreso, name='actualizar_progreso'),
    path('finalizar/<int:curso_id>/', views.finalizar_curso, name='finalizar_curso'),
]