import django_filters
from django_filters import CharFilter, NumberFilter, BooleanFilter

from .models import *

class PropriedadeFilter(django_filters.FilterSet):
    genero = (
        ('Masculino','Masculino'),
        ('Feminino','Feminino'),
        ('Qualquer','Qualquer'),
    )

    preco__gt = django_filters.NumberFilter(field_name='preco', lookup_expr='gt', label='Preço maior que')
    preco__lt = django_filters.NumberFilter(field_name='preco', lookup_expr='lt', label='Preço menor que')

    titulo = CharFilter(field_name='titulo', lookup_expr='icontains', label='Título')
    local = CharFilter(field_name='local', lookup_expr='icontains', label='Local')
    
    class Meta:
        model = Propriedade
        fields = ('titulo', 'local','limpeza','internet','fumador','pets','genero')