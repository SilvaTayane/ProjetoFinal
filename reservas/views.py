from django.shortcuts import render

# Create your views here.
def VisualizarReserva(request):
    return render(request, 'reserva.html')