from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from reservas.form import ReservaForm

def VisualizarReserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()
            
            # Verifica se é uma requisição AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Reserva realizada com sucesso!',
                    'reserva_id': reserva.id  # Opcional: retornar o ID da reserva
                })
            else:
                return render(request, 'reserva.html')
        else:
            # Se for AJAX, retorna os erros em formato JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors.get_json_data(),
                    'message': 'Por favor, corrija os erros no formulário.'
                }, status=400)
            else:
                return render(request, 'reserva.html', {'form': form})
    else:
        form = ReservaForm(initial={
            'data_reserva': datetime.now().date()
        })
    
    return render(request, 'reserva.html', {'form': form})