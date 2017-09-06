import React, { Component } from 'react';

import Histogram from './Histogram';

export default class Experiment extends Component {
    constructor(props) {
        super(props);

        this.renderExperiment = this.renderExperiment.bind(this);
    }

    renderExperiment(data, targetElement, width, height) {
        if (this.props.data) {
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

    render() {
        console.log('exp data', this.props.data);
        return(
            <div>
                <div className="exp-header">
                    <div className="title">
                        <h3>{this.props.data ? this.props.data.title : null}</h3>
                    </div>
                    <hr/>
                    <span className="exp-date">10.24.17</span>
                    <span className="exp-id">ID: 00001</span>
                </div>
                <div className="exp-introduction">
                    <p>
                        {this.props.data ? this.props.data.description : null}
                    </p>
                </div>

                <h5>S1 Histograms</h5>
                {this.props.data ? this.renderExperiment(this.props.data.histograms.stokes.S1, 'exp-s1-histogram', 600, 300) : null}

                <p>H Histogram</p>
                {this.props.data ? this.renderExperiment(this.props.data.histograms.measurements.H, 'exp-H-histogram', 300, 150) : null}

                <p>V Histogram</p>
                {this.props.data ? this.renderExperiment(this.props.data.histograms.measurements.V, 'exp-V-histogram', 300, 150) : null}

                <h5>S2 Histograms</h5>
                {this.props.data ? this.renderExperiment(this.props.data.histograms.stokes.S2, 'exp-s2-histogram', 600, 300) : null}

                <p>P Histogram</p>
                {this.props.data ? this.renderExperiment(this.props.data.histograms.measurements.P, 'exp-P-histogram', 300, 150) : null}

                <p>M Histogram</p>
                {this.props.data ? this.renderExperiment(this.props.data.histograms.measurements.M, 'exp-M-histogram', 300, 150) : null}
            </div>
        );
    }
}
