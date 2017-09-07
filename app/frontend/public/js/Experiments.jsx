import React, { Component, PropTypes } from 'react';

import Experiment from './Experiment';
import ExperimentsMenu from './ExperimentsMenu';

export default class Experiments extends Component {
    constructor(props) {
        super(props);

        this.state = {
            expIndex: null
        };

        this.setExperimentData = this.setExperimentData.bind(this);
        this.renderContent = this.renderContent.bind(this);
    }



    setExperimentData (index) {
        console.log("index", index)
    //    if (index !== this.state.expIndex) {
            console.log("set experiment", this.state.expIndex);
            this.setState({expIndex: index});
    //    }
        // this.renderContent();
    }
    renderContent() {
        // This remove all previous data points
        let data = this.props.data;
        console.log("render content")
        console.log("ExpIndex", this.state.expIndex);
        if (this.state.expIndex !== null) {
            // d3.selectAll("svg > *").remove();
            console.log("HELPP");
            return (
                <Experiment
                    data={data[this.state.expIndex]}
                />
            );
        } else {
            console.log("render menu", this.props.data);
            return (
                <ExperimentsMenu
                    data={this.props.data}
                    onClick={this.setExperimentData}
                />
            );
        }

    }

    render() {
        return (
            <div className="exp">
                {this.renderContent()}
            </div>
        );
    }
}
