from django.contrib import admin
from .models import Curso, Seccion, Inscripcion

class SeccionInline(admin.TabularInline):
    model = Seccion
    extra = 1

class CursoAdmin(admin.ModelAdmin):
    inlines = [SeccionInline]

admin.site.register(Curso, CursoAdmin)
admin.site.register(Seccion)
admin.site.register(Inscripcion)