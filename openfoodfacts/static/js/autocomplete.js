$(function () {
    $("#search_input").autocomplete({
        source: "/api/get_products/",
        minLength: 2,
    });
});