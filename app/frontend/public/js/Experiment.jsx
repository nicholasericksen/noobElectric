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
            data: {},
            stokesDataSet: []
        };
        this.requestData = this.requestData.bind(this);
        this.renderAll = this.renderAll.bind(this);
        this.setStokesDataset = this.setStokesDataset.bind(this);
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
            const dataSet = [];
            dataSet.push(data.histograms.stokes.S1.data);

            dataSet.push(data.histograms.stokes.S2.data);

            this.setState({
                data: data,
                stokesDataSet: dataSet
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

    setStokesDataset(index) {
        const S1 = this.state.data.histograms.stokes.S1.data;
        const S2 = this.state.data.histograms.stokes.S2.data;

        if (index === 0) {
            const dataSet = [];
            dataSet.push(S1);
            dataSet.push(S2);

            this.setState({
                stokesDataSet: dataSet
            });
        }
        if ( index === 1) {
            this.setState({
                stokesDataSet: [S1]
            });
        } else if (index === 2) {

            this.setState({
                stokesDataSet: [S2]
            });

        }
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
                        <h4>Stokes Histograms</h4>
                        <div className="histogram-filter-container">
                            <span className="histogram-filter button btn" onClick={() => this.setStokesDataset(0)}>All</span>
                            <span className="histogram-filter button btn" onClick={() => this.setStokesDataset(1)}>S1</span>
                            <span className="histogram-filter button btn" onClick={() => this.setStokesDataset(2)}>S2</span>
                        </div>
                        <Histogram
                            data={this.state.stokesDataSet}
                            targetElement={'exp-stokes-histograms'}
                            width={600}
                            height={300}
                            yTicks={10}
                        />

                    </div>
                </div>
                <div className="stokes-stats-container">
                    <h4>Statistics</h4>
                        <div className="stokes-stats">
                            <h5>S1</h5>
                            <div>Data pts: {this.state.data.histograms.stokes.S1.stats.numpts}</div>
                            <div>Max: {this.state.data.histograms.stokes.S1.stats.max}</div>
                            <div>Min: {this.state.data.histograms.stokes.S1.stats.min}</div>
                            <div>Mean: {this.state.data.histograms.stokes.S1.stats.mean }</div>
                            <div>STD: {this.state.data.histograms.stokes.S1.stats.std }</div>
                        </div>
                        <div className="stokes-stats">
                            <h5>S2</h5>
                            <div className="calc">Data pts: {this.state.data.histograms.stokes.S2.stats.numpts }</div>
                            <div className="calc">Max: {this.state.data.histograms.stokes.S2.stats.max }</div>
                            <div className="calc">Min: {this.state.data.histograms.stokes.S2.stats.min}</div>
                            <div className="calc">Mean: {this.state.data.histograms.stokes.S2.stats.mean}</div>
                            <div className="calc">STD: {this.state.data.histograms.stokes.S2.stats.std}</div>
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
