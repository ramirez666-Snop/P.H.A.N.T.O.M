from django.contrib import admin
from .models import Resultado

# Register your models here.
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'seccion', 'calificacion')
    search_fields = ('usuario__nombre',)
    list_filter = ('calificacion',)

admin.site.register(Resultado, ResultadoAdmin)


