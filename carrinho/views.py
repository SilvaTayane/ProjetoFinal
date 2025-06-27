from django.shortcuts import redirect, render, get_object_or_404
from carrinho.models import Carrinho, CarItem
from produtos.models import Produto
from django.core.exceptions import ObjectDoesNotExist

app_name = 'carrinho' 

def get_car_id(request):
    """Obtém ou cria um ID de sessão para o carrinho"""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def visualizar_carrinho(request):
    try:
        carrinho = Carrinho.objects.get(car_id=get_car_id(request))
        car_items = CarItem.objects.filter(carrinho=carrinho, esta_disponivel=True)
        
        for item in car_items:
            item.subtotal = float(item.produto.preco) * item.quantidade
        
        total = sum(item.subtotal for item in car_items)
        quantidade = sum(item.quantidade for item in car_items)
        
        # Formata para 2 casas decimais
        total = round(total, 2)
        
    except ObjectDoesNotExist:
        car_items = None
        total = 0.00
        quantidade = 0

    contexto = {
        'car_items': car_items,
        'total': total,
        'quantidade': quantidade,
    }
    return render(request, 'carrinho.html', contexto)

def adicionar_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    try:
        carrinho = Carrinho.objects.get(car_id=get_car_id(request))
    except Carrinho.DoesNotExist:
        carrinho = Carrinho.objects.create(car_id=get_car_id(request))
        request.session.modified = True  # Importante para persistir a sessão
    
    car_item, created = CarItem.objects.get_or_create(
        produto=produto,
        carrinho=carrinho,
        defaults={'quantidade': 1}
    )
    
    if not created:
        car_item.quantidade += 1
        car_item.save()
    
    return redirect('carrinho')

def remover_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho = Carrinho.objects.get(car_id=get_car_id(request))
    
    try:
        car_item = CarItem.objects.get(
            produto=produto,
            carrinho=carrinho
        )
        if car_item.quantidade > 1:
            car_item.quantidade -= 1
            car_item.save()
        else:
            car_item.delete()
    except CarItem.DoesNotExist:
        pass
    
    return redirect('carrinho')

def remover_item_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho = Carrinho.objects.get(car_id=get_car_id(request))
    
    CarItem.objects.filter(
        produto=produto,
        carrinho=carrinho
    ).delete()
    
    return redirect('carrinho')