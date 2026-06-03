from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from laboratorios.models import Resultado


@login_required
def desafio_sql_injection(request):
    q = request.GET.get("q", "")
    results = []
    error = None
    query_ejecutada = None
    completado = False

    if q:
        query_ejecutada = f"SELECT secret_key FROM users WHERE username = '{q}'"

        if "' OR 1=1 --" in q or "OR 1=1" in q.upper():
            results = [("PHANTOM{sql_injection_success}",)]
            completado = True
        else:
            error = "Consulta inválida o sin resultados."

    return render(request, "desafios/sql_lab.html", {
        "results": results,
        "error": error,
        "query_ejecutada": query_ejecutada,
        "completado": completado,
        "slug": "sql-injection",
    })


@login_required
def completar_desafio(request):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Método no permitido"
        }, status=405)

    slug = request.POST.get("slug")

    nombres = {
        "sql-injection": "SQL Injection",
        "tcp-visualizer": "Visualización TCP",
    }

    if slug not in nombres:
        return JsonResponse({
            "status": "error",
            "message": "Desafío inválido"
        }, status=400)

    resultado, _ = Resultado.objects.get_or_create(
        usuario=request.user,
        slug=slug,
        defaults={
            "nombre": nombres[slug],
            "calificacion": 100
        }
    )

    resultado.nombre = nombres[slug]
    resultado.completado = True
    resultado.calificacion = 100
    resultado.fecha_completado = timezone.now()
    resultado.save()

    return JsonResponse({"status": "success"})