$(document).ready(function () {
    // Dynamic year in footer copyrights
    $('#curr_year').text((new Date).getFullYear());

    // Common ajax success handler
    function request_response(response) {
        if (response.success) { window.location.reload(); }
        else {
            $(".alert.alert-danger").show().text(response.error_message);
        }
    }

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

        $.post("/register/", form_data, request_response)
        .fail(function (xhr, status, error) { console.log(error); });
    });

    // Login
    $("#loginForm").submit(function (e) {
        e.preventDefault();
        var form_data = $(this).serialize();

        $.post("/login/", form_data, request_response)
        .fail(function (xhr, status, error) { console.log(error); });
    });

    // Edit profile info
    $("#acc_page_edit").click(function(e) {
        e.preventDefault();
        $("#EMAIL").prop("disabled", false);
        $("#PHONE").prop("disabled", false);
        $("#PASSWORD").prop("disabled", false);
        $("#PASSWORD").prop("type", "text");
        $("#acc_page_edit").hide();
        $("#acc_page_save").show();
    });
    $("#acc_page_save").click(function(e) {
        $("#EMAIL").prop("disabled", true);
        $("#PHONE").prop("disabled", true);
        $("#PASSWORD").prop("disabled", true);
        $("#PASSWORD").prop("type", "password");
        $("#acc_page_edit").show();
        $("#acc_page_save").hide();
    });
    
});