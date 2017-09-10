import React, { Component, PropTypes } from 'react';

import Experiment from './Experiment';
import ExperimentsMenu from './ExperimentsMenu';

export default class Experiments extends Component {
    constructor(props) {
        super(props);

        this.state = {
            expIndex: null,
            compareIndexes: []
        };

        this.setExperimentData = this.setExperimentData.bind(this);
        this.renderContent = this.renderContent.bind(this);
        this.compareButtonClick = this.compareButtonClick.bind(this);
    }



    setExperimentData (index) {
    //    if (index !== this.state.expIndex) {
            this.setState({expIndex: index});
    //    }
    }

    compareButtonClick(index) {
        const indexes = this.state.compareIndexes;
        indexes.push(index);

        this.setState({
            compareIndexes: indexes
        });

        if (this.state.compareIndexes.length() === 2) {

        }
        console.log("compareIndex", this.state.compareIndexes);
    }

    renderContent() {
        let data = this.props.data;
        if (this.state.expIndex !== null) {
            d3.selectAll("svg > *").remove();
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
                    compareClick={this.compareButtonClick}
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
