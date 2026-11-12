from django.contrib import admin

from .models import Emprestimo, Livro, Reserva


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "isbn", "quantidade_disponivel", "quantidade_total")
    search_fields = ("titulo", "autor", "isbn")


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ("livro", "usuario", "data_emprestimo", "data_devolucao_prevista", "status")
    list_filter = ("status",)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("livro", "usuario", "data_reserva", "status")
    list_filter = ("status",)
