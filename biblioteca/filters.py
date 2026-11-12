"""Filtros (django-filter) usados nas listagens."""

import django_filters
from django import forms

from .models import Emprestimo, Livro, Reserva


class LivroFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr="icontains", label="Título")
    autor = django_filters.CharFilter(lookup_expr="icontains", label="Autor")
    categoria = django_filters.CharFilter(lookup_expr="icontains", label="Categoria")
    disponibilidade = django_filters.ChoiceFilter(
        label="Disponibilidade",
        choices=[("sim", "Com exemplares disponíveis"), ("nao", "Sem exemplares")],
        empty_label="Todos",
        method="filtrar_disponibilidade",
    )

    class Meta:
        model = Livro
        fields = ["titulo", "autor", "categoria", "disponibilidade"]

    def filtrar_disponibilidade(self, queryset, name, value):
        if value == "sim":
            return queryset.filter(quantidade_disponivel__gt=0)
        if value == "nao":
            return queryset.filter(quantidade_disponivel=0)
        return queryset


class EmprestimoFilter(django_filters.FilterSet):
    livro = django_filters.CharFilter(
        field_name="livro__titulo", lookup_expr="icontains", label="Livro"
    )
    status = django_filters.ChoiceFilter(
        choices=Emprestimo.STATUS_CHOICES, empty_label="Todos", label="Status"
    )
    data_devolucao_prevista = django_filters.DateFromToRangeFilter(
        label="Devolução prevista (de / até)",
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}),
    )

    class Meta:
        model = Emprestimo
        fields = ["livro", "status", "data_devolucao_prevista"]


class ReservaFilter(django_filters.FilterSet):
    livro = django_filters.CharFilter(
        field_name="livro__titulo", lookup_expr="icontains", label="Livro"
    )
    status = django_filters.ChoiceFilter(
        choices=Reserva.STATUS_CHOICES, empty_label="Todos", label="Status"
    )

    class Meta:
        model = Reserva
        fields = ["livro", "status"]
