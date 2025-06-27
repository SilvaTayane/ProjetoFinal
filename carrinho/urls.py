from django.urls import path
from . import views



urlpatterns = [
    path('', views.visualizar_carrinho, name='carrinho'),
    path('adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('remover/<int:produto_id>/', views.remover_carrinho, name='remover_carrinho'),
    path('remover-item/<int:produto_id>/', views.remover_item_carrinho, name='remover_item_carrinho'),
]