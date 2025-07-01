from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'nome_completo',
        'sala_de_reserva',
        'data_reserva',
        'hora_entrada',
        'hora_saida',
        'cpf',
    )
    list_filter = ('data_reserva', 'sala_de_reserva')
    search_fields = ('nome_completo', 'cpf', 'email')
    readonly_fields = ('data_criacao', 'data_atualizacao')

    fieldsets = (
        ('Informações da Reserva', {
            'fields': ('sala_de_reserva', 'data_reserva', 'hora_entrada', 'hora_saida')
        }),
        ('Dados do Cliente', {
            'fields': ('nome_completo', 'cpf', 'email')
        }),
        ('Controle Interno', {
            'fields': ('data_criacao', 'data_atualizacao')
        }),
    )

