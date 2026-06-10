from django.urls import include, path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path('registro/', views.registro_view, name='registro'),
    path('cargar-curso/<int:curso_id>/', views.cargar_curso, name='cargar_curso'),
    path('', include('cursos.urls')),
    path("aviso-etico/", views.aviso_etico_view, name="aviso_etico"),
]

