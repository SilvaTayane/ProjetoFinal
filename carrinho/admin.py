from django.contrib import admin

from carrinho.models import CarItem, Carrinho

# Register your models here.
admin.site.register(Carrinho)
admin.site.register(CarItem)