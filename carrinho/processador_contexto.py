from carrinho.models import CarItem, Carrinho
from carrinho.views import getCarId


def contador(request):
    contador = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            car = Carrinho.objects.filter(car_id = getCarId(request))
            car_items = CarItem.objects.all().filter(carrinho = car[:1])
            for car_item in car_items:
                contador += car_item.quantidade
        except Carrinho.DoesNotExist:
            contador = 0
    return dict(car_cont = contador)