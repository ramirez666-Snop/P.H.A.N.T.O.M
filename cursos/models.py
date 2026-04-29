from django.db import models

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.URLField(blank=True, null=True)
    duracion = models.CharField(max_length=50, blank=True)
    dificultad = models.CharField(max_length=20, blank=True)

    def __str__(self):
        # Forzamos a que siempre se reconozca como string
        return str(self.titulo) if self.titulo else "Sin título"


class Seccion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="secciones")
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.URLField(blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    orden = models.IntegerField()

    def __str__(self):
        # Accedemos de forma que Pylint no se confunda
        nombre_curso = getattr(self.curso, 'titulo', 'Curso sin nombre')
        return f"{nombre_curso} - {self.titulo}"
    
class Inscripcion(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.curso.titulo}"