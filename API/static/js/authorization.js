$(document).ready(function() {

        $('.form-signin').submit(function (event) {
        event.preventDefault();

        $.post($(this).attr('action'), $(this).serialize())
        .done(function(data) {
            if (data['redirect'].startsWith('http')) {
                window.location.href = data['redirect'];
            } else {
                $("#submit_button").html('Se connecter');
            }
        }, 'json');
    });
});