import React, { Component } from 'react';

import ExperimentHeader from './ExperimentHeader';
import ExperimentIntro from './ExperimentIntro';
import ExperimentImages from './ExperimentImages';
import ScatterPlot from './ScatterPlot';

import Histogram from './Histogram';

export default class Experiment extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: {}
        };
        this.requestData = this.requestData.bind(this);
        this.renderAll = this.renderAll.bind(this);
    }

    componentDidMount() {
        this.requestData();
    }

    requestData(props) {
        var request = new XMLHttpRequest();
        var expId = `${this.props.match.params.experiment}`;
        let params =  {
            id: expId
        };
        request.open('POST', 'http://localhost:5000/api/experiments', true);

        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            var rawdata = JSON.parse(request.responseText);
            var data = rawdata.exp;
            this.setState({
                data: data
            });
          } else {
            // We reached our target server, but it returned an error
          }
        };
        request.onerror = function() {
          // There was a connection error of some sort
        };
        request.send(JSON.stringify(params));
    }

    renderAll() {
        if (this.state.data.images) {
            return(
                <div>
                <ExperimentHeader
                    title={this.state.data.title}
                    date={this.state.data.date}
                    id={this.state.data._id.$oid}
                />
                <ExperimentIntro
                    summary={this.state.data.summary}
                    description={this.state.data.description}
                />
                <ExperimentImages
                    images={this.state.data.images}
                    histograms={this.state.data.histograms}
                />
                <div className="stokes-container">
                    <div className="histogram-stokes">
                        <h4>S1 Histograms</h4>
                        <Histogram
                            data={this.state.data.histograms.stokes.S1.data}
                            targetElement={'exp-s1-histogram'}
                            width={600}
                            height={300}
                            yTicks={10}
                        />
                        <div className="stokes-stats">
                            <h5>Statistics</h5>
                            <div>Data pts: {this.state.data.histograms.stokes.S1.stats.numpts}</div>
                            <div>Max: {this.state.data.histograms.stokes.S1.stats.max}</div>
                            <div>Min: {this.state.data.histograms.stokes.S1.stats.min}</div>
                            <div>Mean: {this.state.data.histograms.stokes.S1.stats.mean }</div>
                            <div>STD: {this.state.data.histograms.stokes.S1.stats.std }</div>
                        </div>
                    </div>
                </div>
                <div className="stokes-container">
                    <div className="histogram-stokes">
                        <h4>S2 Histograms</h4>
                        <Histogram
                            data={this.state.data.histograms.stokes.S2.data}
                            targetElement={'exp-s2-histogram'}
                            width={600}
                            height={300}
                            yTicks={10}
                        />
                        <div className="stokes-stats">
                            <h5>Statistics</h5>
                            <div className="calc">Data pts: {this.state.data.histograms.stokes.S2.stats.numpts }</div>
                            <div className="calc">Max: {this.state.data.histograms.stokes.S2.stats.max }</div>
                            <div className="calc">Min: {this.state.data.histograms.stokes.S2.stats.min}</div>
                            <div className="calc">Mean: {this.state.data.histograms.stokes.S2.stats.mean}</div>
                            <div className="calc">STD: {this.state.data.histograms.stokes.S2.stats.std}</div>
                        </div>
                    </div>
                </div>

                {/* <ScatterPlot data={this.state.data} /> */}
            </div>
            )
        }

    }



    render() {
        return(
            <div>
                {this.state.data ? this.renderAll() : 'Error'}
            </div>
        );
    }
}
