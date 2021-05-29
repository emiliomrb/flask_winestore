$(document).ready(function() {
    $('#client_id').on('blur', function(){
        $.getJSON('/autocomplete', {
            client: $('#client_id').val()
        }, function(data) {
            $('#client_name').text('chaja')
        });
    })
});
hfjhgfghj;