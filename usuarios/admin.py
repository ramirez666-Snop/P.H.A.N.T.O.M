from django.contrib import admin
from .models import Usuario

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'rol')
    search_fields = ('nombre', 'correo')
    list_filter = ('rol',)

admin.site.register(Usuario, UsuarioAdmin)


