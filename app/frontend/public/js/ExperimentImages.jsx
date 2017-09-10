import React, { Component } from 'react';

import Histogram from './Histogram';

export default class ExperimentImages extends Component {
    constructor(props) {
        super(props);

        this.state = {
            activeImageModal: 0,
            showModal: true
        };

        this.renderImageModal = this.renderImageModal.bind(this);
        this.openImageModal = this.openImageModal.bind(this);
        this.renderHistogram = this.renderHistogram.bind(this);
    }

    renderHistogram(data, targetElement, width, height, yTicks) {
        if( data ) {
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
                        <img src={`http://localhost:5050/data/${this.props.images}/${img}.jpg`} />
                    </div>
                    <div className="exp-image-full-histogram">
                        <div className="histogram-large-container">
                            <h5>{LETTERS[img]} Histogram</h5>
                            {this.renderHistogram(this.props.histograms.measurements[LETTERS[img]], `exp-${LETTERS[img]}-modal-histogram`, 375, 200, 10)}
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    openImageModal(image) {
        d3.select('.exp-H-modal-histogram svg').remove();
        // d3.selectAll('bar').remove();
        this.setState({showModal: true, activeImageModal: image});
        this.renderImageModal(image);


        var svg = d3.select(".exp-H-modal-histogram").transition();
        // svg.selectAll('bar').duration(750)

    }

    render() {
        return(
            <div className="image-container">
                <h4>Images</h4>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('0')} src={`http://localhost:5050/data/${this.props.images}/0.jpg`} />
                    <span className="exp-image-subtitle">H.jpg</span>
                </div>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('90')} src={`http://localhost:5050/data/${this.props.images}/90.jpg`} />
                    <span className="exp-image-subtitle">V.jpg</span>
                </div>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('45')} src={`http://localhost:5050/data/${this.props.images}/45.jpg`} />
                    <span className="exp-image-subtitle">P.jpg</span>
                </div>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('135')} src={`http://localhost:5050/data/${this.props.images}/135.jpg`} />
                    <span className="exp-image-subtitle">M.jpg</span>
                </div>
                {this.state.showModal ?
                    this.renderImageModal(this.state.activeImageModal)
                :null}
            </div>
        )
    }
}
