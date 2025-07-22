from django.db import models

# Create your models here.
class Produto(models.Model):
    produto_nome =    models.CharField(max_length=200, unique=True)
    slug =            models.SlugField(max_length=200, unique=True)
    descricao =       models.CharField(max_length=200, unique=False)
    preco =           models.DecimalField(max_digits=12, decimal_places=2)
    imagens =         models.ImageField(upload_to='fotos/produtos',blank=True)
    estoque =         models.IntegerField()
    esta_disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.produto_nome
    