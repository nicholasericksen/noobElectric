import React, { Component } from 'react';

export default class ScatterPlot extends Component {
    constructor(props) {
        super(props);

        this.renderData = this.renderData.bind(this);
    }
    renderData() {
        console.log("this.props.data", this.props.data)
        var S1data = this.props.data.histograms.stokes.S1.data;
        var S2data = this.props.data.histograms.stokes.S2.data;

        var data = [];

        for (var i = 0; i < S1data.length; i++) {
            data[i] = [S1data[i], S2data[i]];
        }
        console.log("data", data);

    var margin = {top: 20, right: 15, bottom: 60, left: 60}
      , width = 960 - margin.left - margin.right
      , height = 500 - margin.top - margin.bottom;

    var x = d3.scale.linear()
              .domain([0, d3.max(data, function(d) { return d[0]; })])
              .range([ 0, width ]);

    var y = d3.scale.linear()
    	      .domain([0, d3.max(data, function(d) { return d[1]; })])
    	      .range([ height, 0 ]);

    var chart = d3.select('body')
	.append('svg:svg')
	.attr('width', width + margin.right + margin.left)
	.attr('height', height + margin.top + margin.bottom)
	.attr('class', 'chart')

    var main = chart.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
	.attr('width', width)
	.attr('height', height)
	.attr('class', 'main')

    // draw the x axis
    var xAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom');

    main.append('g')
	.attr('transform', 'translate(0,' + height + ')')
	.attr('class', 'main axis date')
	.call(xAxis);

    // draw the y axis
    var yAxis = d3.svg.axis()
	.scale(y)
	.orient('left');

    main.append('g')
	.attr('transform', 'translate(0,0)')
	.attr('class', 'main axis date')
	.call(yAxis);

    var g = main.append("svg:g");

    g.selectAll("scatter-dots")
      .data(data)
      .enter().append("svg:circle")
          .attr("cx", function (d,i) { return x(d[0]); } )
          .attr("cy", function (d) { return y(d[1]); } )
          .attr("r", 8);
    }
    componentDidMount() {
        this.renderData();
    }
    render() {
        return(
            <div>Hello</div>
        )
    }
}
