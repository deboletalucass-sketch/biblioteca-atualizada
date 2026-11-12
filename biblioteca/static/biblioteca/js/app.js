/*
 * Plugins jQuery usados no projeto:
 *   1. jQuery Mask Plugin  -> máscaras nos campos ISBN e ano
 *   2. DataTables          -> ordenação das colunas nas tabelas
 *   3. Bootbox             -> confirmação de exclusão em janela modal
 *   4. Select2             -> select pesquisável para escolher o livro
 */
$(function () {
    // 1) Máscaras (jQuery Mask Plugin)
    $("#id_ano_publicacao").mask("0000");
    $("#id_isbn").mask("ZZZZZZZZZZZZZZZZZ", {
        translation: { Z: { pattern: /[0-9Xx\-]/, optional: true } },
    });

    // 2) DataTables: só ordenação no cliente; a paginação e a busca ficam
    //    por conta do Django (ListView + django-filter).
    $("table.js-datatable").DataTable({
        paging: false,
        searching: false,
        info: false,
        order: [],
        columnDefs: [{ orderable: false, targets: "no-sort" }],
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.8/i18n/pt-BR.json",
        },
    });

    // 3) Bootbox: confirma e então envia um POST para a URL de exclusão.
    //    Sem JavaScript, o link continua levando à página de confirmação.
    $(document).on("click", "a.js-excluir", function (e) {
        e.preventDefault();
        var url = $(this).attr("href");
        var nome = $(this).data("nome") || "este registro";
        bootbox.confirm({
            title: "Confirmar exclusão",
            message: "Deseja realmente excluir <strong>" + $("<div>").text(nome).html() + "</strong>?",
            buttons: {
                cancel: { label: "Cancelar", className: "btn-secondary" },
                confirm: { label: "Excluir", className: "btn-danger" },
            },
            callback: function (confirmado) {
                if (confirmado) {
                    var form = document.getElementById("form-excluir");
                    form.setAttribute("action", url);
                    form.submit();
                }
            },
        });
    });

    // 4) Select2
    $("select.js-select2").select2({ language: "pt-BR", width: "100%" });
});
