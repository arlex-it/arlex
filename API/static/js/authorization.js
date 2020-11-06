$(document).ready(function() {
    $('.register-link').click(function () {
        $('.form-login')[0].submit();
        // $.post($('.form-login')[0].action, $('.form-login').serialize());
    });
    let $form = $(".form-signin");
    let data = getFormData($form);
    const state = data['state'];
    const response_type = data['response_type'];
    const client_id = data['client_id'];
    const redirect_uri = data['redirect_uri'];

    console.log(`/api/auth/authorize?state=${state}&client_id=${client_id}&response_type=${response_type}&redirect_uri=${redirect_uri}`);
    function getFormData($form){
        var unindexed_array = $form.serializeArray();
        var indexed_array = {};

        $.map(unindexed_array, function(n, i){
            if (n['name'] === "gender")
                indexed_array[n['name']] = parseInt(n['value']);
            else
                indexed_array[n['name']] = n['value'];
        });

        return indexed_array;
    }

    $('.form-signin').submit(function (event) {
        event.preventDefault();


        let $form = $(".form-signin");
        let data = getFormData($form);
        let address = data['street'].trim();
        let matches = address.match('[0-9/-/ ]+');
        if (matches[0].trim() !== "") {
            data['street_number'] = matches[0].trim();
            data['street'] = data['street'].replace(matches[0], "");
        }
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: JSON.stringify(data),
            success: function(res){
                const state = data['state'];
                const response_type = data['response_type'];
                const client_id = data['client_id'];
                const redirect_uri = data['redirect_uri'];
                window.location.replace(`/api/auth/authorize?state=${state}&client_id=${client_id}&response_type=${response_type}&redirect_uri=${redirect_uri}`);
                alert(JSON.stringify(res));
            },
            error: function(data){
                alert(JSON.stringify(data['responseJSON']));
            },
            dataType: "json",
            contentType : "application/json"
        });
    });
    return false;
});