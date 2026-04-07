from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "usuarios/login.html", {"error": "Credenciales inválidas"})
    return render(request, "usuarios/login.html")


def dashboard_view(request):
    return render(request, "usuarios/dashboard.html")


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

