"""Tags para paginação que preservam os filtros do django-filter.

Problema: um link ``?page=2`` descarta os parâmetros do filtro
(``?titulo=dom&page=2``). A tag ``url_replace`` copia a query string atual e
troca apenas os parâmetros informados.

Uso:
    {% load paginacao %}
    <a href="?{% url_replace page=3 %}">3</a>
    {% paginacao %}          {# renderiza a barra de paginação completa #}
"""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """Devolve a query string atual com os parâmetros de ``kwargs`` trocados."""
    query = context["request"].GET.copy()
    for chave, valor in kwargs.items():
        if valor in (None, ""):
            query.pop(chave, None)
        else:
            query[chave] = valor
    return query.urlencode()


@register.inclusion_tag("biblioteca/_paginacao.html", takes_context=True)
def paginacao(context):
    """Barra de paginação (com reticências) compatível com filtros."""
    page_obj = context.get("page_obj")
    paginas = []
    ellipsis = "…"
    if page_obj is not None:
        ellipsis = page_obj.paginator.ELLIPSIS
        paginas = list(
            page_obj.paginator.get_elided_page_range(
                page_obj.number, on_each_side=2, on_ends=1
            )
        )
    return {
        "request": context["request"],
        "page_obj": page_obj,
        "paginas": paginas,
        "ellipsis": ellipsis,
    }
