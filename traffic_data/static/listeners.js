$(document).ready(function () {
    $('#num_tweets a').click(function (e) {
        e.preventDefault();
        var tweet_count = $(this).text();
        document.getElementById("tweet_btn").innerHTML = tweet_count + " <i class=\"caret\"></i>";
    });
});

function bind_tweets(graph_container, type, tweets, max_tweets) {
    $(graph_container).click(function () {
        var tweets_title = make_tweets_title(type, max_tweets);
        var tweets_container = $("#tweets");
        tweets_container.html("<b>" + tweets_title + "</b>");
        tweets_container.append(tweets);
        tweets_container.attr('tweets-type', type);
        tweets_container.scrollTop(0);
    });
}

function make_ajax(start_date, end_date, hashtag) {
    
    var loader = document.getElementById("loader");
    loader.style.display = "inline-block";
    $.ajax({
        url: "/",
        type: "POST",
        data: {
            min_date: start_date,
            max_date: end_date,
            hashtag: hashtag
        },
        success: function (data) {
            data = JSON.parse(data);
            $('#top_tweets').html(data.tweets);
            $('#sent_line').html(data.line);
            $('#bar_graphs').html(data.bar);
            loader.style.display = "none";
        },
        error: function (xhr, errmsg, err) {
            alert(errmsg)
        }
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
            var loader = document.getElementById("loader");
            loader.style.display = "block";
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#from').on("change", function (e) {
        var start_date = $("#from").datepicker("getDate");
        var end_date = $("#to").datepicker("getDate");
        var hash_tag = $('#hashtag-dropdown').text();
        make_ajax(start_date, end_date, hash_tag);
    });

    $('#to').on("change", function (e) {
        var start_date = $("#from").datepicker("getDate");
        var end_date = $("#to").datepicker("getDate");
        var hash_tag = $('#hashtag-dropdown').text();
        make_ajax(start_date, end_date, hash_tag);
    });

    $('#hashtag-list li a').on("click", function () {

        // slice is used to strip off the '#' from the text
        var hashtag = $(this).text();

        if (hashtag !== 'All') {
            hashtag = ($(this).text()).slice(1);
        }

        $('#hashtag-dropdown').html(hashtag + " <i class=\"caret\"></i>");

        var start_date = $("#from").datepicker("getDate");
        var end_date = $("#to").datepicker("getDate");
        var hash_tag = $('#hashtag-dropdown').text();

        make_ajax(start_date, end_date, hash_tag);

    });
});