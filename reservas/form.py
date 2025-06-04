from django import forms
from .models import Reserva
from datetime import date  # Importamos date para verificação da data atual

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['sala_de_reserva', 'nome_completo', 'email', 'cpf', 
                 'data_reserva', 'hora_entrada', 'hora_saida']
        
        # Personalizando os widgets
        widgets = {
            'data_reserva': forms.DateInput(attrs={'type': 'date'}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time'}),
            'hora_saida': forms.TimeInput(attrs={'type': 'time'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
        }
        
        # Personalizando os labels
        labels = {
            'sala_de_reserva': 'Sala para Reserva',
            'nome_completo': 'Nome Completo',
            'data_reserva': 'Data da Reserva',
            'hora_entrada': 'Hora de Entrada',
            'hora_saida': 'Hora de Saída',
        }
        
        # Adicionando help_texts
        help_texts = {
            'data_reserva': 'Selecione a data desejada',
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['CPF']
        # Validação simples do formato do CPF
        if not len(cpf) == 14 or not cpf[3] == '.' or not cpf[7] == '.' or not cpf[11] == '-':
            raise forms.ValidationError("CPF deve estar no formato 000.000.000-00")
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        hora_entrada = cleaned_data.get('hora_entrada')
        hora_saida = cleaned_data.get('hora_saida')
        data_reserva = cleaned_data.get('data_reserva')
        sala_de_reserva = cleaned_data.get('sala_de_reserva')

        # Verifica se a hora de saída é depois da hora de entrada
        if hora_entrada and hora_saida and hora_saida <= hora_entrada:
            raise forms.ValidationError("A hora de saída deve ser após a hora de entrada")

        # Verifica se a data da reserva não é no passado (usando date.today())
        if data_reserva and data_reserva < date.today():
            raise forms.ValidationError("Não é possível reservar para datas passadas")

        # Verifica se a sala já está reservada no mesmo horário
        if sala_de_reserva and data_reserva and hora_entrada and hora_saida:
            conflitos = Reserva.objects.filter(
                sala_de_reserva=sala_de_reserva,
                data_reserva=data_reserva,
                hora_entrada__lt=hora_saida,
                hora_saida__gt=hora_entrada
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if conflitos.exists():
                raise forms.ValidationError("A sala já está reservada neste horário")

        return cleaned_data