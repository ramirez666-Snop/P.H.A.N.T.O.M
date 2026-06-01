from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Curso, Inscripcion, Seccion

def lista_cursos(request):
    # Pylint a veces no ve el objeto 'objects', usamos disable si es necesario
    cursos = Curso.objects.all()  # pylint: disable=no-member
    return render(request, "cursos/lista_cursos.html", {"cursos": cursos})

@login_required
def curso_detalle(request, id):
    curso = get_object_or_404(Curso, id=id)

    inscripcion, _ = Inscripcion.objects.get_or_create(
        usuario=request.user,
        curso=curso,
        defaults={
            "progreso_porcentaje": 0,
            "completado": False,
        }
    )

    print("INSCRIPCION CREADA/OBTENIDA:", inscripcion.id)

    return render(request, "cursos/curso_detalle.html", {
        "curso": curso,
        "inscripcion": inscripcion
    })


@login_required
def finalizar_curso(request, curso_id):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Método no permitido"
        }, status=405)

    curso = get_object_or_404(Curso, id=curso_id)

    inscripcion, created = Inscripcion.objects.get_or_create(
        usuario=request.user,
        curso=curso,
        defaults={
            "progreso_porcentaje": 0,
            "completado": False,
        }
    )

    inscripcion.progreso_porcentaje = 100
    inscripcion.completado = True
    inscripcion.fecha_finalizacion = timezone.now()
    inscripcion.save()

    return JsonResponse({
        "status": "success",
        "message": "Curso completado",
        "progreso": inscripcion.progreso_porcentaje,
        "completado": inscripcion.completado,
    })


@login_required
def actualizar_progreso(request, inscripcion_id):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Método no permitido'
        }, status=405)

    try:
        data = json.loads(request.body)

        inscripcion = get_object_or_404(
            Inscripcion,
            id=inscripcion_id,
            usuario=request.user
        )

        nuevo_progreso = int(data.get('progreso', 0))

        if nuevo_progreso > inscripcion.progreso_porcentaje:
            inscripcion.progreso_porcentaje = nuevo_progreso

        if data.get('completado') is True:
            inscripcion.completado = True
            inscripcion.progreso_porcentaje = 100
            inscripcion.fecha_finalizacion = timezone.now()

        inscripcion.save()

        return JsonResponse({
            'status': 'success',
            'progreso': inscripcion.progreso_porcentaje,
            'completado': inscripcion.completado
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    