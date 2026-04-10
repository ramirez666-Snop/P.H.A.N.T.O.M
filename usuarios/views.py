from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:  # pylint: disable=no-member
            return render(request, "usuarios/login.html", {
                "error": "Usuario no existe"
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "usuarios/login.html", {
                "error": "Credenciales incorrectas"
            })

    return render(request, "usuarios/login.html")


@login_required
def dashboard_view(request):
    return render(request, "usuarios/dashboard.html")


def registro_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        #Valida la contraseñas
        if password1 != password2:
            return render(request, "usuarios/registro.html", {
                "error": "Las contraseñas no coinciden"
            })

        #Valida al usuario existente
        if User.objects.filter(username=username).exists():
            return render(request, "usuarios/registro.html", {
                "error": "El usuario ya existe"
            })

        #Valida el correo existente
        if User.objects.filter(email=email).exists():
            return render(request, "usuarios/registro.html", {
                "error": "El correo ya está registrado"
            })

        #Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        user.save()

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
    Vista que retorna el partial del curso solicitado
    """
    # Mapeo de IDs a templates
    cursos = {
        1: 'usuarios/partials/primer_curso.html',
        
    }
    
    template_name = cursos.get(curso_id)
    
    if template_name:
        context = {
            'curso_id': curso_id,
            'titulo': f'Curso {curso_id}'  # Puedes pasar datos adicionales
        }
        return render(request, template_name, context)
    else:
        return render(request, 'usuarios/partials/primer_curso.html', {'curso_id': curso_id})