# Generated by Django 5.2.1 on 2025-05-27 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_reserva_cpf_reserva_email_reserva_final_hora_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reserva',
        ),
    ]
