$(function () {
    $("#search_input").autocomplete({
        source: "/api/get_products/",
        select: function (event, ui) { //item selected
            AutoCompleteSelectHandler(event, ui)
        },
        minLength: 2,
    });
});

function AutoCompleteSelectHandler(event, ui) {
    var selectedObj = ui.item;
}