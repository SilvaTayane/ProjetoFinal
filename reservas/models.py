from django.db import models
from django.conf import settings
from salas.models import Sala

# Create your models here.
class Reserva(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    data = models.DateField()
    inicio_hora = models.TimeField
    final_hora = models.TimeField


    def __str__(self):
        return self.sala

