from django.db import models
from salas.models import Sala
# Create your models here.
class Reserva(models.Model):
    sala_de_reserva = models.ForeignKey(Sala, on_delete=models.CASCADE)
    nome_completo =   models.CharField(max_length=200)
    email =           models.EmailField()
    cpf =             models.CharField(max_length=14)  # Formatado como 000.000.000-00
    data_reserva =    models.DateField()
    hora_entrada =    models.TimeField()
    hora_saida =      models.TimeField()
    data_criacao =    models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['data_reserva']  # Ordem crescente


    def __str__(self):
        return f"{self.nome_completo} - {self.sala_de_reserva} em {self.data_reserva}"
    
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)