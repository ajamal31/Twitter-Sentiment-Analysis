$(document).ready(function () {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
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
    $(document).on('click',"#bind", function(){
        $("#updated").html("<br><p style='color: white;'>Updating...</p>");
        $.ajax({url:'database/',
            success: function(){
                location.reload(true);
            },
            error: function(){
                $("#updated").html("<a id='bind'><b>Update Tweets</b></a>");
                alert("Failed to update");
            }
        });
    });
});
