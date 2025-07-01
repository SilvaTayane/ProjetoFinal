# Para realizar o envio de email em segundo plano
import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def enviar_email_confirmacao(reserva):
    def envio():
        try:

            sala = reserva.sala_de_reserva

            context = {
                'nome': reserva.nome_completo,
                'data': reserva.data_reserva,
                'hora_entrada': reserva.hora_entrada,
                'hora_saida': reserva.hora_saida,
                'preco_por_hora': sala.preco_por_hora,
            }
            html_content = render_to_string('confirmacao_reserva.html', context)
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(
                subject='✅ Confirmação de Reserva - Haven Coworking',
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[reserva.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print("Erro ao enviar e-mail:", e)
    
    threading.Thread(target=envio).start()
