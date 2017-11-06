import React, { Component } from 'react';

export default class ScatterPlot extends Component {
    constructor(props) {
        super(props);

        this.renderData = this.renderData.bind(this);
    }
    componentWillReceiveProps(nextProps) {
        // if (nextProps.data !== this.props.data) {
            // this.setState({ledgend: []});
            console.log("nextProps", nextProps);
            this.renderData(nextProps.data);
        // }
    }
    renderData(dataSet) {
        d3.select(this.props.container + ' svg').remove();
            var margin = {top: 20, right: 15, bottom: 60, left: 60}
              , width = 600 - margin.left - margin.right
              , height = 300 - margin.top - margin.bottom;

              var xMin = d3.min(dataSet[0], function(d) { return d[0]; });
              var xMax = d3.max(dataSet[0], function(d) { return d[0]; });

              var yMin = d3.min(dataSet[0], function(d) { return d[1]; });
              var yMax = d3.max(dataSet[0], function(d) { return d[1]; });


            var x = d3.scale.linear()
                      .domain([ xMin, xMax ])
                      .range([0, width ]);

            var y = d3.scale.linear()
            	      .domain([ yMin, yMax ])
            	      .range([ height, 0 ]);

            var chart = d3.select('.' + this.props.container)
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
            .text("# of pxs")
        	.call(xAxis);

            // draw the y axis
            var yAxis = d3.svg.axis()
        	.scale(y)
        	.orient('left');

            // yAxis.append('text')
                // .text('#of pxs')

            main.append('g')
        	.attr('transform', 'translate(0,0)')
        	.attr('class', 'main axis date')
        	.call(yAxis);
            console.log("SCATTER PLOT DAta Ericksen", dataSet);
            var g = main.append("svg:g");
            const COLORS = ['steelblue', 'red', 'grey', 'green', 'black', 'purple'];
            dataSet.map((data, index) => {
                console.log("color", COLORS[index]);
                g.selectAll("scatter-dots")
                  .data(data)
                  .enter().append("svg:circle")
                      .style("fill", COLORS[index])
                      .attr("cx", function (d,i) { return x(d[0]); } )
                      .attr("cy", function (d) { return y(d[1]); } )
                      .attr("r", 4);
            })

    }
    componentDidMount() {
        this.renderData(this.props.data);
    }
    componentWillUnmount() {
        d3.select(this.props.container + ' svg').remove();
    }
    render() {
        return(
            <div>
                <svg width={600} height={300} className={this.props.container}></svg>
            </div>
        )
    }
}
