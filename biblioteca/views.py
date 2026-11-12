import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from .filters import EmprestimoFilter, LivroFilter, ReservaFilter
from .forms import EmprestimoForm, LivroForm, RecuperarUsuarioForm, ReservaForm
from .models import Emprestimo, Livro, Reserva

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Mixins reutilizáveis
# ---------------------------------------------------------------------------
class MensagemSucessoMixin:
    """Exibe uma mensagem (framework de mensagens) após Create/Update/Delete.

    Defina ``mensagem_sucesso`` na view; use ``{objeto}`` para o registro.
    """

    mensagem_sucesso = "Operação realizada com sucesso."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, self.mensagem_sucesso.format(objeto=self.object)
        )
        return response


class ExclusaoProtegidaMixin:
    """Evita erro 500 ao excluir registro referenciado por outro (PROTECT)."""

    mensagem_protegido = "Não foi possível excluir: o registro está em uso."

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, self.mensagem_protegido)
            return redirect(self.success_url)


class UsuarioFiltradoMixin:
    """Restringe o queryset aos registros do usuário logado.

    Vale para listar, visualizar, alterar e excluir: como todas as views usam
    ``get_queryset``, um registro de outro usuário resulta em 404.
    """

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


class FiltroListMixin:
    """Aplica um ``django_filters.FilterSet`` a uma ListView."""

    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(
            self.request.GET or None, queryset=queryset, request=self.request
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


# ---------------------------------------------------------------------------
# Livros (catálogo compartilhado)
# ---------------------------------------------------------------------------
class LivroListView(LoginRequiredMixin, FiltroListMixin, ListView):
    model = Livro
    filterset_class = LivroFilter
    template_name = "biblioteca/livro_list.html"
    context_object_name = "livros"
    paginate_by = 20


class LivroDetailView(LoginRequiredMixin, DetailView):
    model = Livro
    template_name = "biblioteca/livro_detail.html"
    context_object_name = "livro"


class LivroCreateView(LoginRequiredMixin, MensagemSucessoMixin, CreateView):
    mensagem_sucesso = 'Livro "{objeto}" cadastrado com sucesso.'
    model = Livro
    form_class = LivroForm
    template_name = "biblioteca/livro_form.html"
    success_url = reverse_lazy("biblioteca:livro_list")


class LivroUpdateView(LoginRequiredMixin, MensagemSucessoMixin, UpdateView):
    mensagem_sucesso = 'Livro "{objeto}" atualizado com sucesso.'
    model = Livro
    form_class = LivroForm
    template_name = "biblioteca/livro_form.html"
    success_url = reverse_lazy("biblioteca:livro_list")


class LivroDeleteView(
    LoginRequiredMixin, ExclusaoProtegidaMixin, MensagemSucessoMixin, DeleteView
):
    mensagem_sucesso = 'Livro "{objeto}" excluído com sucesso.'
    mensagem_protegido = "Este livro possui empréstimos ou reservas e não pode ser excluído."
    model = Livro
    template_name = "biblioteca/livro_confirm_delete.html"
    success_url = reverse_lazy("biblioteca:livro_list")

# ---------------------------------------------------------------------------
# Empréstimos (registros pertencem ao usuário que os cadastrou)
# ---------------------------------------------------------------------------
class EmprestimoListView(
    LoginRequiredMixin, FiltroListMixin, UsuarioFiltradoMixin, ListView
):
    model = Emprestimo
    filterset_class = EmprestimoFilter
    template_name = "biblioteca/emprestimo_list.html"
    context_object_name = "emprestimos"
    paginate_by = 20


class EmprestimoDetailView(LoginRequiredMixin, UsuarioFiltradoMixin, DetailView):
    model = Emprestimo
    template_name = "biblioteca/emprestimo_detail.html"
    context_object_name = "emprestimo"


class EmprestimoCreateView(LoginRequiredMixin, MensagemSucessoMixin, CreateView):
    mensagem_sucesso = 'Empréstimo de "{objeto.livro.titulo}" cadastrado(a) com sucesso.'
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = "biblioteca/emprestimo_form.html"
    success_url = reverse_lazy("biblioteca:emprestimo_list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class EmprestimoUpdateView(
    LoginRequiredMixin, UsuarioFiltradoMixin, MensagemSucessoMixin, UpdateView
):
    mensagem_sucesso = 'Empréstimo de "{objeto.livro.titulo}" atualizado(a) com sucesso.'
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = "biblioteca/emprestimo_form.html"
    success_url = reverse_lazy("biblioteca:emprestimo_list")


class EmprestimoDeleteView(
    LoginRequiredMixin, UsuarioFiltradoMixin, MensagemSucessoMixin, DeleteView
):
    mensagem_sucesso = 'Empréstimo de "{objeto.livro.titulo}" excluído(a) com sucesso.'
    model = Emprestimo
    template_name = "biblioteca/emprestimo_confirm_delete.html"
    success_url = reverse_lazy("biblioteca:emprestimo_list")

# ---------------------------------------------------------------------------
# Reservas (registros pertencem ao usuário que os cadastrou)
# ---------------------------------------------------------------------------
class ReservaListView(
    LoginRequiredMixin, FiltroListMixin, UsuarioFiltradoMixin, ListView
):
    model = Reserva
    filterset_class = ReservaFilter
    template_name = "biblioteca/reserva_list.html"
    context_object_name = "reservas"
    paginate_by = 20


class ReservaDetailView(LoginRequiredMixin, UsuarioFiltradoMixin, DetailView):
    model = Reserva
    template_name = "biblioteca/reserva_detail.html"
    context_object_name = "reserva"


class ReservaCreateView(LoginRequiredMixin, MensagemSucessoMixin, CreateView):
    mensagem_sucesso = 'Reserva de "{objeto.livro.titulo}" cadastrado(a) com sucesso.'
    model = Reserva
    form_class = ReservaForm
    template_name = "biblioteca/reserva_form.html"
    success_url = reverse_lazy("biblioteca:reserva_list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ReservaUpdateView(
    LoginRequiredMixin, UsuarioFiltradoMixin, MensagemSucessoMixin, UpdateView
):
    mensagem_sucesso = 'Reserva de "{objeto.livro.titulo}" atualizado(a) com sucesso.'
    model = Reserva
    form_class = ReservaForm
    template_name = "biblioteca/reserva_form.html"
    success_url = reverse_lazy("biblioteca:reserva_list")


class ReservaDeleteView(
    LoginRequiredMixin, UsuarioFiltradoMixin, MensagemSucessoMixin, DeleteView
):
    mensagem_sucesso = 'Reserva de "{objeto.livro.titulo}" excluído(a) com sucesso.'
    model = Reserva
    template_name = "biblioteca/reserva_confirm_delete.html"
    success_url = reverse_lazy("biblioteca:reserva_list")


# ---------------------------------------------------------------------------
# Recuperação de usuário por e-mail (a de senha usa as views do Django)
# ---------------------------------------------------------------------------
class RecuperarUsuarioView(FormView):
    template_name = "registration/usuario_recuperar_form.html"
    form_class = RecuperarUsuarioForm
    success_url = reverse_lazy("biblioteca:usuario_recuperar_done")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        usuarios = get_user_model().objects.filter(email__iexact=email, is_active=True)
        # Sempre mostramos a mesma página de sucesso, existindo ou não o
        # e-mail, para não revelar quais e-mails estão cadastrados.
        if usuarios.exists():
            corpo = render_to_string(
                "registration/usuario_recuperar_email.txt",
                {
                    "usernames": [u.get_username() for u in usuarios],
                    "login_url": self.request.build_absolute_uri(
                        reverse_lazy("biblioteca:login")
                    ),
                },
            )
            try:
                send_mail(
                    "Recuperação de usuário - Biblioteca",
                    corpo,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
            except Exception:  # SMTP fora do ar, credenciais erradas etc.
                logger.exception("Falha ao enviar e-mail de recuperação de usuário")
                messages.error(
                    self.request,
                    "Não foi possível enviar o e-mail agora. Tente novamente mais tarde.",
                )
                return self.form_invalid(form)
        return super().form_valid(form)


class RecuperarUsuarioDoneView(TemplateView):
    template_name = "registration/usuario_recuperar_done.html"
