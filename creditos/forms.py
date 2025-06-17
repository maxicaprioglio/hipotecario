import re
from django import forms

class FormularioCredito(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        max_length=100,
        error_messages={
            'required': 'El nombre es obligatorio.',
            'max_length': 'El nombre no puede superar los 100 caracteres.'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control texto-formulario',
            'placeholder': 'Nombre y apellido',
            'id': 'nombre',
            'required': 'required'
        })
    )
    edad = forms.IntegerField(
        label='Edad',
        min_value=18,
        error_messages={
            'required': 'La edad es obligatoria.',
            'min_value': 'Debes ser mayor de 18 años para solicitar un crédito.'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control texto-formulario',
            'placeholder': 'Edad',
            'id': 'edad',
            'required': 'required',
            'min': '0',
            'max': '120'
        })
    )
    email = forms.EmailField(
        label='Email',
        error_messages={
            'required': 'El email es obligatorio.',
            'invalid': 'Ingresa un email válido.'
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control texto-formulario',
            'placeholder': 'Correo electrónico',
            'id': 'email',
            'required': 'required'
        })
    )
    celular = forms.CharField(
        label='Celular',
        min_length=8,
        max_length=15,
        error_messages={
            'required': 'El celular es obligatorio.',
            'min_length': 'El número de celular debe tener al menos 8 dígitos.',
            'max_length': 'El número de celular no puede tener más de 15 dígitos.'
        },    
        widget=forms.TextInput(attrs={
            'class': 'form-control texto-formulario',
            'placeholder': 'Celular',
            'id': 'celular',
            'required': 'required',
            'pattern': '[0-9\\s]{8,15}',
        })
    )
    tipo_empleo = forms.ChoiceField(
        choices=[
            ('', 'Tipo de empleo'),
            ('1', 'Relación de dependencia'),
            ('2', 'Independiente'),
        ],
        label='Tipo de Empleo',
        error_messages={
            'required': 'El tipo de empleo es obligatorio.'
        },
        widget=forms.Select(attrs={
            'class': 'form-select texto-formulario',
            'aria-label': 'Tipo de empleo',
            'id': 'tipo_empleo',
            'required': 'required'
        })
    )
    antiguedad_laboral = forms.IntegerField(
        label='Antigüedad Laboral (en años)',
        error_messages={
            'required': 'La antigüedad laboral es obligatoria.'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control texto-formulario',
            'id': 'antiguedad_laboral',
            'placeholder': 'Antigüedad laboral',
            'min': '0',
            'max': '80',
            'required': 'required',
        })
    )
    bruto = forms.IntegerField(
        label='Ingreso Bruto Mensual',
        min_value=0,
        error_messages={
            'required': 'El ingreso bruto mensual es obligatorio.',
            'min_value': 'El ingreso bruto mensual debe ser mayor a 0.'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control texto-formulario',
            'id': 'bruto',
            'placeholder': 'Ingreso bruto mensual (en pesos)',
            'required': 'required',
            'min': '0'
        })
    )
    propiedad = forms.IntegerField(
        label='Propiedad',
        min_value=1,
        error_messages={
            'required': 'El valor de la propiedad es obligatorio.',
            'min_value': 'El valor de la propiedad debe ser mayor a 0.'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control texto-formulario',
            'id': 'propiedad',
            'placeholder': 'Valor de la propiedad (en pesos)',
            'required': 'required',
            'min': '0'
        })
    )
    ahorros = forms.IntegerField(
        label='Ahorros Disponibles',
        min_value=0,
        error_messages={
            'required': 'Los ahorros disponibles son obligatorios.',
            'min_value': 'Los ahorros no pueden ser negativos.'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control texto-formulario',
            'id': 'ahorros',
            'placeholder': 'Ahorros disponibles (en pesos)',
            'required': 'required',
            'min': '0'
        })
    )
    plazo = forms.IntegerField(
        label='Plazo (en años)',
        min_value=1,
        max_value=30,
        error_messages={
            'required': 'El plazo es obligatorio.',
            'min_value': 'El plazo debe ser mayor a 0.',
            'max_value': 'El plazo no puede ser mayor a 30 años.'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control texto-formulario',
            'id': 'plazo',
            'placeholder': 'Plazo de financiamiento',
            'required': 'required',
            'min': '1',
            'max': '30'
        })
    )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo debe contener letras y espacios.")
        return nombre

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if not celular.isdigit():
            raise forms.ValidationError("El número de celular solo debe contener dígitos.")
        return celular

    def clean_antiguedad_laboral(self):
        antiguedad = self.cleaned_data.get('antiguedad_laboral')
        tipo_empleo = self.cleaned_data.get('tipo_empleo')

        if antiguedad is not None and tipo_empleo:
            if tipo_empleo == '1' and antiguedad < 1:
                raise forms.ValidationError("Debes tener al menos 1 año de antigüedad laboral para relación de dependencia.")
            elif tipo_empleo == '2' and antiguedad < 2:
                raise forms.ValidationError("Debes tener al menos 2 años de antigüedad laboral si sos independiente.")
        return antiguedad

    def clean(self):
        cleaned_data = super().clean()
        propiedad = cleaned_data.get('propiedad')
        ahorros = cleaned_data.get('ahorros')
        plazo = cleaned_data.get('plazo')
        bruto = cleaned_data.get('bruto')

        if propiedad is not None and ahorros is not None:
            if ahorros > propiedad:
                self.add_error('ahorros', "Los ahorros no pueden ser mayores al valor de la propiedad.")
            if ahorros < (propiedad * 0.2):
                self.add_error('ahorros', "Los ahorros deben ser al menos el 20% del valor de la propiedad.")

        if propiedad and ahorros and plazo and bruto:
            cuota_mensual = ((propiedad - ahorros) * 1.065) / (plazo * 12) # 6.5% de interes al prestamo
            if cuota_mensual > ((bruto * 0.8) * 0.3): # 20% de retenciones al sueldo bruto
                self.add_error('plazo', "La cuota mensual no puede ser mayor al 30% de tu ingreso neto mensual. Revisa el plazo o el valor de la propiedad.")

        return cleaned_data
