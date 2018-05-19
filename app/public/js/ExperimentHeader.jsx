import React, { Component } from 'react';

export default class ExperimentHeader extends Component {
    render() {
        return(
            <div className="exp-header">
                <div className="exp-title">
                    <h3>{this.props.title}</h3>
                </div>
                <hr/>
                <span className="exp-date">{this.props.date}</span>
                <span className="exp-id">ID: {this.props.id}</span>
            </div>
        )
    }
}
