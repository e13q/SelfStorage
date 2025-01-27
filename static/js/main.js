$(document).ready(function () {
    // Dynamic year in footer copyrights
    $('#curr_year').text(new Date().getFullYear());

    // Common ajax success handler
    function request_response(response) {
        if (response.success) { window.location.reload(); }
        else {
            $(".alert.alert-danger").show().text(response.error_message);
        }
    }

    const selectedBoxField = document.querySelector('select[name="selected_box"]');
    document.querySelectorAll('.select-box-btn').forEach(button => {
        button.addEventListener('click', function () {
            const boxId = this.dataset.id;
            if (selectedBoxField) {
                selectedBoxField.value = boxId;
            }
            document.getElementById('orderForm').scrollIntoView({ behavior: 'smooth' });
        });
    });
    // Boxes     
    document.querySelectorAll('.SelfStorage__warehouselink').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const warehouseId = this.getAttribute('data-bs-target').split('-')[1];
            fetch(`/filter-boxes/${warehouseId}/`)
                .then(response => response.json())
                .then(data => {
                    document.querySelector('#pills-all').innerHTML = data.boxes_html;
                    document.querySelector('#pills-to3').innerHTML = data.boxes_to3_html;
                    document.querySelector('#pills-to10').innerHTML = data.boxes_to10_html;
                    document.querySelector('#pills-from10').innerHTML = data.boxes_from10_html;
                    document.querySelectorAll('.select-box-btn').forEach(button => {
                        button.addEventListener('click', function () {
                            const boxId = this.dataset.id;
                            if (selectedBoxField) {
                                selectedBoxField.value = boxId;
                            }
                            document.getElementById('orderForm').scrollIntoView({ behavior: 'smooth' });
                        });
                    });
                });
            
        });
    });
    
    

    // Order making
    $("#orderForm").on("submit", function (e) {
        e.preventDefault();        
        $("#loadingOverlay").show();
        let form = $(this);
        let url = form.attr("action");
        let formData = form.serialize();
        form.find(".errorlist").remove();
        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            success: function (response) {                
                $("#loadingOverlay").hide();
                if (response.success) {
                    alert(response.message);
                    form[0].reset();
                } else {
                    for (let field in response.errors) {
                        let input = $("[name=" + field + "]", form);
                        let errors = response.errors[field];
                        let errorList = $("<ul>").addClass("errorlist");
                        errors.forEach(error => errorList.append($("<li>").text(error)));
                        input.after(errorList);
                    }
                }
            },
            error: function (xhr, status, error) {                
                $("#loadingOverlay").hide();
                alert("Произошла ошибка: " + error);
            }
        });
    });

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
        $("#PASSWORD").prop("value", "");
        $("#acc_page_edit").hide();
        $("#acc_page_save").show();
    });
    $("#profileInfoForm").submit(function (e) {
        e.preventDefault();
        var form_data = $(this).serialize();

        $.post("/profile/", form_data, request_response)
        .fail(function (xhr, status, error) { console.log(error); });
    });

    // Extend order time
    var order_id, boxDateEnd;

    $(".rentExtButton").click(function(e) {
        order_id = $(this).attr("data-order-id");
        boxDateEnd = $(this).attr("data-box-date-end");
        var date = new Date(boxDateEnd);
        date.setTime(date.getTime() + 86400000);
        var newBoxDateEnd = date.toISOString().split('T')[0];
        $("#RentExtModalTitle").text("Продлить аренду бокса " + $(this).attr("data-box-number") + " до");
        $("#rentExtForm").find('[name="NEW_RENT_END_DATE"]').attr("min", newBoxDateEnd);
        $("#RentExtModal").fadeIn();
    });

    $("#RentExtModalClose").click(function(e) {
        $("#RentExtModal").fadeOut();
    });

    $("#rentExtForm").submit(function (e) {
        e.preventDefault();
        var new_date = $(this).find('[name="NEW_RENT_END_DATE"]').val();
        if (new Date(new_date).getTime() <= new Date(boxDateEnd).getTime() + 86400000) {
            $(".alert.alert-danger").show().text("Новая дата должна быть после текущей даты окончания аренды");
            return false;
        }
        var form_data = {
            csrfmiddlewaretoken: $(this).find('[name=csrfmiddlewaretoken]').val(),
            extend_rent_time: true,
            order_id: order_id,
            new_rent_end_date: new_date
        };

        $.post("/profile/", form_data, request_response)
        .fail(function (xhr, status, error) { console.log(error); });
    });

    $(".openBoxButton").click(function(e) {
        order_id = $(this).attr("data-order-id");

        $.ajax({
            url: '/profile/',
            method: 'POST',
            data: {
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
                open_box: true,
                order_id: order_id,
            },
            beforeSend: function() {
                if (confirm("Вам на почту будет отправлен QR-код для открытия бокса.\nОткрытие бокса завершит аренду.\nСогласны продолжить?")) {
                    $("#loadingOverlay").show();
                    return true;
                } else {
                    return false;
                }
            },
            success: function(response) {
                request_response(response);
                $("#loadingOverlay").hide();
            },
            error: function (xhr, status, error) {
                console.log(error);
                $("#loadingOverlay").hide();
            }
          });
    });

});