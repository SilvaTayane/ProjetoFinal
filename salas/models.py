from django.db import models

# Create your models here.
class Sala(models.Model):
    nome_sala =      models.CharField(max_length=50)
    slug =           models.SlugField(max_length=50, unique=True)
    capacidade =     models.PositiveIntegerField()
    sala_imagem =    models.ImageField(upload_to='media/fotos', blank=True)
    preco_por_hora = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    descricao_sala = models.TextField()




    def __str__(self):
        return self.nome_sala