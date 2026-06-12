
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from laboratorios.models import LaboratorioProgreso


@login_required
def completar_laboratorio(request, slug):

    try:

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

    except Exception as e:
        print("ERROR LAB:", e)

        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)


        
@login_required
def desafio_sql_injection(request):
    slug = "sql-injection"

    progreso, _ = LaboratorioProgreso.objects.get_or_create(
        usuario=request.user,
        slug=slug,
        defaults={
            "nombre": "SQL Injection",
            "iniciado": True,
            "completado": False,
        }
    )

    if request.method == "POST":
        progreso.iniciado = True
        progreso.completado = True
        progreso.save()

        return JsonResponse({
            "status": "success",
            "message": "Desafío guardado correctamente."
        })

    q = request.GET.get("q", "").strip()
    print("VALOR DE Q:", q)

    results = []
    error = None
    query_ejecutada = None
    objetivo_resuelto = False

    if q:
        query_ejecutada = (
            "SELECT username, role, secret_key "
            "FROM users "
            f"WHERE username = '{q}';"
        )

        q_lower = q.lower()
        q_clean = q_lower.replace(" ", "")

        if q_lower == "admin":
            results = [
                {
                    "username": "admin",
                    "role": "administrator",
                    "secret_key": "********"
                }
            ]

        elif q_lower == "victor":
            results = [
                {
                    "username": "victor",
                    "role": "student",
                    "secret_key": "********"
                }
            ]

        elif q_lower == "guest":
            results = [
                {
                    "username": "guest",
                    "role": "guest",
                    "secret_key": "********"
                }
            ]

        elif "'or1=1--" in q_clean or "'or'1'='1" in q_clean:
            results = [
                {
                    "username": "admin",
                    "role": "administrator",
                    "secret_key": "PHANTOM{SQL_INJECTION_LAB_COMPLETED}"
                },
                {
                    "username": "victor",
                    "role": "student",
                    "secret_key": "********"
                },
                {
                    "username": "guest",
                    "role": "guest",
                    "secret_key": "********"
                },
            ]

            objetivo_resuelto = True

        else:
            error = "La consulta no devolvió registros."

    return render(request, "challenges/sql_injection.html", {
        "results": results,
        "error": error,
        "query_ejecutada": query_ejecutada,
        "objetivo_resuelto": objetivo_resuelto,
        "ya_completado": progreso.completado,
    })