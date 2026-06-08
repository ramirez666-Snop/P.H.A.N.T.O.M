from django.db import models
import django.contrib.auth.models
from django.utils import timezone


# Create your models here.
class Resultado(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    seccion = models.ForeignKey('cursos.Seccion', on_delete=models.CASCADE)
    calificacion = models.FloatField()

    def __str__(self):
        return f"{self.usuario.nombre} - {self.seccion.titulo} ({self.calificacion})"

class LaboratorioProgreso(models.Model):
    usuario = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)

    slug = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)

    iniciado = models.BooleanField(default=False)
    completado = models.BooleanField(default=False)

    progreso_binario = models.IntegerField(default=0)
    calificacion = models.FloatField(default=0)

    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("usuario", "slug")

    def __str__(self):
        return f"{self.usuario.username} - {self.nombre} - {self.calificacion}"