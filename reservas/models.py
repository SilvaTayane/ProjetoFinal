from django.db import models
from salas.models import Sala
from planos.models import Plano
'''
# Adicione este modelo se ainda não existir
class Plano(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Plano")
    descricao = models.TextField(verbose_name="Descrição")
    preco = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        verbose_name="Preço Mensal"
    )
    beneficios = models.TextField(
        verbose_name="Benefícios Incluídos",
        blank=True,
        help_text="Lista os benefícios deste plano"
    )

    class Meta:
        verbose_name = "Plano"
        verbose_name_plural = "Planos"
        ordering = ['preco']
    def __str__(self):
        return f"{self.nome} (R${self.preco}/mês)"'''


class Reserva(models.Model):
    sala_de_reserva = models.ForeignKey(
        Sala, 
        on_delete=models.CASCADE,
        verbose_name="Sala Reservada"
    )
    nome_completo = models.CharField(
        max_length=200,
        verbose_name="Nome Completo"
    )
    email = models.EmailField(
        verbose_name="E-mail"
    )
    cpf = models.CharField(
        max_length=14,
        verbose_name="CPF",
        help_text="Formato: 000.000.000-00"
    )
    data_reserva = models.DateField(
        verbose_name="Data da Reserva"
    )
    hora_entrada = models.TimeField(
        verbose_name="Hora de Entrada"
    )
    hora_saida = models.TimeField(
        verbose_name="Hora de Saída"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    # Novo campo para o plano (opcional)
    plano = models.ForeignKey(
        Plano,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Plano Associado",
        help_text="Plano de assinatura escolhido (se aplicável)"
    )
    
    # Novo campo para marcar se é assinatura
    assinatura_plano = models.BooleanField(
        default=False,
        verbose_name="Assinar Plano?",
        help_text="Marcar se deseja associar um plano à reserva"
    )

    class Meta:
        ordering = ['data_reserva']
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        plano_info = f" - Plano: {self.plano.tipo_plano}" if self.plano else ""
        return f"{self.nome_completo} - {self.sala_de_reserva} em {self.data_reserva}{plano_info}"
    
    def save(self, *args, **kwargs):
        # Garante que se não for assinatura, o plano seja None
        if not self.assinatura_plano:
            self.plano = None
        
        self.full_clean()
        super().save(*args, **kwargs)