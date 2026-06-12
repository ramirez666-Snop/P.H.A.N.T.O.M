from django.urls import include, path

from cursos import challenge_logic
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path('registro/', views.registro_view, name='registro'),
    path('cargar-curso/<int:curso_id>/', views.cargar_curso, name='cargar_curso'),
    path('', include('cursos.urls')),
    path("aviso-etico/", views.aviso_etico_view, name="aviso_etico"),
    path("dashboard/<str:section>/", views.dashboard_partial, name="dashboard_partial"),
    path("laboratorios/completar/<slug:slug>/",challenge_logic.completar_laboratorio,name="completar_laboratorio"),
    path("laboratorios/completar/<slug:slug>/",challenge_logic.completar_laboratorio,name="completar_laboratorio"),
    path("challenges/sql-injection/",challenge_logic.desafio_sql_injection,name="sql_challenge"),
    path("laboratorios/completar/<slug:slug>/",challenge_logic.completar_laboratorio,name="completar_laboratorio"),
    path("laboratorios/completar/<slug:slug>/",challenge_logic.completar_laboratorio,name="completar_laboratorio"),
]

