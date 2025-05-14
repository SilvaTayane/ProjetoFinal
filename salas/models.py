from django.db import models

# Create your models here.
class Sala(models.Model):
    nome_sala = models.CharField(max_length=50)
    capacidade = models.IntegerField()
    sala_imagem =models.ImageField(upload_to='fotos/equipamentos')
    slug = models.SlugField(max_length=50, unique=True)
    descricao_sala = models.TextField()




    def __str__(self):
        return self.nome_sala