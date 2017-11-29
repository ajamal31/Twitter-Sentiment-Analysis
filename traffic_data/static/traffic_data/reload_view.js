$(document).ready(function(){
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $("p1").click(function(){
        $.ajax({url:'database/',
            success: function(){
                $.ajax({url:'reload/',
                    type: 'POST',
                    success: function(data){
                        $("#update-view").html(data);
                        alert("test success" + data);
                    }
                });
            },
            failure: function(result){
                alert("test failed");
            }
        });

    });
});
