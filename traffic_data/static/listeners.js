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