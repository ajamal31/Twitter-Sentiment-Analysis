var draw_time = 800;

function makeGraph(data, title, divName, xTitle, yTitle) {

    var svg = dimple.newSvg(divName, "100%", "100%");
    var chart = new dimple.chart(svg, data);
    chart.addCategoryAxis("y", yTitle);
    chart.addMeasureAxis("x", xTitle);
    var s = chart.addSeries(null, dimple.plot.bar);
    chart.setMargins("20%", "20%", "10%", "15%");

    s.tooltipFontSize = "14px";
    s.getTooltipText = function (e) {
        tooltip = [];
        tooltip.push(yTitle + ": " + e.cy);
        tooltip.push("Tweets" + ": " + e.cx);
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

    chart.draw(draw_time);

    s.shapes.on("mouseover", function (e) {
        d3.select(divName).selectAll("rect").style("opacity", .3);
        d3.select(this).style("opacity", 0.8);
        dimple._showBarTooltip(e, this, chart, s);
    });

    s.shapes.on("mouseleave", function (e) {
        d3.selectAll("rect").style("opacity", 0.8);
        dimple._removeTooltip(e, this, chart, s);
    })
}

function makeSocialGraph(data, divName, title, xTitle) {
    makeGraph(data, title, divName, xTitle, "User");
}

function makeSentimentGraph(data, divName, title, xTitle) {
    makeGraph(data, title, divName, xTitle, "Sentiment");
}
   
function makeSentimentGraph(data, divName, title, xTitle) {
    chart = makeGraph(data, title, divName, xTitle, "Sentiment");
}

function redraw_socialgraph(data, object_name, title, x_title) {
    $(object_name).remove();
    var class_name = object_name.slice(1);
    $(".bar-graphs").append("<div class=" + class_name + "></div>");
    makeSocialGraph(data, object_name, title, x_title);
    return;
}
