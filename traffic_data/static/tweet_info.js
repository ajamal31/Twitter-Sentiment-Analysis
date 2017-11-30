function process_tweet(body, date, screen_name, name, url, rating) {
    var block = document.createElement("blockquote");
    block.className = "twitter-tweet";
    block.innerHTML = '<data-lang=\"en\">' +
                "<p lang='en'>" + body + "</p>" +
                "<p lang='en'>Tweet Rating: " + rating + "</p>" +
                "&mdash; " + name + " (@" + screen_name + ") "+ '<a href="">' +
                date + "</a>";
    block.onclick = function(tweet) {
            window.open(url);
    } 
    $( "#tweets" ).append(block);
}