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
            stokesDataSet: null,
            index: 0,
            glcmDataset: null,
            histogramDataset: null
        };
        this.requestData = this.requestData.bind(this);
        this.renderAll = this.renderAll.bind(this);
        this.setStokesDataset = this.setStokesDataset.bind(this);
        this.renderStatistics = this.renderStatistics.bind(this);
        this.requestGlcmData = this.requestGlcmData.bind(this);
        this.requestHistogramData = this.requestHistogramData.bind(this);
    }

    componentDidMount() {
        this.requestData();
    }

    requestGlcmData(params) {
        var request = new XMLHttpRequest();

        request.open('POST', 'http://localhost:5000/api/experiments/glcm', true);

        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            var rawdata = JSON.parse(request.responseText);
            var data = rawdata.exp;
            var dataset = [];
            if (data.glcm) {
                this.setState({
                    glcmDataset: data.glcm
                });
            }
            else {
                // this.setState({data: data});
            }

          } else {
            // We reached our target server, but it returned an error
          }
        };
        request.onerror = function() {
          // There was a connection error of some sort
        };
        request.send(JSON.stringify(params));
    }

    requestHistogramData(params) {
            var request = new XMLHttpRequest();

            request.open('POST', 'http://localhost:5000/api/experiments/histograms', true);

            request.onload = () => {
              if (request.status >= 200 && request.status < 400) {
                var rawdata = JSON.parse(request.responseText);
                var data = rawdata.exp;
                var dataset = [];
                if (data.histograms && data.histograms.stokes) {
                    const S1 = {data: data.histograms.stokes.S1.data, title: `S1 ${this.state.data.title}`};
                    const S2 = {data: data.histograms.stokes.S2.data, title: `S2 ${this.state.data.title}`};

                    dataset.push(S1);
                    dataset.push(S2);

                    this.setState({
                        stokesDataSet: dataset,
                        histogramDataset: data
                    });
                    console.log("NICHOLAS", this.state.histogramDataset);
                }
                else {
                    // this.setState({data: data});
                }

              } else {
                // We reached our target server, but it returned an error
              }
            };
            request.onerror = function() {
              // There was a connection error of some sort
            };
            request.send(JSON.stringify(params));
    }

    requestData(props) {
        var request = new XMLHttpRequest();
        var expId = `${this.props.match.params.experiment}`;
        let params =  {
            id: expId
        };

        this.requestGlcmData(params);
        this.requestHistogramData(params);

        request.open('POST', 'http://localhost:5000/api/experiments', true);

        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            var rawdata = JSON.parse(request.responseText);
            var data = rawdata.exp;
            console.log("DATA", data);
            var dataset = [];

                this.setState({data: data});

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
        console.log("histogram", this.state.histogramDataset);
        console.log("jack", this.state.stokesDataSet);
        const S1 = this.state.histogramDataset ? {data: this.state.histogramDataset.histograms.stokes.S1.data, title: `S1 ${this.state.data.title}`} : [];
        const S2 = this.state.histogramDataset ? {data: this.state.histogramDataset.histograms.stokes.S2.data, title: `S2 ${this.state.data.title}`} : [];

        if (index === 0) {
            const dataSet = [];
            dataSet.push(S1);
            dataSet.push(S2);

            this.setState({
                stokesDataSet: dataSet,
                index: 0
            });
            console.log("cow", stokesDataSet);
        }
        else if ( index === 1) {
            // const S1 = this.state.histogramDataset[0]
            this.setState({
                index: 1,
                stokesDataSet: [S1]
            });
        } else if (index === 2) {
            // const S2 = this.state.histogramDataset[1]
            this.setState({
                index: 2,
                stokesDataSet: [S2]
            });

        }
    }
    renderStatistics() {
        return (
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
        )
    }

    renderAll() {
        if (this.state.data.images) {
            const scatterPlotData = [];
            const stokesScatter = [];
            let glcmData = this.state.glcmDataset ? this.state.glcmDataset : null;
            let glcm = '';
            if (glcmData) {
                glcm = JSON.parse(glcmData.replace(/'/g, '"'));
                glcm.map((sample, index) => {
                    // stokesScatter.push([sample.S[index][0], sample.S[index][1]])
                    scatterPlotData.push([sample.dissimilarity, sample.correlation])
                })
            }
            console.log("ScatterPlotData", scatterPlotData);
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
            {this.state.histogramDataset ?
                <ExperimentImages
                    images={this.state.data.images}
                    histograms={this.state.histogramDataset.histograms}
                />
            : null}

                <div className="stokes-container">
                    <div className="histogram-stokes">
                        <h4>Stokes Histograms</h4>
                        <div className="histogram-filter-container">
                            <span className="histogram-filter button btn" onClick={() => this.setStokesDataset(0)}>All</span>
                            <span className="histogram-filter button btn" onClick={() => this.setStokesDataset(1)}>S1</span>
                            <span className="histogram-filter button btn" onClick={() => this.setStokesDataset(2)}>S2</span>
                        </div>
                        {this.state.stokesDataSet ?
                            <Histogram
                                data={this.state.stokesDataSet}
                                targetElement={'exp-stokes-histograms'}
                                width={600}
                                height={300}
                                yTicks={10}
                            />
                        : null}

                    </div>
                </div>
                {this.state.data.histograms ? this.renderStatistics() : null}

                <div className="glcm-container">
                    <div className="glcm-scatter-plot-container">
                        {scatterPlotData ?
                            <div>
                                <h4>GLCM Scatter Plot</h4>
                                <ScatterPlot
                                    data={scatterPlotData}
                                    container={'glcm-scatter-plot'}
                                />
                            <h4>Stokes Comparision</h4>
                                {/*<ScatterPlot
                                    data={stokesScatter}
                                    container={'stokes-scatter-plot'}
                                />*/}
                            </div>

                        : null}
                    </div>
                    <div className="glcm-samples">
                        <h4>GLCM Samples</h4>
                    {glcm ? glcm.map((sample, index) => {
                        if (index <= 10) {
                            return(
                                <div className="sample-container">
                                    <img src={`http://localhost:8090/data/${sample.file}`} role="presentation"/>
                                    <div className="sample-stats-container">
                                        <div className="glcm-stats">
                                            <div>GLCM Correlation{sample.correlation}</div>
                                            <div> GLCM Disimilarity{sample.dissimilarity}</div>
                                        </div>
                                        <div className="s1-sample-stats-container">
                                            <div>S1 Mean: {sample.S1.stats.mean}</div>
                                            <div>S1 Variance: {sample.S1.stats.std}</div>
                                                <Histogram
                                                    data={[sample.S1]}
                                                    targetElement={`exp-S1-stokes-histograms-${index}`}
                                                    width={300}
                                                    height={150}
                                                    yTicks={2}
                                                />
                                        </div>

                                        <div className="s2-sample-stats-container">
                                            <div>S2 Mean: {sample.S2.stats.mean}</div>
                                            <div>S2 Variance: {sample.S2.stats.std}</div>
                                                <Histogram
                                                    data={[sample.S2]}
                                                    targetElement={`exp-S2-stokes-histograms-${index}`}
                                                    width={300}
                                                    height={150}
                                                    yTicks={2}
                                                />
                                        </div>

                                    </div>
                                </div>

                            )
                        } else {
                            return null;
                        }


                    }) : null}
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
