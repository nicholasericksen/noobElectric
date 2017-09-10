import React, { Component, PropTypes } from 'react';

import { Link } from 'react-router-dom';

export default class Menu extends Component {
    render() {
        return(
            <div className="home-menu">
                {this.props.labels.map((label, index) => {
                    return <Link key={index} className="button" to={label.url} >{label.label}</Link>
                })}
            </div>
        )
    }
}
