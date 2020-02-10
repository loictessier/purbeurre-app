$(document).ready(function() {
    $("a.add_favorite").on('click', function(event){
        event.preventDefault();
        var link = $(this);
        var url = link.attr('href');

        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
                if(data.status == 200){
                    link.replaceWith('<span>Sauvegardé</span>');
                } else {
                    console.log(data);
                }
            }
        });
    });
});