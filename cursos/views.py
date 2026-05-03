from django.shortcuts import render, get_object_or_404
from .models import Curso

def lista_cursos(request):
    cursos = Curso.objects.all()  # pylint: disable=no-member
    return render(request, "cursos/lista_cursos.html", {"cursos": cursos})


def curso_detalle(request, id):
    curso = get_object_or_404(Curso, id=id)
    return render(request, "cursos/curso_detalle.html", {
        "curso": curso
    })
def finalizar_curso(request, curso_id):
        curso = get_object_or_404(Curso, id=id)
{}