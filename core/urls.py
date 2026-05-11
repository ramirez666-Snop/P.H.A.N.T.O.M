from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from cursos import challenge_logic

urlpatterns = [
    path('', lambda request: redirect('login')),  # Redirige la raíz a login
    path('admin/', admin.site.urls),
    # path('menu/', views.menu, name='menu'),  # <--- COMENTA o ELIMINA mientras no exista
    # path('login/', views.login_view, name='login'),  # <--- COMENTA o ELIMINA
    # path('logout/', views.logout_view, name='logout'),  # <--- COMENTA o ELIMINA
    # path('dashboard/', views.dashboard, name='dashboard'),  # <--- COMENTA o ELIMINA
    path('', include('usuarios.urls')),  # Usa las URLs de la app usuarios
    path('cursos/', include('cursos.urls')),
    path('laboratorios/', include('laboratorios.urls')),
    path('challenges/sql-injection/', challenge_logic.desafio_sql_injection, name='sql_challenge'),
path('iniciar/<str:desafio_slug>/', challenge_logic.iniciar_desafio, name='lanzador_desafios'),    
]