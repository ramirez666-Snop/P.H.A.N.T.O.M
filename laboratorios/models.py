from django.db import models

# Create your models here.
class Resultado(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    seccion = models.ForeignKey('cursos.Seccion', on_delete=models.CASCADE)
    calificacion = models.FloatField()

    def __str__(self):
        return f"{self.usuario.nombre} - {self.seccion.titulo} ({self.calificacion})"