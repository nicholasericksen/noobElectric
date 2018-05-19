import React, { Component } from 'react';

import Histogram from './Histogram';

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
        let histogramData = {data: this.props.histograms.measurements[img], title:this.props.title};

        return (
            <div className="exp-image-modal">
                <div className="exp-image-modal-container">
                    <div className="exp-image-full">
                        <img src={`http://localhost:8090/data/${this.props.images}/${img}.png`} />
                    </div>
                    <div className="exp-image-full-histogram">
                        <div className="histogram-large-container">
                            <h5>{img} Histogram</h5>
                            <Histogram
                                data={[histogramData]}
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
        this.setState({showModal: true, activeImageModal: img});
        this.renderImageModal(img);
    }

    render() {
        return(
            <div className="image-container">
                <h4>Images</h4>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('H')} src={`http://localhost:8090/data/${this.props.images}/H.png`} />
                    <span className="exp-image-subtitle">H.png</span>
                </div>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('V')} src={`http://localhost:8090/data/${this.props.images}/V.png`} />
                    <span className="exp-image-subtitle">V.png</span>
                </div>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('P')} src={`http://localhost:8090/data/${this.props.images}/P.png`} />
                    <span className="exp-image-subtitle">P.png</span>
                </div>
                <div className="exp-image">
                    <img onClick={() => this.openImageModal('M')} src={`http://localhost:8090/data/${this.props.images}/M.png`} />
                    <span className="exp-image-subtitle">M.png</span>
                </div>
                {this.state.showModal ?
                    this.renderImageModal(this.state.activeImageModal)
                :null}
            </div>
        )
    }
}
