function process_tweet(body, date, user, url, rating) {
    var block = document.createElement("blockquote");
    block.className = "twitter-tweet";
    block.innerHTML = '<data-lang=\"en\">' +
                "<p lang='en'>" + body + "</p>" +
                "<p lang='en'>Tweet Rating: " + rating + "</p>" +
                "&mdash; " + user + " (@" + user + ") "+ '<a href="">' +
                date + "</a>";
    block.onclick = function(tweet) {
            window.open(url);
    } 
    $( "#tweets" ).append(block);
}