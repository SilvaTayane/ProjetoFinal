from django import forms
from .models import Reserva, Plano
from datetime import date

class ReservaForm(forms.ModelForm):
    assinatura_plano = forms.BooleanField(
        required=False,
        label='Deseja assinar um Plano?',
        widget=forms.CheckboxInput(attrs={
            'class': 'styled-checkbox',
            'id': 'assinaturaPlanoCheckbox'
        })
    )
    
    plano = forms.ModelChoiceField(
        queryset=Plano.objects.all(),
        required=False,
        label="Escolha seu plano",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_plano'
        })
    )

    class Meta:
        model = Reserva
        fields = ['sala_de_reserva', 'nome_completo', 'email', 'cpf', 
                 'data_reserva', 'hora_entrada', 'hora_saida', 'assinatura_plano', 'plano']
        
        widgets = {
            'data_reserva': forms.DateInput(attrs={'type': 'date'}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time'}),
            'hora_saida': forms.TimeInput(attrs={'type': 'time'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
        }
        
        labels = {
            'sala_de_reserva': 'Sala para Reserva',
            'nome_completo': 'Nome Completo',
            'data_reserva': 'Data da Reserva',
            'hora_entrada': 'Hora de Entrada',
            'hora_saida': 'Hora de Saída',
        }
        
        help_texts = {
            'data_reserva': 'Selecione a data desejada',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se for uma instância existente e tiver plano, marca o checkbox
        if self.instance and self.instance.plano:
            self.initial['assinatura_plano'] = True

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf') 
        if not len(cpf) == 14 or not cpf[3] == '.' or not cpf[7] == '.' or not cpf[11] == '-':
            raise forms.ValidationError("CPF deve estar no formato 000.000.000-00")
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        hora_entrada = cleaned_data.get('hora_entrada')
        hora_saida = cleaned_data.get('hora_saida')
        data_reserva = cleaned_data.get('data_reserva')
        sala_de_reserva = cleaned_data.get('sala_de_reserva')
        assinatura_plano = cleaned_data.get('assinatura_plano')
        plano = cleaned_data.get('plano')

        # Validação do plano se o checkbox estiver marcado
        if assinatura_plano and not plano:
            self.add_error('plano', "Por favor, selecione um plano quando optar por assinar")

        # Verifica se a hora de saída é depois da hora de entrada
        if hora_entrada and hora_saida and hora_saida <= hora_entrada:
            raise forms.ValidationError("A hora de saída deve ser após a hora de entrada")

        # Verifica se a data da reserva não é no passado
        if data_reserva and data_reserva < date.today():
            raise forms.ValidationError("Não é possível reservar para datas passadas")

        # Verifica conflitos de reserva
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

    def save(self, commit=True):
        reserva = super().save(commit=False)
        if not self.cleaned_data.get('assinatura_plano'):
            reserva.plano = None  # Remove o plano se o checkbox não estiver marcado
        
        if commit:
            reserva.save()
            self.save_m2m()
        
        return reserva