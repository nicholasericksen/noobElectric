import React, { Component, PropTypes } from 'react';

import Experiment from './Experiment';

export default class Experiments extends Component {
    constructor(props) {
        super(props);

        this.state = {
            expIndex: 0
        };

        this.setExperimentData = this.setExperimentData.bind(this);
    }

    setExperimentData(index) {
        if (index !== this.state.expIndex) {
            this.setState({expIndex: index});
        }
    }

    renderExperiment() {
        // This remove all previous data points
        d3.selectAll("svg > *").remove();
        return (
            <Experiment
                data={this.props.data[this.state.expIndex]}
            />
        );
    }

    render() {
        return (
            <div className="exp">
                {this.props.data ?
                    this.props.data.map((experiment, index) => {
                        return(
                            <div key={index} onClick={() => this.setExperimentData(index)}>{experiment.title}</div>
                        )
                    })
                : null
                }
                {this.renderExperiment()}
            </div>
        );
    }
}
