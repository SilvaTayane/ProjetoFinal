from django.shortcuts import redirect, render

from carrinho.models import Carrinho, CarItem
from produtos.models import Produto
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# Verifica se o carrinho já existe na sessão
def getCarId(request):
    carSession = request.session.session_key
    if not carSession:
        carSession = request.session.create()
    return carSession

    
def visualizarCarrinho(request, total=0, quantidade=0, car_items=None):
    try:
        car = Carrinho.objects.get(car_id = getCarId(request))
        car_items = CarItem.objects.filter(carrinho = car, esta_disponivel=True)

    except ObjectDoesNotExist:
        pass

    contexto = {
        'car_items' : car_items
    }
    return render(request, 'carrinho.html', contexto)


# Adiciona o produto ao carrinho
def adicionarCarrinho(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    try:
        carrinho = Carrinho.objects.get(
            car_id=getCarId(request)
            )
    except Carrinho.DoesNotExist:
        carrinho = Carrinho.objects.create(
            car_id=getCarId(request)
            )
    carrinho.save()

    try:
        car_item = CarItem.objects.get(produto=produto, carrinho=carrinho)
        car_item.quantidade += 1 
        car_item.save()
    except CarItem.DoesNotExist:
        car_item = CarItem.objects.create(
            produto = produto,
            quantidade = 1,
            carrinho = carrinho,
        )
        car_item.save()
    return redirect('carrinho')