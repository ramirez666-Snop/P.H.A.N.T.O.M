from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Importación explícita desde el paquete actual
from .models import Curso, Inscripcion, Seccion

def lista_cursos(request):
    # Pylint a veces no ve el objeto 'objects', usamos disable si es necesario
    cursos = Curso.objects.all()  # pylint: disable=no-member
    return render(request, "cursos/lista_cursos.html", {"cursos": cursos})

def curso_detalle(request, id):
    # Obtenemos el curso y su inscripción para el usuario actual
    curso = get_object_or_404(Curso, id=id)
    
    # IMPORTANTE: Buscamos la inscripción del usuario para pasar el progreso al template
    # Si no existe, podrías crearla o manejar el error
    inscripcion = Inscripcion.objects.filter(usuario=request.user, curso=curso).first()
    
    return render(request, "cursos/curso_detalle.html", {
        "curso": curso,
        "inscripcion": inscripcion
    })

def finalizar_curso(request, curso_id):
    # Corregido: se usaba 'id' pero el parámetro es 'curso_id'
    curso = get_object_or_404(Curso, id=curso_id)
    return JsonResponse({'status': 'terminado'})

@csrf_exempt # Permite recibir peticiones POST desde JS sin errores de token si no se envía el header
def actualizar_progreso(request, inscripcion_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Usamos filter().first() o get() para obtener la inscripción
            inscripcion = Inscripcion.objects.get(id=inscripcion_id) # pylint: disable=no-member
            
            # 1. Actualizar porcentaje si es mayor al actual
            nuevo_progreso = int(data.get('progreso', 0))
            if nuevo_progreso > inscripcion.progreso_porcentaje:
                inscripcion.progreso_porcentaje = nuevo_progreso
            
            # 2. Si llega al final, marcar como completado
            if data.get('completado') is True:
                inscripcion.completado = True
                # Aquí podrías asignar timezone.now() a fecha_finalizacion
            
            inscripcion.save()
            return JsonResponse({'status': 'success', 'progreso': inscripcion.progreso_porcentaje})
            
        except Inscripcion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Inscripción no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)