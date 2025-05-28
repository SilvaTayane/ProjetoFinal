from django.shortcuts import render
from .models import Plano

# Create your views here.
def VisualizarPlanos(request):
    planos = Plano.objects.all()
    return render(request, 'planos.html', {'planos': planos})