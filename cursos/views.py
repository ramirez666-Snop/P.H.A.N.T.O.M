from django.shortcuts import render
from django.http import HttpResponse

def cursos_home(request):
    return HttpResponse("Página de Cursos funcionando")

