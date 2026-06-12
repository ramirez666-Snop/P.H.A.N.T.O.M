from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from cursos import challenge_logic

urlpatterns = [
    path('', lambda request: redirect('login')),  # Redirige la raíz a login
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # Usa las URLs de la app usuarios
    path('cursos/', include('cursos.urls')),
    path('laboratorios/', include('laboratorios.urls')),
    path('challenges/sql-injection/', challenge_logic.desafio_sql_injection, name='sql_challenge'),
    path('iniciar/<str:desafio_slug>/', challenge_logic.iniciar_desafio, name='lanzador_desafios'),   
    path("laboratorio/auditoria-linux/",challenge_logic.lab_auditoria_linux,name="lab_auditoria_linux"),
    path("laboratorio/ingenieria-social/",challenge_logic.ingenieria_social,name="ingenieria_social"),
    path("laboratorio/sniffing/",challenge_logic.sniffing_lab,name="sniffing_lab"),
    path("laboratorio/analisis-red-noc/",challenge_logic.analisis_red_noc,name="analisis_red_noc"),
    path("laboratorios/completar/<slug:slug>/",challenge_logic.completar_laboratorio,name="completar_laboratorio"),
]