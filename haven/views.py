from django.shortcuts import render

from produtos.models import Produto

def visualizarHome(request):
    return render(request, 'home.html')