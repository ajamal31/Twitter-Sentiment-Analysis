function makeLineGraph(data, divName, title) {

    var svg = dimple.newSvg(divName, "100%", "100%");
    var myChart = new dimple.chart(svg, data);
    var x = myChart.addTimeAxis("x", "Created", "%Y-%m-%d %H:%M:%S","%Y/%m/%d");
    myChart.addMeasureAxis("y", "Sentiment");
    var s = myChart.addSeries(null, dimple.plot.line);

    s.getTooltipText = function (e) {
        var i, 
        tooltip = [];
        var format = d3.timeFormat("%Y-%m-%d %H:%M:%S");
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
    
    myChart.setMargins("10%", "20%", "10%", "15%");

    svg.append("text")
    .attr("x", myChart._xPixels() + myChart._widthPixels()/2)
    .attr("y", myChart._yPixels() - 40)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .style("text-decoration", "underline")
    .text(title);

    myChart.draw();
}
