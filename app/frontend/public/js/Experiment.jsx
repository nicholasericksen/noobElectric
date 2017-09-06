import React, { Component, PropTypes } from 'react';

import Histogram from './Histogram';

export default class Experiment extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            activeIndex: 0
        };

        this.requestData = this.requestData.bind(this);
        this.renderExperiment = this.renderExperiment.bind(this);
        this.setExperimentData = this.setExperimentData.bind(this);
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
    renderExperiment(data, targetElement, width, height) {
        if (this.state.data) {
            console.log("IN the rendering process");
            return(
                <Histogram
                    data={data}
                    targetElement={targetElement}
                    width={width}
                    height={height}
                />
            );
        }

        return;
    }
    setExperimentData(index) {
        // d3.select(".histogram").remove();
        console.log('index', index);
        this.setState({activeIndex: index})

    }
    render() {


        return (
            <div className="exp">
                {this.state.data ?
                    this.state.data.map((experiment, index) => {
                        return(
                            <div onClick={() => this.setExperimentData(index)}>{experiment.title}</div>
                        )
                    })
                : null
                }
                <div className="exp-header">
                    <div className="title">
                        <h3>{this.state.data ? this.state.data[this.state.activeIndex].title : null}</h3>
                    </div>
                    <hr/>
                    <span className="exp-date">10.24.17</span>
                    <span className="exp-id">ID: 00001</span>
                </div>
                <div className="exp-introduction">
                    <p>
                        {this.state.data ? this.state.data[this.state.activeIndex].description : null}
                    </p>
                </div>

                <h5>S1 Histograms</h5>
                {this.state.data ? this.renderExperiment(this.state.data[this.state.activeIndex].histograms.stokes.S1, 'exp-s1-histogram', 600, 300) : null}

{/*                <p>H Histogram</p>
                {this.state.data ? this.renderExperiment(this.state.data[this.state.activeIndex].histograms.measurements.H, 'exp-H-histogram', 300, 150) : null}
                <div className="exp-H-histogram histogram"></div>

                <p>V Histogram</p>
                {this.state.data ? this.renderExperiment(this.state.data[this.state.activeIndex].histograms.measurements.V, 'exp-V-histogram', 300, 150) : null}
                <div className="exp-V-histogram histogram"></div>

                <h5>S2 Histograms</h5>
                {this.state.data ? this.renderExperiment(this.state.data[this.state.activeIndex].histograms.stokes.S2, 'exp-s2-histogram', 600, 300) : null}
                <div className="exp-s2-histogram histogram"></div>

                <p>P Histogram</p>
                {this.state.data ? this.renderExperiment(this.state.data[this.state.activeIndex].histograms.measurements.P, 'exp-P-histogram', 300, 150) : null}
                <div className="exp-P-histogram histogram"></div>

                <p>M Histogram</p>
                {this.state.data ? this.renderExperiment(this.state.data[this.state.activeIndex].histograms.measurements.M, 'exp-M-histogram', 300, 150) : null}
                <div className="exp-M-histogram histogram"></div> */}

            </div>
        );
    }
}
