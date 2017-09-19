import React, { Component } from 'react';

import Histogram from './Histogram';

const LETTERS = {
    "0": "H",
    "90": "V",
    "45": "P",
    "135": "M"
};

export default class ExperimentImages extends Component {
    constructor(props) {
        super(props);

        this.state = {
            activeImageModal: 0,
            showModal: false
        };

        this.renderImageModal = this.renderImageModal.bind(this);
        this.openImageModal = this.openImageModal.bind(this);
    }

    renderImageModal(img) {

        if (img !== this.state.activeImageModal) {
        }
            // d3.selectAll("svg > *").remove();
        return (
            <div className="exp-image-modal">
                <div className="exp-image-modal-container">
                    <div className="exp-image-full">
                        <img src={`http://localhost:5050/data/${this.props.images}/${img}.png`} />
                    </div>
                    <div className="exp-image-full-histogram">
                        <div className="histogram-large-container">
                            <h5>{LETTERS[img]} Histogram</h5>
                            {/* this.renderHistogram(this.props.histograms.measurements[LETTERS[img]], `exp-${LETTERS[img]}-modal-histogram`, 375, 200, 10) */}
                            <Histogram
                                data={this.props.histograms.measurements[LETTERS[img]]}
                                targetElement={`exp-modal-histogram`}
                                width={375}
                                height={200}
                                yTicks={10}
                            />
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    openImageModal(img) {
        console.log(
            `exp-${LETTERS[img]}-modal-histogram`
        );
        // this.setState({showModal: false});
        // const svg = d3.select(`.exp-${LETTERS[img]}-modal-histogram`);
        // console.log("svg", svg);
        // svg.remove();
        // d3.selectAll('bar').remove();
        this.setState({showModal: true, activeImageModal: img});
        this.renderImageModal(img);

        // var svg =d3.select(`.exp-${LETTERS[img]}-modal-histogram`).transition();
        // svg.selectAll('bar').duration(750)
    }

    render() {
        console.log("this.state.histograms", this.props.histograms);
        return(
            <div className="image-container">
                <h4>Images</h4>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('0')} src={`http://localhost:5050/data/${this.props.images}/0.png`} />
                    <span className="exp-image-subtitle">H.png</span>
                </div>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('90')} src={`http://localhost:5050/data/${this.props.images}/90.png`} />
                    <span className="exp-image-subtitle">V.png</span>
                </div>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('45')} src={`http://localhost:5050/data/${this.props.images}/45.png`} />
                    <span className="exp-image-subtitle">P.png</span>
                </div>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('135')} src={`http://localhost:5050/data/${this.props.images}/135.png`} />
                    <span className="exp-image-subtitle">M.png</span>
                </div>
                {this.state.showModal ?
                    this.renderImageModal(this.state.activeImageModal)
                :null}
            </div>
        )
    }
}
