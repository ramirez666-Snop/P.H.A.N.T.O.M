from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# from core import views  # <--- ELIMINA o COMENTA esta línea

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
]