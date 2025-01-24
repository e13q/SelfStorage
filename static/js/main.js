$(document).ready(function () {
    // Registration
    $("#registerForm").submit(function (e) {
        e.preventDefault();
        var form_data = $(this).serialize();
        var pass = $("input[name=PASSWORD_CREATE]").val();
        var repass = $("input[name=PASSWORD_CONFIRM]").val();
        if ( pass != repass) {
            $(".alert.alert-danger").show().text("Пароли не совпадают");
            return false;
        }

        $.post("/register/", form_data, function (response) {
            if (response.success) { window.location.reload(); }
            else {
                $(".alert.alert-danger").show().text(response.error_message);
            }
        })
        .fail(function (xhr, status, error) { console.log(error); });
    });

    // Login
    $("#loginForm").submit(function (e) {
        e.preventDefault();
        var form_data = $(this).serialize();

        $.post("/login/", form_data, function (response) {
            if (response.success) { window.location.reload(); }
            else {
                $(".alert.alert-danger").show().text(response.error_message);
            }
        })
        .fail(function (xhr, status, error) { console.log(error); });
    });

    // Dinamic year in footer copyrights
    $('#curr_year').text((new Date).getFullYear());
});