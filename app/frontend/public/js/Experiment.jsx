import React, { Component } from 'react';

import Histogram from './Histogram';

export default class Experiment extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showModal: false,
            activeImageModal: false
        };
        this.renderExperiment = this.renderExperiment.bind(this);
    }

    renderExperiment(data, targetElement, width, height, yTicks) {

        if (this.props.data) {
            return(
                <Histogram
                    data={data}
                    targetElement={targetElement}
                    width={width}
                    height={height}
                    yTicks={yTicks}
                />
                );
        }

        return;
    }

    openImageModal(image) {
        d3.select('.exp-H-modal-histogram svg').remove();
        // d3.selectAll('bar').remove();
        this.setState({showModal: true, activeImageModal: image});
        this.renderImageModal(image);


        var svg = d3.select(".exp-H-modal-histogram").transition();
        // svg.selectAll('bar').duration(750)

    }

    renderImageModal(img) {


        const LETTERS = {
            "0": "H",
            "90": "V",
            "45": "P",
            "135": "M"
        };
        if (img !== this.state.activeImageModal) {
        }


            // d3.selectAll("svg > *").remove();
        return (
            <div className="exp-image-modal">
                <div className="exp-image-modal-container">
                    <div className="exp-image-full">
                        <img src={`http://localhost:5050/data/${this.props.data.images}/${img}.jpg`} />
                    </div>
                    <div className="exp-image-full-histogram">
                        <div className="histogram-large-container">
                            <h5>{LETTERS[img]} Histogram</h5>
                            {this.props.data ? this.renderExperiment(this.props.data.histograms.measurements[LETTERS[img]], `exp-${LETTERS[img]}-modal-histogram`, 375, 200, 10) : null}
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    render() {
        // console.log('exp data', this.props.data);
        // const imgSrc = `http://localhost:5050//data/${this.props.data.images.jpg}/0.jpg`;
        // console.log("imgSrc", imgSrc);
        return(
            <div>
                <div className="exp-header">
                    <div className="exp-title">
                        <h3>{this.props.data ? this.props.data.title : null}</h3>
                    </div>
                    <hr/>
                    <span className="exp-date">{this.props.data.date}</span>
                    <span className="exp-id">ID: {this.props.data._id.$oid}</span>
                </div>
                <div className="exp-introduction">
                    <p>
                        {this.props.data ? this.props.data.summary : null}
                    </p>
                    <p>
                        {this.props.data ? this.props.data.description : null}
                    </p>
                </div>
                <div className="image-container">
                    <h4>Images</h4>
                    <div className="exp-image">
                        <img onClick={() => this.openImageModal('0')} src={`http://localhost:5050/data/${this.props.data.images}/0.jpg`} />
                        <span className="exp-image-subtitle">H.jpg</span>
                    </div>
                    <div className="exp-image">
                        <img onClick={() => this.openImageModal('90')} src={`http://localhost:5050/data/${this.props.data.images}/90.jpg`} />
                        <span className="exp-image-subtitle">V.jpg</span>
                    </div>
                    <div className="exp-image">
                        <img onClick={() => this.openImageModal('45')} src={`http://localhost:5050/data/${this.props.data.images}/45.jpg`} />
                        <span className="exp-image-subtitle">P.jpg</span>
                    </div>
                    <div className="exp-image">
                        <img onClick={() => this.openImageModal('135')} src={`http://localhost:5050/data/${this.props.data.images}/135.jpg`} />
                        <span className="exp-image-subtitle">M.jpg</span>
                    </div>
                    {this.state.showModal ?
                        this.renderImageModal(this.state.activeImageModal)
                    :null}



                </div>
                <div className="stokes-container">
                    <div className="histogram-stokes">
                        <h4>S1 Histograms</h4>
                        {this.props.data ? this.renderExperiment(this.props.data.histograms.stokes.S1.data, 'exp-s1-histogram', 600, 300, 10) : null}
                        <div className="stokes-stats">
                            <h5>Statistics</h5>
                            <div>Data pts: {this.props.data.histograms.stokes.S1.stats.numpts}</div>
                            <div>Max: {this.props.data.histograms.stokes.S1.stats.max}</div>
                            <div>Min: {this.props.data.histograms.stokes.S1.stats.min}</div>
                            <div>Mean: {this.props.data.histograms.stokes.S1.stats.mean}</div>
                            <div>STD: {this.props.data.histograms.stokes.S1.stats.std}</div>
                        </div>
                    </div>
                    {/*<div className="histogram-measurements">
                        <div className="histogram-small-container">
                            <h5>H Histogram</h5>
                            {this.props.data ? this.renderExperiment(this.props.data.histograms.measurements.H, 'exp-H-histogram', 300, 150, 5) : null}
                        </div>
                        <div className="histogram-small-container">
                            <h5>V Histogram</h5>
                            {this.props.data ? this.renderExperiment(this.props.data.histograms.measurements.V, 'exp-V-histogram', 300, 150, 5) : null}
                        </div>
                    </div> */}
                </div>
                <div className="stokes-container">
                    <div className="histogram-stokes">
                        <h4>S2 Histograms</h4>
                        {this.props.data ? this.renderExperiment(this.props.data.histograms.stokes.S2.data, 'exp-s2-histogram', 600, 300, 10) : null}
                        <div className="stokes-stats">
                            <h5>Statistics</h5>
                            <div className="calc">Data pts: {this.props.data.histograms.stokes.S2.stats.numpts}</div>
                            <div className="calc">Max: {this.props.data.histograms.stokes.S2.stats.max}</div>
                            <div className="calc">Min: {this.props.data.histograms.stokes.S2.stats.min}</div>
                            <div className="calc">Mean: {this.props.data.histograms.stokes.S2.stats.mean}</div>
                            <div className="calc">STD: {this.props.data.histograms.stokes.S2.stats.std}</div>
                        </div>
                    </div>
                    {/*
                    <div className="histogram-measurements">
                        <div className="histogram-small-container">
                            <h5>P Histogram</h5>
                            {this.props.data ? this.renderExperiment(this.props.data.histograms.measurements.P, 'exp-P-histogram', 300, 150, 5) : null}
                        </div>
                        <div className="histogram-small-container">
                            <h5>M Histogram</h5>
                            {this.props.data ? this.renderExperiment(this.props.data.histograms.measurements.M, 'exp-M-histogram', 300, 150, 5) : null}
                        </div>
                    </div> */}
                </div>
            </div>
        );
    }
}
