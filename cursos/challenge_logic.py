import sqlite3
from django.shortcuts import render, redirect
from django.http import Http404


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
    #"nuevo_lab": {
    #"tipo": "template",
    #"template": "laboratorios/nuevo_lab.html",
#},
}

def lab_auditoria_linux(request):
    return render(request, "desafios/lab_auditoria_linux.html")

def ingenieria_social(request):
    return render(request, "desafios/ingenieria_social.html")

def sniffing_lab(request):
    return render(request, "desafios/sniffing_lab.html")

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


def desafio_sql_injection(request):
    results = []
    error = None
    raw_query = ""

    conn = sqlite3.connect(":memory:")

    try:
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE users (id INT, username TEXT, secret_key TEXT)")
        cursor.execute("INSERT INTO users VALUES (1, 'admin', 'FLAG{SQL_MASTER_2024}')")
        cursor.execute("INSERT INTO users VALUES (2, 'operador', 'password123')")

        query_input = request.GET.get("q", "")

        if query_input:
            raw_query = f"SELECT username FROM users WHERE username = '{query_input}'"
            cursor.execute(raw_query)
            results = list(cursor.fetchall())

    except Exception as e:
        error = str(e)

    finally:
        conn.close()

    return render(request, "desafios/sql_lab.html", {
        "results": results,
        "error": error,
        "query_ejecutada": raw_query
    })