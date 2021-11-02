from django import forms
from django.core.validators import RegexValidator


class ProcurarForm(forms.Form):
    container_number = forms.CharField(
        max_length=11,
        required=True,
        validators=[
            RegexValidator("[A-Z]{4}\d{7}", message="Número do container invalido")
        ],
        label="",
    )
