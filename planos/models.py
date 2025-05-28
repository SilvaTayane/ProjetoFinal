from django.db import models

class Plano(models.Model):
    TIPO_PLANO_CHOICES = [
        ('semanal', 'Semanal'),
        ('mensal', 'Mensal'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    ]

    tipo_de_sala = models.CharField(max_length=100, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    imagens =         models.ImageField(upload_to='fotos/planos',blank=True)
    tipo_plano = models.CharField(max_length=10, choices=TIPO_PLANO_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_de_sala} - {self.tipo_plano}"
