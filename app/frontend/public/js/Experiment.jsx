import React, { Component, PropTypes } from 'react';

import Histogram from './Histogram';

export default class Experiment extends Component {
    constructor(props) {
        super(props);

        this.state = {
            title: 'Experiment',
            description: 'This is an excperiment.',
            data: null,
            activeIndex: 0
        };

        this.requestData = this.requestData.bind(this);
        this.renderExperiments = this.renderExperiments.bind(this);
    }

    componentDidMount() {
        this.requestData();
    }


    requestData() {
        var request = new XMLHttpRequest();
        request.open('GET', 'http://localhost:5000/api', true);

        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            var rawdata = JSON.parse(request.responseText);
            var data = rawdata.exp;
            this.setState({
                title: rawdata.exp[this.state.activeIndex].title,
                description: rawdata.exp[this.state.activeIndex].description,
                data: data
            });
            console.log("DATAS", this.state.data);

          } else {
            // We reached our target server, but it returned an error
          }
        };

        request.onerror = function() {
          // There was a connection error of some sort
        };

        request.send();
    }
    renderExperiments() {
        this.state.data.map((experiment, index) => {
            console.log("EXpERIMENT", experiment);
            // const { date, description, title, _id } = experiment;

            return <div>hey</div>;

            // return (
            //     <div>
            //         <div>Hello</div>
            //         <div>{experiment.title}</div>
            //         <div>{experiment.date}</div>
            //         <div>{experiment.description}</div>
            //     </div>
            // );
        });
    }

    render() {

        // Initialize Axis and dimensions
        var margin = {top: 20, right: 20, bottom: 70, left: 40},
            width = 600 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

        // Parse the date / time
        // var	parseDate = d3.time.format("%Y-%m").parse;
        if (this.state.data) {
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
                .ticks(10);

            var svg = d3.select(".exp-s1-histogram").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform",
                      "translate(" + margin.left + "," + margin.top + ")");

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
                  .text("Value");

              if (this.state.data) {
                  x.domain([-1, d3.max(this.state.data[this.state.activeIndex].histograms.stokes.S1, function(d) { return d[0]; })]);
                  y.domain([0, d3.max(this.state.data[this.state.activeIndex].histograms.stokes.S1, function(d) { return d[1]; })]);

                  svg.selectAll("bar")
                      .data(this.state.data[this.state.activeIndex].histograms.stokes.S1)
                    .enter().append("rect")
                      .style("fill", "steelblue")
                      .attr("x", function(d) { return x(d[0]); })
                      .attr("width", 2)
                      .attr("y", function(d) { return y(d[1]); })
                      .attr("height", function(d) { return height - y(d[1]); });
            }
        }



        // console.log("D3", d3);
        return (
            <div className="exp">
                {this.state.data ? this.renderExperiments() : <div>Hey</div>}
                <div className="exp-header">
                    <div className="title">
                        <h3>{this.state.title}</h3>
                    </div>
                    <hr/>
                    <span className="exp-date">10.24.17</span>
                    <span className="exp-id">ID: 00001</span>
                </div>
                <span onClick={() => this.setState({activeIndex: 1})}>clapapapa</span>
                <div className="exp-introduction">
                    <p>
                        {this.state.description}
                    </p>
                </div>
                <Histogram
                    data={this.state.data}
                />
                <div className="exp-s1-histogram"></div>
            </div>
        );
    }
}
