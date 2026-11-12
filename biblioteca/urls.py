from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = "biblioteca"

urlpatterns = [
    # raiz do site: redireciona para o catálogo (que exige login)
    path("", RedirectView.as_view(pattern_name="biblioteca:livro_list", permanent=False), name="home"),

    #Catalago
    path("livros/", views.LivroListView.as_view(), name="livro_list"),
    path("livros/<int:pk>/", views.LivroDetailView.as_view(), name="livro_detail"),
    path("livros/novo/", views.LivroCreateView.as_view(), name="livro_create"),
    path("livros/<int:pk>/editar/", views.LivroUpdateView.as_view(), name="livro_update"),
    path("livros/<int:pk>/excluir/", views.LivroDeleteView.as_view(), name="livro_delete"),

    # emprestimo
    path("emprestimos/", views.EmprestimoListView.as_view(), name="emprestimo_list"),
    path("emprestimos/<int:pk>/", views.EmprestimoDetailView.as_view(), name="emprestimo_detail"),
    path("emprestimos/novo/", views.EmprestimoCreateView.as_view(), name="emprestimo_create"),
    path("emprestimos/<int:pk>/editar/", views.EmprestimoUpdateView.as_view(), name="emprestimo_update"),
    path("emprestimos/<int:pk>/excluir/", views.EmprestimoDeleteView.as_view(), name="emprestimo_delete"),

    # reserva
    path("reservas/", views.ReservaListView.as_view(), name="reserva_list"),
    path("reservas/<int:pk>/", views.ReservaDetailView.as_view(), name="reserva_detail"),
    path("reservas/novo/", views.ReservaCreateView.as_view(), name="reserva_create"),
    path("reservas/<int:pk>/editar/", views.ReservaUpdateView.as_view(), name="reserva_update"),
    path("reservas/<int:pk>/excluir/", views.ReservaDeleteView.as_view(), name="reserva_delete"),

    # parte de login, logout, autenticação
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "senha/alterar/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
            success_url="/senha/alterada/",
        ),
        name="password_change",
    ),
    path(
        "senha/alterada/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),

    # recuperação de senha por e-mail (views nativas do Django)
    path(
        "senha/recuperar/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.txt",
            subject_template_name="registration/password_reset_subject.txt",
            success_url=reverse_lazy("biblioteca:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "senha/recuperar/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "senha/redefinir/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("biblioteca:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "senha/redefinida/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    # recuperação de usuário por e-mail
    path("usuario/recuperar/", views.RecuperarUsuarioView.as_view(), name="usuario_recuperar"),
    path(
        "usuario/recuperar/enviado/",
        views.RecuperarUsuarioDoneView.as_view(),
        name="usuario_recuperar_done",
    ),
]