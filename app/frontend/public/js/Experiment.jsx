import React, { Component } from 'react';

import io from 'socket.io-client'

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
            glcmDataset: [],
            histogramDataset: null,
            hasGlcmData: false,
            hasStokesData: false,
            params: {}
        };

        this.socket = io(`http://localhost:5000/test`);

        this.requestData = this.requestData.bind(this);
        this.renderAll = this.renderAll.bind(this);
        this.setStokesDataset = this.setStokesDataset.bind(this);
        this.renderStatistics = this.renderStatistics.bind(this);
        this.requestGlcmData = this.requestGlcmData.bind(this);
        this.requestHistogramData = this.requestHistogramData.bind(this);
        this.generateGlcmData = this.generateGlcmData.bind(this);
        this.generateHistogramData = this.generateHistogramData.bind(this);
        this.requestBGR = this.requestBGR.bind(this);
    }
    componentWillUnmount() {
        this.setState({

        })
    }

    componentDidMount() {
        this.requestData();
        var expId = `${this.props.match.params.experiment}`;
        let params =  {
            id: expId,
            skip: 0,
            limit: 50
        };
        this.socket.on(`glcm_sent`, (rawdata) => {
                // console.log(data);
                console.log("DATATATA", rawdata.exp);
                // this.setVoltage(data);
                // var rawdata = JSON.parse(request.responseText);
                var data = rawdata.exp;
                console.log("nnnn", data);
                var dataset = this.state.glcmDataset;
                console.log("dataset", data);
                let final = dataset.concat(data);
                console.log("dasdsad", final);
                if (final.length > 0) {
                    this.setState({
                        glcmDataset: final,
                        hasGlcmData: true
                    });
                    let new_params = params;
                    params['skip'] = params['limit'];
                    params['limit'] += 50;

                    setTimeout(() => this.socket.emit(`request_glcm_samples`, JSON.stringify(params)), 500);
                }
                else {
                    this.setState({hasGlcmData: false});
                }
                // socket.emit(`message`, 'hey');
                console.log("the state version", this.state.glcmDataset);
        });



        // this.interval = setInterval(() => {
            console.log("EMIT");
        this.socket.emit(`request_glcm_samples`, JSON.stringify(params));
        // this.requestGlcmData(params);
        // this.requestHistogramData(params);
    }

    requestGlcmData(params) {
        var request = new XMLHttpRequest();

        request.open('POST', 'http://localhost:5000/api/experiments/glcm');

        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            var rawdata = JSON.parse(request.responseText);
            var data = rawdata.exp;
            var dataset = [];
            if (data && data.glcm) {
                this.setState({
                    glcmDataset: data.glcm,
                    hasGlcmData: true
                });
            }
            else {
                this.setState({hasGlcmData: false});
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

            request.open('POST', 'http://localhost:5000/api/experiments/histograms');

            request.onload = () => {
              if (request.status >= 200 && request.status < 400) {
                var rawdata = JSON.parse(request.responseText);
                var data = rawdata.exp;
                var dataset = [];
                if (data && data.histograms && data.histograms.stokes) {
                    const S1 = {data: data.histograms.stokes.S1.data, title: `S1 ${this.state.data.title}`};
                    const S2 = {data: data.histograms.stokes.S2.data, title: `S2 ${this.state.data.title}`};

                    dataset.push(S1);
                    dataset.push(S2);

                    this.setState({
                        stokesDataSet: dataset,
                        histogramDataset: data
                    });
                    this.setState({hasStokesData: true})
                }
                else {
                    this.setState({hasStokesData: false});
                }

              } else {
                // We reached our target server, but it returned an error
              }
            };
            request.onerror = function(err) {
              // There was a connection error of some sort
              console.log('err', err)
            };
            request.send(JSON.stringify(params));
    }

    requestBGR(params) {
        fetch('http://localhost:5000/api/experiments/histograms/bgr', {method: 'POST', body: JSON.stringify(params)})
        .then((response) => {
            return response.json();
        })
        .then((rawdata) => {
            console.log("cat", rawdata);
            this.setState({bgrDataset: rawdata});
        })
    }

    requestData(props) {
        var request = new XMLHttpRequest();
        var expId = `${this.props.match.params.experiment}`;
        let params =  {
            id: expId
        };
        this.setState({ params: {id: expId}});

        // this.requestGlcmData(params);
        // this.requestHistogramData(params);

        request.open('POST', 'http://localhost:5000/api/experiments');

        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            var rawdata = JSON.parse(request.responseText);
            var data = rawdata.exp;
            var dataset = [];

            this.setState({data: data});

            if (data && data.stokes) {
                const hist_params =  {
                    id: data.stokes.$oid
                };
                console.log("PARAMS", params)
                this.requestHistogramData(params);

            }

            if (data && data.stokes_bgr) {
                this.requestBGR(params);
            }

            if (data && data.glcm) {
                const glcm_params = {
                    id: data.glcm.$oid
                };

                // this.requestGlcmData(params)
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

    setStokesDataset(index) {
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

    generateGlcmData() {
        var xhr = new XMLHttpRequest();
        var expId = `${this.props.match.params.experiment}`;
        const images = this.state.data.images;
        let params =  {
            id: expId,
            images: images
        };
        // fetch('http://localhost:5000/api/generate/glcm', params, )
        console.log("PARAMS", params);
        xhr.open('POST', 'http://localhost:5000/api/generate/glcm', true);

        xhr.onload = () => {
            if(xhr.status >= 200 && xhr.status < 400) {
                console.log("successful upload");
                this.requestGlcmData(params);
            } else {
                console.log("An error was returned")
            }
        }

        xhr.onerror = function(err) {
            console.log("error: ", err);
        }

        xhr.send(JSON.stringify(params));
    }

    generateHistogramData() {
        var xhr = new XMLHttpRequest();
        var expId = `${this.props.match.params.experiment}`;
        const images = this.state.data.images;
        let params =  {
            id: expId,
            images: images
        };
        xhr.open('POST', 'http://localhost:5000/api/generate/stokes', true);

        xhr.onload = () => {
            if(xhr.status >= 200 && xhr.status < 400) {
                console.log("successful upload");
                // var tmpArr = this.state.experiments;
                // var rawdata = JSON.parse(xhr.responseText).data;
                // var data = tmpArr.concat(rawdata);
                // this.setState({
                //     experiments: data
                // });
                this.requestHistogramData(params);
            } else {
                console.log("An error was returned")
            }
        }

        xhr.onerror = function(err) {
            console.log("error: ", err);
        }

        xhr.send(JSON.stringify(params));
    }

    renderAll() {
        if (this.state.data.images) {
            const scatterPlotData = [];
            const stokesScatter = [];
            // let glcm = this.state.glcmDataset && this.state.glcmDataset.length > 1 ? this.state.glcmDataset : [];
            // console.log('glcm', this.state.glcmDataset.length)
            // if (glcm) {
                console.log("bout to map");
                this.state.glcmDataset.map((sample, index) => {
                    scatterPlotData.push([sample.glcm.dissimilarity, sample.glcm.correlation])
                })
            // }
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
                    id={this.state.data._id.$oid}
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
                        {this.state.hasStokesData ?
                            <div className="histogram-filter-container">
                                <span className="histogram-filter button btn" onClick={() => this.setStokesDataset(0)}>All</span>
                                <span className="histogram-filter button btn" onClick={() => this.setStokesDataset(1)}>S1</span>
                                <span className="histogram-filter button btn" onClick={() => this.setStokesDataset(2)}>S2</span>
                            </div>
                            :
                            <div onClick={this.generateHistogramData}>Generate Histogram</div>
                        }

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
                                {this.state.hasGlcmData ?
                                    <ScatterPlot
                                        data={[scatterPlotData]}
                                        container={'glcm-scatter-plot'}
                                    />
                                    :
                                    <div className="button" onClick={this.generateGlcmData}>Generate GLCM</div>
                                }
                            </div>

                        : null}
                    </div>
                    <div className="glcm-samples">
                        <h4>GLCM Samples</h4>
                    {this.state.glcmDataset.length > 1 ? this.state.glcmDataset.map((sample, index) => {
                        if (index <= 10) {
                            return(
                                <div className="sample-container">
                                    <img src={`http://localhost:8090/data/${sample.stokes.filename}`} role="presentation"/>
                                    <div className="sample-stats-container">
                                        <div className="glcm-stats">
                                            <div>GLCM Correlation{sample.glcm.correlation}</div>
                                            <div> GLCM Disimilarity{sample.glcm.dissimilarity}</div>
                                        </div>
                                        <div className="s1-sample-stats-container">
                                            <div>S1 Mean: {sample.stokes.S1.stats.mean}</div>
                                            <div>S1 Variance: {sample.stokes.S1.stats.std}</div>
                                                <Histogram
                                                    data={[sample.stokes.S1]}
                                                    targetElement={`exp-S1-stokes-histograms-${index}`}
                                                    width={300}
                                                    height={150}
                                                    yTicks={2}
                                                />
                                        </div>

                                        <div className="s2-sample-stats-container">
                                            <div>S2 Mean: {sample.stokes.S2.stats.mean}</div>
                                            <div>S2 Variance: {sample.stokes.S2.stats.std}</div>
                                                <Histogram
                                                    data={[sample.stokes.S2]}
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
