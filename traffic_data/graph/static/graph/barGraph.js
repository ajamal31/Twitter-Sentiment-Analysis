function makeGraph(data, title) {
    var margin = { top: 40, right: 20, bottom: 30, left: 100 },
        width = 500 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .range([0, width])
        .domain([0, d3.max(data, function (d) {
            return d.count;
        })]);

    var y = d3.scale.ordinal()
        .rangeRoundBands([height, 0], .1)
        .domain(data.map(function (d) {
            return d.tag;
        }));

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");


    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            return "<strong>Frequency:</strong> <span style='color:red'>" + d.count + "</span>";
        })

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.call(tip);

    // The following code was contained in the callback function.
    y.domain(data.map(function (d) { return d.tag; }));
    x.domain([0, d3.max(data, function (d) { return d.count; })]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)

    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text(title);

    svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("y", function (d) { return y(d.tag); })
        .attr("height", y.rangeBand())
        .attr("x", 0)
        .attr("width", function (d) { return x(d.count); })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)

    function type(d) {
        d.count = +d.count;
        return d;
    }
}