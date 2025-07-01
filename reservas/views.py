from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from reservas.form import ReservaForm
from reservas.utils import enviar_email_confirmacao

def VisualizarReserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()

            # Envia email em background
            enviar_email_confirmacao(reserva)

            # Resposta AJAX rápida
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Reserva realizada com sucesso!',
                    'reserva_id': reserva.id
                })
            else:
                return render(request, 'reserva.html')
        else:
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