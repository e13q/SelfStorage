$(document).ready(function() {
    $("#registerForm").submit(function (e) {
        e.preventDefault();
        var form_data = $(this).serialize();
        $.ajax({
            type: "POST",
            url: "/register/",
            data: form_data,
            success: function () {
                alert("Ваше сообщение отправлено!");
            }
        });
    });

    $('#curr_year').text( (new Date).getFullYear() );
});