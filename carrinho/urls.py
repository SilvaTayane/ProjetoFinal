from django.urls import path
from carrinho import views
from . import views 


urlpatterns = [   
    path('', views.visualizarCarrinho, name='carrinho'), 
    ]