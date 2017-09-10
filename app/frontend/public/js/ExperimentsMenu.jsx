import React, { Component } from 'react';

export default class ExperimentsMenu extends Component {
    render() {
        return (
            <div>
                {this.props.data ?
                    this.props.data.map((experiment, index) => {
                        return(
                            <div className="exp-menu-item-container">
                                <h3 className="" key={index} onClick={() => this.props.onClick(index)}>
                                    {experiment.title}
                                </h3>
                                <div className="exp-description">
                                    {experiment.summary}
                                </div>
                                <div className="exp-buttons">
                                    <span className="exp-menu-more exp-btn" onClick={() => this.props.onClick(index)}>more</span>
                                    <span className="exp-menu-compare exp-btn" onClick={() => this.props.compareClick(index)}>compare</span>
                                </div>
                                <hr />
                            </div>
                        )
                    })
                : null
                }
            </div>
        )
    }
}
