var draw_time = 800;

function makeGraph(data, title, divName, xTitle, yTitle) {

    var svg = dimple.newSvg(divName, "100%", "100%");
    if (data.length > 0) {
        var chart = new dimple.chart(svg, data);
        chart.addCategoryAxis("y", yTitle);
        chart.addMeasureAxis("x", xTitle, "Full Tweet");
        var s = chart.addSeries(null, dimple.plot.bar);

        if (yTitle === "Sentiment") {
            chart.setMargins("15%", "20%", "5%", "15%");
            svg.append("text")
                .attr("x", chart._xPixels() + chart._widthPixels() / 2 - 30)
                .attr("y", chart._yPixels() - 40)
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("text-decoration", "underline")
                .text(title);
        }
        else {
            chart.setMargins("38%", "20%", "5%", "15%");
            svg.append("text")
                .attr("x", chart._xPixels() + chart._widthPixels() / 2 - 150)
                .attr("y", chart._yPixels() - 40)
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .style("text-decoration", "underline")
                .text(title);
        }

        s.tooltipFontSize = "14px";

        s.getTooltipText = function (e) {
            tooltip = [];
            tooltip.push(xTitle + ": " + e.cx);
            return tooltip;
        };


        if (yTitle === "Sentiment") {
            chart.axes[0].addOrderRule(["Negative", "Neutral", "Positive"]);
        }
        else {
            chart.axes[0].addOrderRule(xTitle, false);
        }

        chart.axes[1].fontSize = "14px";
        chart.draw(draw_time);
        chart.axes[0].titleShape.style("font-size", "14px");

        s.shapes.on("mouseover", function (e) {
            d3.select(divName).selectAll("rect").style("opacity", .3);
            d3.select(this).style("opacity", 0.8);
            dimple._showBarTooltip(e, this, chart, s);

            var max_tweets = $("#tweet_btn").text();
            max_tweets = max_tweets.replace(/\s+/g, "");

            if (title === 'Most Retweeted') {
                var type = 'retweet';
                var tweets = get_rt_tweets();
            } else if (title === 'Most Favourited') {
                var type = 'favourite';
                var tweets = get_fav_tweets();
            }

            if (title !== 'Tweets by Sentiment') {
                var tweets_title = make_tweets_title(type, max_tweets);
                var tweets_container = $("#tweets");
                tweets_container.html("<b>" + tweets_title + "</b>");
                tweets_container.append(tweets.slice(0, max_tweets));
                tweets_container.attr('tweets-type', type);

                var tid = data.find(function (d) {
                    return d[xTitle] == e.cx && d[yTitle] == e.cy
                });

                var tweet_box = $("." + tid.ID);
                var vert_position = tweet_box.offset().top + tweets_container.scrollTop() - $('#flex').height() - tweet_box.height();

                tweet_box.addClass("tweet-highlight");
                tweets_container.animate({
                    scrollTop: vert_position
                }, 200);
            }
        });

        s.shapes.on("mouseleave", function (e) {
            $('#tweets').stop(true, true);
            d3.selectAll("rect").style("opacity", 0.8);
            dimple._removeTooltip(e, this, chart, s);
            $(".twitter-tweet").removeClass("tweet-highlight");

        });

        s.shapes.on("click", function (e) {
            var tid = data.find(function (d) {
                return d[xTitle] == e.cx && d[yTitle] == e.cy
            });

            var url = "https://www.twitter.com/" + tid.User + "/status/" + tid.ID;
            url = url.replace(/\s/g, "");
            var text = '<a href=' + url + '></a>';
            var feed = document.createElement("blockquote");
            feed.className = "twitter-tweet";
            feed.setAttribute("data-conversation", "none");
            feed.innerHTML = text;
            if (yTitle != "Sentiment") {
                $(".dial").html(feed);
                $(".dial").dialog({
                    title: "Tweet",
                    draggable: false,
                    position: {my: "center", at: "top"},
                    modal: true,
                    minHeight: 200,
                    minWidth: 500,
                    dialogClass: 'dial-head'
                });
                $.getScript("/static/twitter_widget.js");
                $(".ui-widget-overlay").on("click", function () {
                    $(".dial").dialog("close");
                });
            }
        });
        window.onresize = function () {
            // As of 1.1.0 the second parameter here allows you to draw
            // without reprocessing data.  This saves a lot on performance
            // when you know the data won't have changed.
            chart.draw(0, true);
        };

    }
    else {
        var div = document.getElementById("sentiment");
        rect = div.getBoundingClientRect();

        svg.append("text")
            .attr("x", rect.width / 2)
            .attr("y", rect.height / 2)
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .style("text-decoration", "underline")
            .text("No data avaliable");
    }

}

function makeSocialGraph(data, divName, title, xTitle) {
    makeGraph(data, title, divName, xTitle, "Tweet");
}

function makeSentimentGraph(data, divName, title, xTitle) {
    makeGraph(data, title, divName, xTitle, "Sentiment");
}

function redraw_socialgraph(data, object_name, title, x_title) {
    $(object_name).remove();
    var class_name = object_name.slice(1);
    $(".bar-graphs").append("<div class=" + class_name + "></div>");
    makeSocialGraph(data, object_name, title, x_title);
    return;
}
