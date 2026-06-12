from django.shortcuts import get_object_or_404, render, redirect

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
    get_user_model,
)
from django.contrib.auth.decorators import login_required

from cursos.models import Curso, Inscripcion
from laboratorios.models import LaboratorioProgreso


User = get_user_model()


@login_required
def aviso_etico_view(request):
    if request.method == "POST":
        request.session["aviso_etico_aceptado"] = True
        return redirect("dashboard")

    return render(request, "usuarios/aviso_etico.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
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

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("aviso_etico")

            return render(request, "usuarios/login.html", {
                "error": "Cuenta desactivada"
            })

        return render(request, "usuarios/login.html", {
            "error": "Contraseña incorrecta"
        })

    return render(request, "usuarios/login.html")


@login_required
def dashboard_view(request):
    if not request.session.get("aviso_etico_aceptado"):
        return redirect("aviso_etico")

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

    total_labs = 5

    labs_completados_count = labs_completados.count()
    labs_en_progreso_count = labs_en_progreso.count()
    labs_restantes = max(total_labs - labs_completados_count, 0)

    porcentaje_labs = (
        int((labs_completados_count / total_labs) * 100)
        if total_labs > 0
        else 0
    )

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
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if not username:
            messages.error(request, "El nombre de usuario es obligatorio.")
            return render(request, "usuarios/registro.html")

        if not email:
            messages.error(request, "El correo electrónico es obligatorio.")
            return render(request, "usuarios/registro.html")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "usuarios/registro.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, "usuarios/registro.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este correo ya tiene una cuenta activa.")
            return render(request, "usuarios/registro.html")

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

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

    if section == "config" and request.method == "POST":
        usuario = request.user

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()

        cambios = []

        if not username:
            messages.error(request, "El nombre de usuario no puede estar vacío.")
            return redirect("dashboard")

        if not email:
            messages.error(request, "El correo electrónico no puede estar vacío.")
            return redirect("dashboard")

        if User.objects.exclude(id=usuario.id).filter(username=username).exists():
            messages.error(request, "Ese nombre de usuario ya está en uso.")
            return redirect("dashboard")

        if User.objects.exclude(id=usuario.id).filter(email=email).exists():
            messages.error(request, "Ese correo electrónico ya está registrado.")
            return redirect("dashboard")

        if username != usuario.username:
            usuario.username = username
            cambios.append("nombre de usuario")

        if email != usuario.email:
            usuario.email = email
            cambios.append("correo electrónico")

        if password1 or password2:
            if password1 != password2:
                messages.error(request, "Las contraseñas no coinciden.")
                return redirect("dashboard")

            if len(password1) < 8:
                messages.error(
                    request,
                    "La contraseña debe tener al menos 8 caracteres."
                )
                return redirect("dashboard")

            usuario.set_password(password1)
            cambios.append("contraseña")

        if cambios:
            usuario.save()

            if "contraseña" in cambios:
                update_session_auth_hash(request, usuario)

            messages.success(
                request,
                "Se actualizó correctamente: " + ", ".join(cambios) + "."
            )
        else:
            messages.info(request, "No se realizaron cambios.")

        return redirect("dashboard")

    tpl = template_map.get(section)

    if tpl:
        return render(request, tpl)

    return render(request, "usuarios/partial/panel.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def cargar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    context = {
        "curso": curso,
    }

    return render(request, "cursos/curso_detalle.html", context)