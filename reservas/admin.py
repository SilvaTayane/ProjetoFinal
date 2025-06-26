from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'sala_de_reserva', 'data_reserva', 'hora_entrada', 'hora_saida')
    list_filter = ('sala_de_reserva', 'data_reserva')
    search_fields = ('nome_completo', 'sala_de_reserva__nome')  # Ajuste conforme o campo real
    ordering = ('data_reserva',)
