$(document).ready(function () {
    $('#num_tweets a').click(function (e) {
        e.preventDefault();
        var tweet_count = $(this).text();
        document.getElementById("tweet_btn").innerHTML = tweet_count + "<i class=\"caret\"></i>";
    });
});

function bind_tweets(graph_container, type, tweets, max_tweets) {
    $(graph_container).click(function () {
        var tweets_title = make_tweets_title(type, max_tweets);
        var tweets_container = $("#tweets");
        tweets_container.html("<b>" + tweets_title + "</b>");
        tweets_container.append(tweets);
        tweets_container.attr('tweets-type', type);
    });
}

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

    $('#from').on("change", function (e) {
        $.ajax({
            url: "/",
            type: "POST",
            data: {
                min_date: $("#from").datepicker("getDate"),
                max_date: $("#to").datepicker("getDate")
            },
            success: function (data) {
                data = JSON.parse(data);
                $('.bar-graphs').html(data.bar);
                $('.sent_line').html(data.line);
                $('.top_tweets').html(data.tweets);
            },
            error: function (xhr, errmsg, err) {
                alert(errmsg)
            }
        });
    });
    $('#to').on("change", function (e) {
        $.ajax({
            url: "/",
            type: "POST",
            data: {
                min_date: $("#from").datepicker("getDate"),
                max_date: $("#to").datepicker("getDate")
            },
            success: function (data) {
                data = JSON.parse(data);
                $('.bar-graphs').html(data.bar);
                $('.sent_line').html(data.line);
                $('.top_tweets').html(data.tweets);
            },
            error: function (xhr, errmsg, err) {
                alert(errmsg)
            }
        });
    });
});