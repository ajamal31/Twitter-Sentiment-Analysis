function process_tweet(body, date, screen_name, name, url, rating) {

    var output_rating = complete_rating(rating);
    var rating_text_id = rating_id(output_rating);

    var block = document.createElement("blockquote");
    block.className = "twitter-tweet";
    block.innerHTML = '<data-lang=\"en\">' +
                "<p lang='en'>" + body + "</p>" +
                "<p id=" + rating_text_id + " lang='en'>Tweet Rating: " + output_rating + "</p>" +
                "&mdash; " + name + " (@" + screen_name + ") "+ '<a href="">' +
                date + "</a>";
    block.onclick = function(tweet) {
            window.open(url);
    } 
    $( "#tweets" ).append(block);
}

function complete_rating(rating) {
    if (rating === "pos") {
        return "Positive"
    } else if (rating === "neg") {
        return "Negative"
    } else {
        return "Neutral"
    }
}

function rating_id (rating) {
    if (rating === "Positive") {
        return "positive-rating"
    } else if (rating == "Negative") {
        return "negative-rating"
    } else {
        return "neutral-rating"
    }
}