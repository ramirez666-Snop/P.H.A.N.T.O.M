import sqlite3
import json
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from laboratorios.models import LaboratorioProgreso


DESAFIOS = {
    "sql-injection": {
        "tipo": "redirect",
        "ruta": "sql_challenge",
    },
    "lab_auditoria_linux": {
        "tipo": "loading",
        "template_carga": "desafios/cargando_lab.html",
        "url_final": "lab_auditoria_linux",
        "titulo": "Auditoría Básica Linux",
    },
    "ingenieria_social": {
        "tipo": "loading",
        "template_carga": "desafios/cargando_lab.html",
        "url_final": "ingenieria_social",
        "titulo": "Ingeniería Social",
    },
    "sniffing_lab": {
        "tipo": "loading",
        "template_carga": "desafios/cargando_lab.html",
        "url_final": "sniffing_lab",
        "titulo": "Sniffing Lab",
    },
    "analisis_red_noc": {
        "tipo": "loading",
        "template_carga": "desafios/cargando_lab.html",
        "url_final": "analisis_red_noc",
        "titulo": "Análisis de Red NOC",
    },
}


@login_required
def lab_auditoria_linux(request):

    progreso, _ = LaboratorioProgreso.objects.get_or_create(
        usuario=request.user,
        slug="lab_auditoria_linux",
        defaults={
            "nombre": "Auditoría Básica Linux",
            "iniciado": True,
            "completado": False,
            "progreso_binario": 0,
            "calificacion": 0,
        }
    )

    if not progreso.iniciado:
        progreso.iniciado = True
        progreso.save()

    return render(request, "desafios/lab_auditoria_linux.html", {
        "ya_completado": progreso.completado
    })


@login_required
def ingenieria_social(request):

    progreso, _ = LaboratorioProgreso.objects.get_or_create(
        usuario=request.user,
        slug="ingenieria_social",
        defaults={
            "nombre": "Ingeniería Social",
            "iniciado": True,
            "completado": False,
            "progreso_binario": 0,
            "calificacion": 0,
        }
    )

    if not progreso.iniciado:
        progreso.iniciado = True
        progreso.save()

    return render(request, "desafios/ingenieria_social.html", {
        "ya_completado": progreso.completado
    })


@login_required
def sniffing_lab(request):

    progreso, _ = LaboratorioProgreso.objects.get_or_create(
        usuario=request.user,
        slug="sniffing_lab",
        defaults={
            "nombre": "Sniffing Lab",
            "iniciado": True,
            "completado": False,
            "progreso_binario": 0,
            "calificacion": 0,
        }
    )

    if not progreso.iniciado:
        progreso.iniciado = True
        progreso.save()

    return render(request, "desafios/sniffing_lab.html", {
        "ya_completado": progreso.completado
    })


@login_required
def analisis_red_noc(request):

    progreso, _ = LaboratorioProgreso.objects.get_or_create(
        usuario=request.user,
        slug="analisis_red_noc",
        defaults={
            "nombre": "Análisis de Red NOC",
            "iniciado": True,
            "completado": False,
            "progreso_binario": 0,
            "calificacion": 0,
        }
    )

    if not progreso.iniciado:
        progreso.iniciado = True
        progreso.save()

    return render(request, "desafios/analisis_red_noc.html", {
        "ya_completado": progreso.completado
    })


@login_required
def iniciar_desafio(request, desafio_slug):
    desafio = DESAFIOS.get(desafio_slug)

    if not desafio:
        return redirect("dashboard")

    if desafio["tipo"] == "redirect":
        return redirect(desafio["ruta"])

    if desafio["tipo"] == "loading":
        return render(request, desafio["template_carga"], {
            "titulo": desafio["titulo"],
            "url_final": desafio["url_final"],
        })

    return redirect("dashboard")



@login_required
def desafio_sql_injection(request):
    slug = "sql-injection"
    nombre_lab = "SQL Injection Lab"

    progreso, _ = LaboratorioProgreso.objects.get_or_create(
        usuario=request.user,
        slug=slug,
        defaults={
            "nombre": nombre_lab,
            "iniciado": True,
            "completado": False,
            "progreso_binario": 0,
            "calificacion": 0,
        }
    )

    if not progreso.iniciado:
        progreso.iniciado = True
        progreso.save()

    if request.method == "POST":
        progreso.completado = True
        progreso.progreso_binario = 100
        progreso.calificacion = 100
        progreso.fecha_finalizacion = timezone.now()
        progreso.save()

        return JsonResponse({
            "status": "success",
            "message": "Laboratorio completado correctamente.",
            "progreso": progreso.progreso_binario,
            "calificacion": progreso.calificacion,
        })

    results = []
    error = None
    raw_query = ""
    objetivo_resuelto = False

    conn = sqlite3.connect(":memory:")

    try:
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE users (id INT, username TEXT, secret_key TEXT)")
        cursor.execute("INSERT INTO users VALUES (1, 'admin', 'FLAG{SQL_MASTER_2024}')")
        cursor.execute("INSERT INTO users VALUES (2, 'operador', 'password123')")

        query_input = request.GET.get("q", "")

        if query_input:
            raw_query = f"SELECT username, secret_key FROM users WHERE username = '{query_input}'"
            cursor.execute(raw_query)
            results = list(cursor.fetchall())

            for row in results:
                if "FLAG{SQL_MASTER_2024}" in row:
                    objetivo_resuelto = True

    except Exception as e:
        error = str(e)

    finally:
        conn.close()

    return render(request, "desafios/sql_lab.html", {
        "results": results,
        "error": error,
        "query_ejecutada": raw_query,
        "objetivo_resuelto": objetivo_resuelto,
        "ya_completado": progreso.completado,
        "slug": slug,
    })

@login_required
def completar_laboratorio(request, slug):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Método no permitido"
        }, status=405)

    data = json.loads(request.body or "{}")

    puntaje = data.get("puntaje", 100)

    progreso = get_object_or_404(
        LaboratorioProgreso,
        usuario=request.user,
        slug=slug
    )

    progreso.completado = True
    progreso.progreso_binario = 100
    progreso.calificacion = puntaje
    progreso.fecha_finalizacion = timezone.now()
    progreso.save()

    return JsonResponse({
        "status": "success",
        "message": "Laboratorio completado correctamente"
    })