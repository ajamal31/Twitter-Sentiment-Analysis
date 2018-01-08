function process_tweet(body, date, screen_name, name, url, rating, t_id) {

    var output_rating = complete_rating(rating);
    var rating_text_id = rating_id(output_rating);

    var block = document.createElement("blockquote");
    block.className = "twitter-tweet " + t_id;
    block.innerHTML = '<data-lang=\"en\">' +
        "<p lang='en'>" + body + "</p>" +
        "<p id=" + rating_text_id + " lang='en'>Tweet Rating: " + output_rating + "</p>" +
        "&mdash; " + name + " (@" + screen_name + ") " + '<a style="text-decoration:none">' +
        date + "</a>";
    

    return block;
}

function complete_rating(rating) {
    if (rating === "pos") {
        return "Positive";
    } else if (rating === "neg") {
        return "Negative";
    } else {
        return "Neutral";
    }
}

function rating_id(rating) {
    if (rating === "Positive") {
        return "positive-rating";
    } else if (rating == "Negative") {
        return "negative-rating";
    } else {
        return "neutral-rating";
    }
}

function update_tweets(type, data) {
    var tweets_type = $('#tweets').attr('tweets-type');
    var count = data.length;

    if (tweets_type === type) {
        var tweets_title = make_tweets_title(tweets_type, count);
        $('#tweets').html("<b>" + tweets_title + "</b>");
        $('#tweets').append(data);
    }

    return;
}

function make_tweets_title(type, count) {
    if (type === 'reply') {
        return 'Most Replied Tweets: ' + count;
    } else if (type === 'favourite') {
        return ' Most Favourited Tweets: ' + count;
    } else if (type === 'retweet') {
        return ' Most Retweeted Tweets: ' + count;
    } else if (type === 'recent') {
        return ' Most Recent Tweets: ' + count;
    }
}
