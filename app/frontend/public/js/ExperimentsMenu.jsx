import React, { Component } from 'react';

export default class ExperimentsMenu extends Component {
    render() {
        return (
            <div>
                {this.props.data ?
                    this.props.data.map((experiment, index) => {
                        return(
                            <div className="exp-menu-item-container" onClick={() => this.props.onClick(index)}>
                                <h3 className="" key={index} >
                                    {experiment.title}
                                </h3>
                                <div className="exp-description">
                                    {experiment.description}
                                </div>
                                <div className="exp-buttons">
                                    <span>more</span>
                                    <span>compare</span>
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
