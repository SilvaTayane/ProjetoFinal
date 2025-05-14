from django.db import models
from salas.models import Sala

# Create your models here.
class Equipamento(models.Model):
 sala = models.ForeignKey(Sala, on_delete=models.CASCADE)