import React, { Component } from 'react';

export default class ExperimentIntro extends Component {
    render() {
        return(
            <div className="exp-introduction">
                <p>
                    {this.props.summary}
                </p>
                <p>
                    {this.props.description}
                </p>
            </div>
        )
    }
}
