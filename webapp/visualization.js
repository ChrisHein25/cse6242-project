// margin and size
var margin = {top: 100, right: 100, bottom: 100, left: 100};
var chart_width = 600;
var chart_height = 400;
var w = chart_width + margin.left + margin.right;
var h = chart_height + margin.top + margin.bottom;

// append SVG
var svg = d3.select("#visualization").append("svg")
    .style("border", "solid")
    .attr("width", w)
    .attr("height", h);

// append major groups

// load all csv data as Promises

var injury_data_path = "../time_graphs/html/injuries_open_refine.csv";
var player_data_path = "./data/player_clusters_py.csv";
var nodes_path = "./data/nodes.csv";
var edges_path = "./data/edges.csv";

// helper functions
const timeConv = d3.timeParse("%m/%d/%Y")

Promise.all([
    d3.csv(injury_data_path, function (d) {
        return {
            // format data attributes
            date: timeConv(d["Date"])
        }
    }),
    d3.csv(nodes_path, function (d) {
        return {
            // format data attributes
            id: parseInt(d["id"]),
            name: String(d["name"]).trim(),
            group: parseInt(d["group"]),
            avg_min: parseFloat(d["avg_min"])
        }
    }),
    d3.csv(edges_path, function (d) {
        return {
            // format data attributes
            source: parseInt(d["source"]),
            target: parseInt(d["target"])
        }
    })

]).then(function(data) {
    injury_data = data[0];
    //clustering_data = data[1];
    nodes = data[1];
    edges = data[2];
    ready(nodes, edges, injury_data);
}).catch(function(err) {
    // handle error here
})

function ready(nodes, edges, injury_data) {
    // based on current user selection prepare inputs to the Graph
    // grab selection items like dropdowns from the DOM
    // will eventually need listerners which are in Cloropleth.js code from HW2

    options = {"stuff": "selected by above logic"};
    createGraph(nodes, edges, injury_data, options); // with selected inputs build the Graph
}

function createGraph(nodes_orig, edges, injury_data, options){

    width = w;
    height = h;

    links = edges;
    //nodes = nodes;

    nodes = {};

    // compute the distinct nodes from the links and initialize degree at 0
    links.forEach(function(link) {
      link.source = nodes[link.source] || (nodes[link.source] = {id: link.source, degree: 0});
      link.target = nodes[link.target] || (nodes[link.target] = {id: link.target, degree: 0});
    });

    // for each node find how many times it occurs in the links and increment degree
    maxDegree = 0; // track max degree of set
    links.forEach(function(link) {
      // increment degree of both source and target by 1
      nodes[link.source.id].degree = nodes[link.source.id].degree + 1
      nodes[link.target.id].degree = nodes[link.target.id].degree + 1
      if (nodes[link.source.id].degree > maxDegree) {
        maxDegree = nodes[link.source.id].degree;
      } else if (nodes[link.target.id].degree > maxDegree) {
        maxDegree = nodes[link.target.id].degree;
      }
    });

    // grab additional node info from input node data
    for (const [key, value] of Object.entries(nodes)) {
      nodes[key]['test'] = 'answer' // add
    }

    var force = d3.forceSimulation()
      .nodes(d3.values(nodes))
      .force("link", d3.forceLink(links).distance(1))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX())
      .force("y", d3.forceY())
      .force("charge", d3.forceManyBody().strength(-5))
      .alphaTarget(1)
      .on("tick", tick);

    // add the links
    var path = svg.append("g")
      .selectAll("path")
      .data(links)
      .enter()
      .append("path");

    // define the nodes
    var node = svg.selectAll(".node")
      .data(force.nodes())
      .enter().append("g")
      .attr("class", "node")
//      .call(d3.drag()
//          .on("start", dragstarted)
//          .on("drag", dragged)
//          .on("end", dragended))

    // add the nodes
    node.append("circle")
      .attr("id", function(d){ d.id })
      .attr("r", function (d) { return d.degree })
      //.attr("fill", function (d) { return "rgb(?, ?, ?)".replaceAll("?", 250 - (d.degree / maxDegree ) * 250) });

    // add the curvy lines
    function tick() {
      path.attr("d", function(d) {
          var dx = d.target.x - d.source.x,
              dy = d.target.y - d.source.y,
              dr = Math.sqrt(dx * dx + dy * dy);
          return "M" +
              d.source.x + "," +
              d.source.y + "A" +
              dr + "," + dr + " 0 0,1 " +
              d.target.x + "," +
              d.target.y;
      });

      // add edge styling
      path.attr("stroke", "gray");
      path.attr("fill", "none");
      path.attr("stroke-width", "0.5px");

      node.attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
      });

    };

    // add listener for double click
    //node.selectAll("circle")
    //.on("mousedown", function (d) {
    //    console.log(' ')
    //    console.log(' ')
    //    console.log('mousedown detected');
    //    d3.select(this).attr("fill", "yellow");
    //    d.fixed = true;
    //    d.fx = d.x;
    //    d.fy = d.y;
    //    console.log('mousedown finished');
    //})
//    .on("dblclick", function (d) {
//        console.log('double click detected');
//        d.fx = null;
//        d.fy = null;
//        d.fixed = false;
//        d3.select(this).attr("fill", "rgb(?, ?, ?)".replaceAll("?", 250 - (d.degree / maxDegree ) * 250));
//        console.log('double click finished');
//    });
//
//    function dragstarted(d) {
//      if (!d3.event.active) force.alphaTarget(0.3).restart();
//      d.fixed = true;
//      d.fx = d.x;
//      d.fy = d.y;
//      d3.select(d3.select(this)._groups[0][0].children[0]).attr("fill", "yellow");
//    };
//
//    function dragged(d) {
//      d.fx = d3.event.x;
//      d.fy = d3.event.y;
//    };
//
//    function dragended(d) {
//      if (!d3.event.active) force.alphaTarget(0);
//      if (d.fixed == true) {
//          d.fx = d.x;
//          d.fy = d.y;
//          console.log('detected that fixed is true')
//      }
//      else {
//          d.fx = null;
//          d.fy = null;
//      }
//    };

    // append labels to nodes
//    var labels = node.append("text")
//    .text(function (d) { return d.name; })
//    .attr('x', 10)
//    .attr('y', -10)
//    .attr('font-weight', 'bold')



}


//
//
//
//
//
//
//
//
//
//
//
//
//// load example csv data that will eventually get replaced with real playing style data
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
