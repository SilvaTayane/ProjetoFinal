from django.shortcuts import render
from .models import Planos

# Create your views here.
def VisualizarPlanos(request):
    planos = Planos.objects.all()
    return render(request, 'planos.html', {'planos': planos})