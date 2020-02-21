$(document).ready(function() {
    $("a.set_favorite").on('click', function(event){
        event.preventDefault();
        var link = $(this);
        var url = link.attr('href');

        var html = { "save": "<i class=\"fas fa-save\"></i> Sauvegarder", "remove": "<i class=\"fas fa-trash-alt\"></i> Retirer des favoris"};

        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
                if(data.status == 200){
                    link.html(html[data.action]);
                    link.attr('href', data.replace_url);
                } else {
                    console.log(data);
                }
            }
        });
    });
});

$(document).ready(function() {
    $("a.remove_favorite").on('click', function(event){
        event.preventDefault();
        var link = $(this);
        var url = link.attr('href');

        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
                if(data.status == 200){
                    link.closest('div').remove();
                    if($("a.remove_favorite").length === 0){
                        $('div.fav-content').html('<div class="col-lg-12">Aucun produit(s) sauvegardé(s).</div>');
                    }
                } else {
                    console.log(data);
                }
            }
        });
    });
});