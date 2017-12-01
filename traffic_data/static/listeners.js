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

    $('#num_tweets a').click(function (e) {
        e.preventDefault();
        var tweet_count = $(this).text();
        document.getElementById("tweet_btn").innerHTML = tweet_count + "<i class=\"caret\"></i>";

        $.ajax({
            url: "/",
            type: "POST",
            data: {
                num_tweets: tweet_count,
            },
            success: function (data) {
                $('.bar-graphs').html(data);
            },
            error: function (xhr, errmsg, err) {
                alert(errmsg)
            }
        });
    });

    //update database and reloading view
    $("#updated").on('click', function(){
        $("#updated").unbind();
        $("#updated").html("<p style='color:red;'>loading...</p>");
        $.ajax({url:'database/',
            success: function(){
                location.reload(true);
            }
        });
    });
});
