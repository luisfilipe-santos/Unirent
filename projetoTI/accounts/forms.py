from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import widgets
from django.forms import Textarea
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2','is_staff']

class InquilinoForm(ModelForm):
    class Meta:
        model = Inquilino
        fields = '__all__'
        exclude = ['user', 'propriedade','grupo']

class SenhorioForm(ModelForm):
    class Meta:
        model = Senhorio
        fields = '__all__'
        exclude = ['user','grupo']

class PropriedadeForm(ModelForm):
    class Meta:
        model = Propriedade
        fields = '__all__'
        exclude = ['senhorio']
        labels = {
        "local": "Morada",
        "titulo": "Título",
        "preco": "Preço Mensal",
        "preco_semestral": "Preço Semestral",
        "preco_anual": "Preço Anual",
        "area": "Área (m²)",
        "orientacao_solar": "Orientação Solar",
        "numero_quartos": "Quartos",
        "numero_inquilinos": "Inquilinos",
        }

class UpdatePropriedadeForm(ModelForm):
    class Meta:
        model = Propriedade
        fields = '__all__'
        exclude = ['senhorio',]
        labels = {
        "local": "Morada",
        "titulo": "Título",
        "preco": "Preço Mensal",
        "preco_semestral": "Preço Semestral",
        "preco_anual": "Preço Anual",
        "area": "Área (m²)",
        "orientacao_solar": "Orientação Solar",
        "numero_quartos": "Quartos",
        "numero_inquilinos": "Inquilinos",
        }


class OfertaInquilinoForm(ModelForm):
    class Meta:
        model = Oferta
        fields = ['periodo','quantidade']
        labels = {
        "periodo": "Tipo de contrato",
        "quantidade":"Duração contratual (meses/semestres/anos)",
        }


class ContratoForm(ModelForm):
    class Meta:
        model = Contrato
        exclude = ['propriedade','senhorio','inquilino','periodo','duracao','expirou','quantidade']

class RenovarContratoForm(ModelForm):
    class Meta:
        model = Contrato
        fields = ('quantidade',)
        exclude = ['propriedade','senhorio','inquilino','periodo','duracao','expirou']
        labels = {
        "quantidade": "Número"
        }

class RateForm(forms.ModelForm):
    rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = Review
        fields = ('text', 'rate')

class RateUserForm(forms.ModelForm):
    rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = ReviewUser
        fields = ('text', 'rate')