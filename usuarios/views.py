from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from cursos.models import Curso
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Intentamos obtener al usuario por email
        try:
            # Importante: Asegúrate de que tus usuarios tengan emails únicos
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            return render(request, "usuarios/login.html", {
                "error": "El correo electrónico no está registrado"
            })
        except User.MultipleObjectsReturned:
            return render(request, "usuarios/login.html", {
                "error": "Existen múltiples cuentas con este correo. Contacta a soporte."
            })

        # Ahora autenticamos usando el username recuperado
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("dashboard")
            else:
                return render(request, "usuarios/login.html", {"error": "Cuenta desactivada"})
        else:
            return render(request, "usuarios/login.html", {
                "error": "Contraseña incorrecta"
            })

    return render(request, "usuarios/login.html")


@login_required
def dashboard_view(request):
    return render(request, "usuarios/dashboard.html")


from django.contrib import messages # Importante añadir esto

def registro_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # 1. Validar contraseñas
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "usuarios/registro.html")

        # 2. Validar si el usuario o email ya existen
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso")
            return render(request, "usuarios/registro.html")
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este correo ya tiene una cuenta activa")
            return render(request, "usuarios/registro.html")

        # 3. Crear usuario (Usar create_user para que encripte la clave)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        # No hace falta user.save() aquí, create_user lo hace solo.

        messages.success(request, "¡Cuenta creada! Ya puedes iniciar sesión.")
        return redirect("login")

    return render(request, "usuarios/registro.html")


@login_required
def dashboard_partial(request, section):
    template_map = {
        "panel": "usuarios/partial/panel.html",
        "laboratorios": "usuarios/partial/laboratorios.html",
        "desafios": "usuarios/partial/desafios.html",
        "perfil": "usuarios/partial/perfil.html",
        "config": "usuarios/partial/config.html",
    }
    tpl = template_map.get(section)
    if tpl:
        return render(request, tpl)
    return render(request, "usuarios/partial/panel.html")

def logout_view(request):
    logout(request)
    return redirect("login")




def cargar_curso(request, curso_id):
    """
    Vista que recupera el curso de la base de datos y lo renderiza
    usando una plantilla dinámica.
    """
    # 1. Buscamos el curso en la BD. Si no existe, lanza un error 404.
    curso = get_object_or_404(Curso, id=curso_id)

    # 2. Pasamos el objeto 'curso' completo al contexto.
    # Ya no necesitamos el mapeo de diccionarios.
    context = {
        'curso': curso,
    }

    # 3. Usamos UN SOLO archivo de plantilla que servirá para todos los cursos.
    # Asegúrate de que este archivo sea el que tiene las etiquetas {{ curso.titulo }}, etc.
    return render(request, 'cursos/curso_detalle.html', context)