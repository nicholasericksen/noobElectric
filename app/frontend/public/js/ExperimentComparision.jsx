import React, { Component } from 'react';

import Histogram from './Histogram';
import ScatterPlot from './ScatterPlot';

export default class ExperimentComparision extends Component {
    constructor(props) {
        super(props);

        this.state = {
            experiments : [],
            meta: {},
            histogramDataset : null,
            glcmDataset: []
        }
        this.requestHistogramData = this.requestHistogramData.bind(this);
        this.requestMetaData = this.requestMetaData.bind(this);
        this.requestGlcmData = this.requestGlcmData.bind(this);
    }

    componentDidMount() {
        var ids = `${this.props.match.params.ids}`;
        const idArray = ids.split(',');

        idArray.map((id, index) => {
            const params =  {
                id: id
            };

            console.log("ID", id);
            this.requestMetaData(params);

            // this.requestGlcmData(params);
        });
    }
    requestMetaData(params) {
        fetch('http://localhost:5000/api/experiments', {method: 'POST', body: JSON.stringify(params)})
            .then((response) => {
                return response.json();
            })
            .then((rawdata) => {
                const data = rawdata.exp;
                const experiments = this.state.meta;
                const key = data._id.$oid;

                experiments[key] = data

                this.setState({
                    meta: experiments
                });

                if (data && data.stokes) {
                    const hist_params =  {
                        id: data.stokes.$oid
                    };
                    this.requestHistogramData(hist_params);
                }

                if (data && data.glcm) {
                    const glcm_params =  {
                        id: data.glcm.$oid
                    };
                    this.requestGlcmData(glcm_params);
                }
                console.log("THIS.state.experiments", this.state.experiments);
            })
            .catch((err) => {
                console.log("error getting the meta data");
            })
    }
    requestHistogramData(params) {
            // var request = new XMLHttpRequest();
            console.log("Params", params);

            fetch('http://localhost:5000/api/experiments/histograms', {method: 'POST', body: JSON.stringify(params)})
            .then((response) => {
                return response.json();
            })
            .then((rawdata) => {
                console.log("RESPONSEES", rawdata);
                var data = rawdata.exp;
                var dataset = [];
                if (data && data.histograms && data.histograms.stokes) {

                    const S1 = {meta_id: data.meta_id, data: data.histograms.stokes.S1.data, title: `S1`};
                    const S2 = {meta_id: data.meta_id, data: data.histograms.stokes.S2.data, title: `S2`};

                    dataset.push(S1);
                    dataset.push(S2);

                    const experiments = this.state.experiments;
                    experiments.push(dataset);

                    this.setState({
                        experiments: experiments
                    });
                }
            })
            .catch((err) => {
                console.log("Error fetching Histogram Data", err);
            })

    }
    requestGlcmData(params) {
        // var request = new XMLHttpRequest();

        fetch('http://localhost:5000/api/experiments/glcm', {method:'POST', body: JSON.stringify(params)})
        .then((response) => {
            return response.json();
        })
        .then((rawdata) => {
            var data = rawdata.exp;
            var dataset = this.state.glcmDataset;
            var scatterPlotData = [];
            var glcm = data.glcm;
            if (glcm) {

                glcm.map((sample, index) => {
                    // stokesScatter.push([sample.S[index][0], sample.S[index][1]])
                    scatterPlotData.push([sample.data.dissimilarity, sample.data.correlation]);
                })
                dataset.push(scatterPlotData);
                this.setState({
                    glcmDataset: dataset
                });
                console.log("this.state.glcmDataset", this.state.glcmDataset);
            }
        })
        .catch((err) => {
            console.log("There was en error gneerating GLCM", err);
        })

        // request.open('POST', 'http://localhost:5000/api/experiments/glcm', true);
        //
        // request.onload = () => {
        //   if (request.status >= 200 && request.status < 400) {
        //     var rawdata = JSON.parse(request.responseText);
        //     var data = rawdata.exp;
        //     var dataset = this.state.glcmDataset;
        //     var scatterPlotData = [];
        //     var glcm = data.glcm;
        //     if (glcm) {
        //
        //         glcm.map((sample, index) => {
        //             // stokesScatter.push([sample.S[index][0], sample.S[index][1]])
        //             scatterPlotData.push([sample.data.dissimilarity, sample.data.correlation]);
        //         })
        //         dataset.push(scatterPlotData);
        //         this.setState({
        //             glcmDataset: dataset
        //         });
        //         console.log("this.state.glcmDataset", this.state.glcmDataset);
        //     }
        //     else {
        //         // this.setState({data: data});
        //     }
        //
        //   } else {
        //     // We reached our target server, but it returned an error
        //   }
        // };
        // request.onerror = function() {
        //   // There was a connection error of some sort
        // };
        // request.send(JSON.stringify(params));
    }

    render() {
        let S1 = [];
        let S2 = [];
        console.log("META", this.state.meta);
        let stokes = this.state.experiments.length === Object.keys(this.state.meta).length ? this.state.experiments.map((experiment, index) => {
            debugger;
            const meta_id = this.state.experiments[index][index].meta_id;
            const title = this.state.meta[meta_id].title;

            let experimentS1 = {data: experiment[0].data, title: `S1 ${title}`};
            let experimentS2 = {data: experiment[1].data, title: `S2 ${title}`};

            S1.push(experimentS1);
            S2.push(experimentS2);
        }) : null;

        console.log("s1", S1);

        return(
            <div>

                {S1.length > 0 && typeof S1 !== undefined  ?
                    <div>
                        <h4>S1 Parameter</h4>
                        <Histogram
                            data={S1}
                            targetElement={'exp-stokes-S1-histograms'}
                            width={600}
                            height={300}
                            yTicks={10}
                        />
                    <h4>S2 Parameter</h4>
                        <Histogram
                            data={S2}
                            targetElement={'exp-stokes-S2-histograms'}
                            width={600}
                            height={300}
                            yTicks={10}
                        />

                    </div>
                 : null}
                 {this.state.glcmDataset.length > 0 && typeof this.state.glcmDataset !== undefined?
                     <div>
                         <h4>GLCM Comparison</h4>
                         <ScatterPlot
                             data={this.state.glcmDataset}
                             container={'glcm-scatter-plot'}
                         />
                     </div>
                     : null}

            </div>
        )
    }
}
