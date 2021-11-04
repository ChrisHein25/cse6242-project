// margin and size
var margin = {top: 100, right: 100, bottom: 100, left: 100};
var chart_width = 600;
var chart_height = 400;
var w = chart_width + margin.left + margin.right;
var h = chart_height + margin.top + margin.bottom;

// data
var injury_data_path = ""
var boxscore_data_path = ""
var playing_style_path = ""

// append SVG
var svg = d3.select("#visualization").append("svg")
    .style("border", "solid")
    .attr("width", w)
    .attr("height", h);

console.log('finished')

// load example csv data that will eventually get replaced with real playing style data
//d3.dsv(",", pathToCsv, function (d) {
//    return {
//        // format data attributes
//        name: String(d["name"]),
//        year: parseInt(d["year"]),
//        average_rating: Math.floor(d["average_rating"]),
//        users_rated: parseInt(d["users_rated"]),
//
//    }
//}).then(function (data) {
//    console.log(data);
//
//    // create linechart-specific dataset based on data
//    year_min = 2015;
//    year_max = 2019;
//    rating_min = 0;
//    rating_max = 9;
//    data_chart = []
//
//    for (let i = year_min; i <= year_max; i++) {
//        // for each year, get number of boardgames by rating value. If no boardgames for rating assign value of 0
//        bg_in_yr = data.filter(data => data.year === i);
//        // for each rating, count boardgames
//        for (let j = rating_min; j <= rating_max; j++) {
//            data_chart.push({
//                year: i,
//                rating: j,
//                bg_count: bg_in_yr.filter(bg_in_yr => bg_in_yr.average_rating === j).length
//            })
//        }
//    }
//
//    //based on data, create Scales
//    y_min = 0;
//    y_max = d3.max(data_chart, function (d) { return d.bg_count; });
//    x_min = 0;
//    x_max = d3.max(data_chart, function (d) { return d.rating; });
//
//    xScale = d3.scaleLinear()
//        .domain([x_min, x_max])
//        .range([margin.left, w - margin.right]);
//    yScale = d3.scaleLinear()
//        .domain([y_min, y_max])
//        .range([h - margin.bottom, margin.top]);
//
//    // build required DOM structure groups
//
//    lines = svg_lines.append("g")
//        .attr("id", "lines");
//
//    circles = svg_lines.append("g")
//        .attr("id", "circles");
//
//    title = svg_lines.append("g")
//        .attr("id", "line_chart_title");
//
//    legend = svg_lines.append("g")
//        .attr("id", "legend")
//        .attr("transform", "translate("+(w - margin.right)+","+margin.top+")");
//
//    // Axes and Axes Titles
//
//    xAxis = d3.axisBottom(xScale);
//
//    xAxisGroup = svg_lines.append("g")
//        .attr("id", "x-axis-lines")
//        .attr("transform", "translate(0," + (h-margin.bottom) + ")")
//        .call(xAxis)
//
//    svg_lines
//        .append("text")
//        .attr("text-anchor", "middle")
//        .attr("fill", "black")
//        .attr("x", w / 2)
//        .attr("y", h - margin.bottom + 50)
//        .text("Rating");
//
//    yAxis = d3.axisLeft(yScale);
//
//    yAxisGroup = svg_lines.append("g")
//        .attr("id", "y-axis-lines")
//        .attr("transform", "translate(" + margin.left + ", 0)")
//        .call(yAxis)
//
//    svg_lines
//        .append("text")
//        .attr("text-anchor", "middle")
//        .attr("fill", "black")
//        .attr("x", - h/2)
//        .attr("y", 50)
//        .attr("transform", "rotate(-90)")
//        .text("Count");
//
//    // GT username text
//
//    svg_lines
//        .append("text")
//        .attr("text-anchor", "end")
//        .attr("fill", "black")
//        .attr("id", "credit")
//        .attr("x", w - 10 )
//        .attr("y", h - 10 )
//        .text("chein8");
//
//    // Add the chart title to the title group
//      title_text = title.append("text")
//        .attr("text-anchor", "middle")
//        .attr("x", w / 2)
//        .attr("y", margin.top-20)
//        .text("Board games by Rating 2015-2019");
//
//    // create elements - iterate through years and plot lines
//    cnt = 0
//    for (let i = year_min; i <= year_max; i++) {
//        // get filtered line data for each year
//        line_data = data_chart.filter(data_chart => data_chart.year === i)
//
//        // create line object and path for line on chart
//        line_obj = d3.line()
//            .x(function (d) { return xScale(d.rating); })
//            .y(function (d) { return yScale(d.bg_count); });
//
//        linePath = lines.append("path")
//            .data([line_data])
//            .attr("class", "line")
//            .attr("d", line_obj)
//            .attr("stroke", d3.schemeCategory10[cnt])
//            .attr("stroke-width", 2)
//            .attr("fill", "none");
//
//        // create circles for line
//
//        circles.selectAll()
//            .data(line_data)
//            .enter()
//            .append("circle")
//            .attr("class", "data-circle")
//            .attr("r", 4)
//            .attr("stroke", d3.schemeCategory10[cnt])
//            .attr("fill", d3.schemeCategory10[cnt])
//            .attr("cx", function (d) { return xScale(d.rating) })
//            .attr("cy", function (d) { return yScale(d.bg_count) })
//            .on("mouseover", function (d) {
//                // increase bubble size when selected
//                d3.select(this).attr("r", 6);
//                // For selected year (d.year) and rating (d.rating) build chart
//                barchart_data = data.filter(data => data.year === d.year).filter(data => data.average_rating === d.rating)
//                barchart_data.sort((a, b) => (a.users_rated <= b.users_rated) ? 1 : -1)
//                barchart_data = barchart_data.slice(0, 5)
//
//                //build barchart using data
//
//                // margin and size
//                margin_barchart = {top: 100, right: 100, bottom: 100, left: 100};
//                barchart_width = 600;
//                barchart_height = 400;
//                w_bar = barchart_width + margin_barchart.left + margin_barchart.right;
//                h_bar= barchart_height + margin_barchart.top + margin_barchart.bottom;
//
//                // append SVG
//                svg_barchart = d3.select("body").append("svg")
//                    .style("border", "solid")
//                    .attr("width", w_bar)
//                    .attr("height", h_bar)
//                    .attr("id", "barchart");
//
//                // append groups to barchart
//                bars = svg_barchart.append("g")
//                    .attr("id", "bars");
//
//                bar_x_axis_label = svg_barchart.append("g")
//                    .attr("id", "bar_x_axis_label");
//
//                bar_y_axis_label = svg_barchart.append("g")
//                    .attr("id", "bar_y_axis_label");
//
//                // title
//                title_bar = svg_barchart.append("g")
//                    .attr("id", "bar_chart_title")
//                    .append("text")
//                        .attr("text-anchor", "middle")
//                        .attr("x", w_bar / 2)
//                        .attr("y", margin_barchart.top-20)
//                        .text("Top 5 most rated games of "+d.year+" with rating "+d.rating);
//
//                // Scales
//                x_min_bar = 0;
//                x_max_bar = d3.max(barchart_data, function (d) { return d.users_rated; });
//
//                xScaleBar = d3.scaleLinear()
//                    .domain([x_min_bar, x_max_bar])
//                    .range([margin_barchart.left, w_bar - margin_barchart.right]);
//                yScaleBar = d3.scaleBand()
//                    .domain(barchart_data.map(a => a.name.slice(0, 10)))
//                    .range([margin_barchart.top, h_bar - margin_barchart.bottom]);
//
//                // Axes and Axes Titles
//
//                xAxisBar = d3.axisBottom(xScaleBar);
//
//                xAxisGroupBar = svg_barchart.append("g")
//                    .attr("id", "x-axis-bars")
//                    .attr("transform", "translate(0," + (h_bar-margin_barchart.bottom) + ")")
//                    .call(xAxisBar)
//
//                bar_x_axis_label
//                    .append("text")
//                    .attr("text-anchor", "middle")
//                    .attr("fill", "black")
//                    .attr("x", w_bar / 2)
//                    .attr("y", h_bar - margin_barchart.bottom + 50)
//                    .text("Number of users");
//
//                yAxisBar = d3.axisLeft(yScaleBar);
//
//                yAxisGroup = svg_barchart.append("g")
//                    .attr("id", "y-axis-bars")
//                    .attr("transform", "translate(" + margin_barchart.left + ", 0)")
//                    .call(yAxisBar)
//
//                bar_y_axis_label
//                    .append("text")
//                    .attr("text-anchor", "middle")
//                    .attr("fill", "black")
//                    .attr("x", - h_bar/2)
//                    .attr("y", 50)
//                    .attr("transform", "rotate(-90)")
//                    .text("Games");
//
//                // Elements
//                bars.selectAll("rect")
//                    .data(barchart_data)
//                    .enter()
//                    .append("rect")
//                    .attr("x", margin_barchart.left)
//                    .attr("y", function (d) { return yScaleBar(d.name.slice(0, 10)) })
//                    .attr("width", function (d) { return xScaleBar(d.users_rated) - margin.right })
//                    .attr("height", 20)
//                    .attr("fill", "teal");
//
//                if (barchart_data.length === 0) {
//                    //d3.selectAll("#barchart").attr("display", "none");
//
//                    children = document.getElementById('barchart').childNodes;
//
//                    function removeAllChildNodes(parent) {
//                        while (parent.firstChild) {
//                            parent.removeChild(parent.firstChild);
//                        }
//                    }
//
//                     // Loop through the children
//                     for(var c=0; c < children.length; c++) {
//                      if(children[c].style) {
//                       removeAllChildNodes(children[c]);
//                       d3.select(children[c]).attr("display", "none");
//                      }
//                     }
//
//                    //document.getElementById('barchart').style.display = 'none'
//
//                    return;  // do not display any chart if 0 games
//                }
//
//            })
//            .on("mouseout", function (d) {
//                // resume original bubble sie when deselected
//                d3.select(this).attr("r", 4);
//
//                // delete svg object based on id
//                d3.select("#barchart").remove();
//            });
//
//        legend
//            .append("circle")
//            .attr("class", "data-circle")
//            .attr("r", 4)
//            .attr("stroke", d3.schemeCategory10[cnt])
//            .attr("fill", d3.schemeCategory10[cnt])
//            .attr("cx", 0)
//            .attr("cy", cnt*20);
//
//        legend
//            .append("text")
//            .attr("fill", "black")
//            .attr("text-anchor", "start")
//            .attr("x", 10)
//            .attr("y", cnt*20 + 5)
//            .text(i);
//
//        cnt = cnt + 1;
//    }
//
//
//
//}).catch(function (error) {
//    console.log(error);
//})
