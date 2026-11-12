from django import forms
from django.contrib.auth import get_user_model

from .models import Emprestimo, Livro, Reserva


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            "titulo",
            "autor",
            "isbn",
            "categoria",
            "editora",
            "ano_publicacao",
            "quantidade_total",
            "quantidade_disponivel",
            "capa",
        ]


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ["livro", "data_devolucao_prevista", "status"]
        widgets = {
            "livro": forms.Select(attrs={"class": "js-select2"}),
            "data_devolucao_prevista": forms.DateInput(attrs={"type": "date"}),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["livro", "status"]
        widgets = {
            "livro": forms.Select(attrs={"class": "js-select2"}),
        }


class RecuperarUsuarioForm(forms.Form):
    """Pede o e-mail para enviar o(s) nome(s) de usuário cadastrado(s)."""

    email = forms.EmailField(label="E-mail cadastrado")
