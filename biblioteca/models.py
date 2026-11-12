from django.conf import settings
from django.db import models
from django.urls import reverse


class Livro(models.Model):
    """Catálogo de livros da biblioteca (não possui FK para User)."""

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    categoria = models.CharField(max_length=100, blank=True)
    editora = models.CharField(max_length=150, blank=True)
    ano_publicacao = models.PositiveIntegerField(null=True, blank=True)
    quantidade_total = models.PositiveIntegerField(default=1)
    quantidade_disponivel = models.PositiveIntegerField(default=1)
    capa = models.ImageField(
        "Capa do livro",
        upload_to="capas_livros/",
        null=True,
        blank=True,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.titulo} ({self.autor})"

    def get_absolute_url(self):
        return reverse("biblioteca:livro_detail", kwargs={"pk": self.pk})


class Emprestimo(models.Model):
    """Empréstimo de um livro. Possui FK para User (usuário)."""

    STATUS_CHOICES = [
        ("ATIVO", "Ativo"),
        ("DEVOLVIDO", "Devolvido"),
        ("ATRASADO", "Atrasado"),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="emprestimos")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="emprestimos",
    )
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao_prevista = models.DateField()
    data_devolucao_real = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ATIVO")

    class Meta:
        ordering = ["-data_emprestimo"]

    def __str__(self):
        return f"Empréstimo de {self.livro.titulo} - {self.usuario}"

    def get_absolute_url(self):
        return reverse("biblioteca:emprestimo_detail", kwargs={"pk": self.pk})


class Reserva(models.Model):
    """Reserva de um livro. Possui FK para User (usuário)."""

    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("ATENDIDA", "Atendida"),
        ("CANCELADA", "Cancelada"),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="reservas")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservas",
    )
    data_reserva = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDENTE")

    class Meta:
        ordering = ["-data_reserva"]

    def __str__(self):
        return f"Reserva de {self.livro.titulo} - {self.usuario}"

    def get_absolute_url(self):
        return reverse("biblioteca:reserva_detail", kwargs={"pk": self.pk})
