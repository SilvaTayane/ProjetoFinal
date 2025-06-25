from django.db import models

from produtos.models import Produto

# Class que representará o ciclo de vida do carrinho.
class Carrinho(models.Model):
    car_id = models.CharField(max_length=250, blank=True)
    _data_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.car_id

class CarItem(models.Model):
    produto    = models.ForeignKey(Produto, on_delete=models.CASCADE)
    carrinho    = models.ForeignKey(Carrinho, on_delete=models.CASCADE, null=True)
    quantidade = models.IntegerField()
    esta_disponivel = models.BooleanField(default=True)

    def getSubtotal(self):
        return self.produto.preco * self.quantidade