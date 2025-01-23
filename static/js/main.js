$(document).ready(function () {
    $("#registerForm").submit(function (e) {
        e.preventDefault();
        var form_data = $(this).serialize();
        var pass = $("input[name=PASSWORD_CREATE]").val();
        var repass = $("input[name=PASSWORD_CONFIRM]").val();
        if ( pass != repass) {
            $(".alert.alert-danger").show().text("Пароли не совпадают");
            $(this).stop();
        }
        $.ajax({
            type: "POST",
            url: "/register/",
            data: form_data,
            success: function (response) {
                if (!response.status) {
                    $(".alert.alert-danger").show().text(response.error_message);
                }
            },
            error: function (xhr, status, error) { console.log(error); }
        });
    });

    $('#curr_year').text((new Date).getFullYear());
});