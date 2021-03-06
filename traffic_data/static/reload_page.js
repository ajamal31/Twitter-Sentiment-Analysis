$(document).ready(function () {

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //update database and reloading view
    $(document).on('click', "#bind", function (event) {
        event.preventDefault();
        $("#updated").html("<br><a style='color: white !important;'>Updating...</a>");
        $.ajax({
            url: "database",
            dataType: 'text',
            type: "GET",
            success: function (data) {
                location.reload(true);
            },
            error: function (xhr, errmsg, err) {
                alert(errmsg);
            }
        });
    });
});
