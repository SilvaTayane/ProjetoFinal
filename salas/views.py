from django.shortcuts import render
from .models import Sala

# Create your views here.


def VisualizarSalas(request):
    salas = Sala.objects.all()
    return render(request, 'salas.html', {'salas': salas})

    