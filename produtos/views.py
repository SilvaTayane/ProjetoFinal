from django.shortcuts import render

from produtos.models import Produto

# Create your views here.
def visualizarloja(request, categoria_slug=None):
    produtos = Produto.objects.all()
    contexto = {
        'produtos' : produtos
    }
    return render(request, 'loja.html', contexto)