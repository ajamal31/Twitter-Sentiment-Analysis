var draw_time = 800;

function makeGraph(data, title, divName, xTitle, yTitle) {

    var svg = dimple.newSvg(divName, "100%", "100%");
    if (data.length > 0) {
        var chart = new dimple.chart(svg, data);
        chart.addCategoryAxis("y", yTitle);
        chart.addMeasureAxis("x", xTitle);
        var s = chart.addSeries(null, dimple.plot.bar);
        chart.setMargins("15%", "20%", "5%", "15%");

        s.tooltipFontSize = "14px";

        s.getTooltipText = function (e) {
            tooltip = [];
            tooltip.push(yTitle + ": " + e.cy);
            tooltip.push(xTitle + ": " + e.cx);
            return tooltip;
        }

        svg.append("text")
            .attr("x", chart._xPixels() + chart._widthPixels() / 2)
            .attr("y", chart._yPixels() - 40)
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .style("text-decoration", "underline")
            .text(title);

        if (yTitle === "Sentiment") {
            chart.axes[0].addOrderRule(["Negative", "Neutral","Positive"]);
        }
        else {
            chart.axes[0].addOrderRule(xTitle, false);
        }
        
        chart.axes[1].fontSize = "12px";
        chart.draw(draw_time);
        chart.axes[0].titleShape.style("font-size", "12px");
        
        s.shapes.on("mouseover", function (e) {
            d3.select(divName).selectAll("rect").style("opacity", .3);
            d3.select(this).style("opacity", 0.8);
            dimple._showBarTooltip(e, this, chart, s);
            var tid = data.find(function(d){ return d[xTitle] == e.cx && d[yTitle] == e.cy});
            console.log($("." + tid.ID));
            $("." + tid.ID).addClass("tweet-highlight");
        });

        // s.shapes.on("mouseleave", function (e) {
        //     d3.selectAll("rect").style("opacity", 0.8);
        //     dimple._removeTooltip(e, this, chart, s);
        //     $(".twitter-tweet").removeClass("tweet-highlight");
        // });

        window.onresize = function () {
            // As of 1.1.0 the second parameter here allows you to draw
            // without reprocessing data.  This saves a lot on performance
            // when you know the data won't have changed.
            chart.draw(0, true);
        };
    s.tooltipFontSize = "14px";

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
    makeGraph(data, title, divName, xTitle, "User");
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
