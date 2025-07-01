from django.urls import path
from . import views




urlpatterns = [
    path('', views.visualizar_carrinho, name='carrinho'),
    path('adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('remover_item/<int:produto_id>/', views.remover_item_carrinho, name='remover_item_carrinho'),
    path('qrcode/total/<str:total>/', views.gerar_qrcode_total, name='qrcode_total'),
]