# from django import forms
# from django.core.validators import RegexValidator
# from django.core.exceptions import ValidationError
# from datetime import date, time, datetime

# # Create your models here.
# class ReservaForm(forms.ModelForm):
#     class Meta:
#         fields = ['sala', 'data', 'inicio_hora', 'final_hora', 'cpf', 'nome', 'email']
#         widgets = {
#             'data': forms.DateInput(attrs={'type': 'date'}),
#             'inicio_hora': forms.TimeInput(attrs={'type': 'time'}),
#             'final_hora': forms.TimeInput(attrs={'type': 'time'}),
#             'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Definir valores iniciais
#         self.fields['data'].initial = date.today()
#         self.fields['inicio_hora'].initial = time(9, 0)  # 09:00
#         self.fields['final_hora'].initial = time(18, 0)  # 18:00
        
#         # Melhorar a exibição do campo de sala
#         self.fields['sala'].queryset = Sala.objects.all().order_by('nome')
    
#     def clean_cpf(self):
#         cpf = self.cleaned_data.get('cpf')
#         if cpf:
#             # Validar formato do CPF (000.000.000-00)
#             cpf_validator = RegexValidator(
#                 regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
#                 message='CPF deve estar no formato 000.000.000-00'
#             )
#             try:
#                 cpf_validator(cpf)
#             except ValidationError:
#                 raise forms.ValidationError("Formato de CPF inválido. Use 000.000.000-00")
#         return cpf
    
#     def clean(self):
#         cleaned_data = super().clean()
#         data = cleaned_data.get('data')
#         inicio_hora = cleaned_data.get('inicio_hora')
#         final_hora = cleaned_data.get('final_hora')
#         sala = cleaned_data.get('sala')
        
#         # Verificar se a data não é no passado
#         if data and data < date.today():
#             raise forms.ValidationError("Não é possível fazer reservas para datas passadas.")
        
#         # Verificar se o horário final é depois do inicial
#         if inicio_hora and final_hora and final_hora <= inicio_hora:
#             raise forms.ValidationError("O horário final deve ser após o horário inicial.")
        
#         # Verificar se a sala está disponível
#         if sala and data and inicio_hora and final_hora:
#             conflitos = Reserva.objects.filter(
#                 sala=sala,
#                 data=data,
#             ).exclude(
#                 pk=self.instance.pk if self.instance else None
#             ).filter(
#                 inicio_hora__lt=final_hora,
#                 final_hora__gt=inicio_hora
#             )
            
#             if conflitos.exists():
#                 raise forms.ValidationError("Já existe uma reserva para esta sala no horário selecionado.")
        
#         return cleaned_data