function makeLineGraph(data, divName, title) {

    var svg = dimple.newSvg(divName, "100%", "100%");
    var myChart = new dimple.chart(svg, data);
    var x = myChart.addTimeAxis("x", "Created", "%a %b %d %Y %H:%M:%S","%Y/%m/%d");
    myChart.addMeasureAxis("y", "Sentiment");
    myChart.addColorAxis("Sentiment", ["red", "yellow", "green"]);
    var s = myChart.addSeries(null, dimple.plot.bubble);

    s.getTooltipText = function (e) {
        var i,
        tooltip = [];
        var format = d3.timeFormat("%a %b %d %Y %H:%M:%S");
        for (i = 0;  i < data.length; i++) {
            if (format(e.x) === data[i].Created ) {
                tooltip.push("User: " + data[i].User);
                tooltip.push("Tweet: " + data[i].Tweet);
                tooltip.push("Date: " + data[i].Created);
                tooltip.push("Sentiment: " + data[i].Sentiment);
            }
        }
        return tooltip
        };

    myChart.setMargins("15%", "20%", "5%", "25%");

    svg.append("text")
    .attr("x", myChart._xPixels() + myChart._widthPixels()/2)
    .attr("y", myChart._yPixels() - 40)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .style("text-decoration", "underline")
    .text(title);

    myChart.axes[0].showGridlines = true;
    myChart.axes[1].showGridlines = false;
    myChart.axes[1].fontSize = "12px";
    myChart.draw();
    myChart.axes[0].titleShape.style("font-size", "12px");

    rotate_labels(myChart);

    window.onresize = function () {
        // As of 1.1.0 the second parameter here allows you to draw
        // without reprocessing data.  This saves a lot on performance
        // when you know the data won't have changed.
        myChart.draw(0, true);
        rotate_labels(myChart);
        

    };
}

function rotate_labels(chart) {
    chart.axes[0].shapes.selectAll('text').attr('transform',
    function () {
        var transformAttributeValue = d3.select(this).attr('transform');

        if (transformAttributeValue) {
            transformAttributeValue = transformAttributeValue.replace('rotate(90,', 'rotate(45,');
        }
        return transformAttributeValue;
    });
}