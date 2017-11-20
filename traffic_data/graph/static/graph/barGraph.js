function makeGraph(data, title, divName, xTitle, yTitle){

    var svg = dimple.newSvg(divName, "100%", "100%");
    var chart = new dimple.chart(svg, data);
    chart.addCategoryAxis("y", yTitle);
    chart.addMeasureAxis("x", xTitle);
    chart.addSeries(null, dimple.plot.bar);
    chart.setMargins("20%", "20%", "10%", "15%");

    svg.append("text")
    .attr("x", chart._xPixels() + chart._widthPixels() / 2)
    .attr("y", chart._yPixels() - 40)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .style("text-decoration", "underline")
    .text(title);
    
    return chart;
}

function makeSocialGraph(data, divName, title, xTitle){
   chart = makeGraph(data, title, divName, xTitle, "User");
   chart.axes[0].addOrderRule(xTitle, false);
   chart.draw();
}

function makeSentimentGraph(data, divName, title, xTitle){
    chart = makeGraph(data, title, divName, xTitle, "Sentiment");
    chart.axes[0].addOrderRule(["Positive", "Neutral", "Negative"]);
    chart.draw();   
}