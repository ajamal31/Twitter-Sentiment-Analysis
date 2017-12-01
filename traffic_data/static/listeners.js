$(document).ready(function () {

    function ajax_post(click_elem, change_elem, elem_id) {
        $(click_elem).click(function (e) {
            e.preventDefault();
            var clicked_text = $(this).text();
            document.getElementById(elem_id).innerHTML = clicked_text + "<i class=\"caret\"></i>";

            var cur_tweet_count = $("#tweet_btn").text();
            var cur_hashtag = $("#hashtag-btn").text();

            console.log(cur_tweet_count);
            console.log(cur_hashtag);

            $.ajax({
                url: "/",
                type: "POST",
                data: {
                    num_tweets: cur_tweet_count,
                    hashtag: cur_hashtag
                },
                success: function (data) {
                    $(change_elem).html(data);
                },
                error: function (xhr, errmsg, err) {
                    alert(errmsg)
                }
            });
        });
    }

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

    ajax_post('#num_tweets a', '.bar-graphs', 'tweet_btn');
    ajax_post('#hashtag-text a', '.bar-graphs', 'hashtag-btn');

    // $('#num_tweets a').click(function (e) {
    //     e.preventDefault();
    //     var tweet_count = $(this).text();
    //     var hashtag = $('#hashtag-btn');
    //     console.log(hashtag);
    //     document.getElementById("tweet_btn").innerHTML = tweet_count + "<i class=\"caret\"></i>";
    //
    //     $.ajax({
    //         url: "/",
    //         type: "POST",
    //         data: {
    //             num_tweets: tweet_count,
    //         },
    //         success: function (data) {
    //             $('.bar-graphs').html(data);
    //         },
    //         error: function (xhr, errmsg, err) {
    //             alert(errmsg)
    //         }
    //     });
    // });
});