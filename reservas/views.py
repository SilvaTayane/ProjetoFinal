from django.shortcuts import render
from .models import Reserva

# Create your views here.
def VisualizarReserva(request):
    reserva = Reserva.objects.filter()
    return render(request, 'reserva.html', {'reserva': reserva})