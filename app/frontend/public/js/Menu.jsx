import React, { Component, PropTypes } from 'react';

export default class Menu extends Component {
    render() {
        return(
            <div className="home-menu">
                {this.props.labels.map((label, index) => (
                    <div key={index} onClick={() => this.props.onClick(index)} className="button">{label}</div>
                ))}
            </div>
        )
    }
}
