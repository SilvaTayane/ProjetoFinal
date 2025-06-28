import base64
from django.shortcuts import redirect, render, get_object_or_404
from carrinho.models import Carrinho, CarItem
from produtos.models import Produto
from django.core.exceptions import ObjectDoesNotExist
import qrcode
from io import BytesIO

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
        produto_carrinho = Produto.objects.all()

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
        'produto_carrinho':produto_carrinho,
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


def remover_item_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho = Carrinho.objects.get(car_id=get_car_id(request))
    
    CarItem.objects.filter(
        produto=produto,
        carrinho=carrinho
    ).delete()
    
    return redirect('carrinho')


def gerar_qrcode_total(request, total):
    # Gera o texto com o valor total
    total = float(total)

    # Cria o QR Code
    qr = qrcode.make(total)

    # Salva a imagem em memória
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Passa a imagem codificada para o template
    return render(request, 'qrcode_total.html', {'qr_code': img_base64, 'total': total})
