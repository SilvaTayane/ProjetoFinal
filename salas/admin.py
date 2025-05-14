from django.contrib import admin
from salas.models import Sala

# Register your models here.
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome_sala', 'descricao_sala')
    prepopulated_fields = {
        'slug': ('nome_sala',)
    }
    

admin.site.register(Sala, SalaAdmin)
