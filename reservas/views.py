from django.shortcuts import render
from datetime import datetime
from reservas.form import ReservaForm



def VisualizarReserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()
            return render(request, 'reserva.html')
    else:
        form = ReservaForm(initial={
            'data_reserva': datetime.now().date()  # Usando datetime.now()
        })
    
    return render(request, 'reserva.html', {'form': form})