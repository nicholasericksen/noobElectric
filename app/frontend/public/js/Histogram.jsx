import React, { Component } from 'react';

import classNames from 'classnames';

export default class Histogram extends Component {
    constructor(props) {
        super(props);
        this.state = {
            g: null,
            ledgend: []
        };


        this.onRef = this.onRef.bind(this);
        this.renderHistogram = this.renderHistogram.bind(this);
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.data !== this.props.data) {
            this.setState({ledgend: []});
            this.renderHistogram(nextProps.data);
        }
    }

    // shouldComponentUpdate() { console.log("COMponent should update"); return false }

    componentDidMount() {
        this.setState({ledgend: []});
        this.renderHistogram(this.props.data);
    }

    onRef(ref) {
        // this.setState({ g: d3.select(ref) }, () => this.renderHistogram(this.props.data))
    }

    renderHistogram(dataSet) {
            // Initialize Axis and dimensions

            var margin = {top: 20, right: 20, bottom: 70, left: 50},
                width = this.props.width - margin.left - margin.right,
                height = this.props.height - margin.top - margin.bottom;

            // Parse the date / time
            // var	parseDate = d3.time.format("%Y-%m").parse;
                var x = d3.scale.linear().range([0, width]);
                // var x = d3.scale.linear().range([width, 0]);
                var y = d3.scale.linear().range([height, 0]);

                var xAxis = d3.svg.axis()
                    .scale(x)
                    .orient("bottom")
                    .ticks(10);


                var yAxis = d3.svg.axis()
                    .scale(y)
                    .orient("left")
                    .ticks(this.props.yTicks);

                var targetElement = '.' + this.props.targetElement;
                d3.select(targetElement + ' svg').remove();
                var svg = d3.select(targetElement).append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                  .append("g")
                    .attr("transform",
                          "translate(" + margin.left + "," + margin.top + ")");

                var yMax = 0;
                var yMaxTmp = 0;

                if (dataSet.length > 0) {

                dataSet.map((experiment, index) => {
                    if (index === 0) {
                        yMax = d3.max(dataSet[0].data, function(d) { return d[1]; })
                    } else {
                        yMaxTmp = d3.max(dataSet[index].data, function(d) { return d[1]; })
                    }

                    if (yMaxTmp > yMax) {
                        yMax = yMaxTmp;
                    }

                });
                }
                  x.domain([-1, d3.max(dataSet[0].data, function(d) { return d[0]; })]);
                  y.domain([0, yMax]);

                  svg.append("g")
                      .attr("class", "x axis")
                      .attr("transform", "translate(0," + height + ")")
                      .call(xAxis)
                    .selectAll("text")
                      .style("text-anchor", "end")
                      .attr("dx", "-.8em")
                      .attr("dy", "-.55em")
                      .attr("transform", "rotate(-90)" );

                  svg.append("g")
                      .attr("class", "y axis")
                      .call(yAxis)
                    .append("text")
                      .attr("transform", "rotate(-90)")
                      .attr("y", 6)
                      .attr("dy", ".71em")
                      .style("text-anchor", "end")
                      .text("# of pxs");



                const COLORS = ['steelblue', 'red', 'grey', 'green', 'black', 'purple'];

                const tmpLedgendObject = [];

                dataSet.map((experiment, index) => {
                    svg.selectAll("bar")
                        .data(experiment.data)
                      .enter().append("rect")
                        .style("fill", COLORS[index])
                        .attr("x", function(d) { return x(d[0]); })
                        .attr("width", 2)
                        .attr("y", function(d) { return y(d[1]); })
                        .attr("height", function(d) { return height - y(d[1]); });


                    experiment.color = COLORS[index];

                    tmpLedgendObject.push(experiment);
                    this.setState({ledgend: tmpLedgendObject});
                })
    }

    render() {
        return(
            <div>
                <div className="ledgend">
                    {this.state.ledgend ? this.state.ledgend.map((experiment, index) => {
                        return (
                            <div>
                                <span className={classNames(["ledgend-color", experiment.color])}></span>
                                <span className="ledgend-experiment-title">{experiment.title ? experiment.title : 'tmp'}</span>
                            </div>
                        )
                    }) : null }
                </div>
            <svg width={this.props.width} height={this.props.height} className={this.props.targetElement}>
                <g ref={this.onRef}  />
            </svg>
            </div>
        );
    }
}
