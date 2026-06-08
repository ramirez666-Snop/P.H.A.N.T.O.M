from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import django.contrib.auth.models
from cursos.models import Curso, Inscripcion
from django.contrib import messages
from laboratorios.models import LaboratorioProgreso

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Intentamos obtener al usuario por email
        try:
            # Importante: Asegúrate de que tus usuarios tengan emails únicos
            user_obj = django.contrib.auth.models.User.objects.get(email=email)
            username = user_obj.username
        except django.contrib.auth.models.User.DoesNotExist:
            return render(request, "usuarios/login.html", {
                "error": "El correo electrónico no está registrado"
            })
        except django.contrib.auth.models.User.MultipleObjectsReturned:
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
    inscripciones = Inscripcion.objects.filter(
        usuario=request.user
    ).select_related("curso")

    cursos_completados = inscripciones.filter(completado=True)
    cursos_en_progreso = inscripciones.filter(completado=False)

    labs_completados = LaboratorioProgreso.objects.filter(
        usuario=request.user,
        completado=True
    )

    labs_en_progreso = LaboratorioProgreso.objects.filter(
        usuario=request.user,
        iniciado=True,
        completado=False
    )

    total_labs = 5  # SQL, Auditoría Linux, Ingeniería Social, Sniffing, NOC

    labs_completados_count = labs_completados.count()
    labs_en_progreso_count = labs_en_progreso.count()

    labs_restantes = total_labs - labs_completados_count

    if labs_restantes < 0:
        labs_restantes = 0

    porcentaje_labs = int((labs_completados_count / total_labs) * 100)

    return render(request, "usuarios/dashboard.html", {
        "inscripciones": inscripciones,

        "cursos_completados": cursos_completados,
        "cursos_en_progreso": cursos_en_progreso,

        "labs_completados": labs_completados,
        "labs_en_progreso": labs_en_progreso,

        "labs_completados_count": labs_completados_count,
        "labs_en_progreso_count": labs_en_progreso_count,
        "labs_restantes": labs_restantes,
        "total_labs": total_labs,
        "porcentaje_labs": porcentaje_labs,
    })

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
        if django.contrib.auth.models.User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso")
            return render(request, "usuarios/registro.html")
            
        if django.contrib.auth.models.User.objects.filter(email=email).exists():
            messages.error(request, "Este correo ya tiene una cuenta activa")
            return render(request, "usuarios/registro.html")

        # 3. Crear usuario (Usar create_user para que encripte la clave)
        user = django.contrib.auth.models.User.objects.create_user(
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