from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from reservas.form import ReservaForm

def VisualizarReserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()

            # Enviar e-mail
            try:
                send_mail(
                    subject='Confirmação de Reserva',
                    message=f"Olá {reserva.nome_completo}, sua reserva foi realizada com sucesso para o dia {reserva.data_reserva}.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[reserva.email],
                )
            except Exception as e:
                print("Erro ao enviar e-mail:", e)

            # Resposta AJAX
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
