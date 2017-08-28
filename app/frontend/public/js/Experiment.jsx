import React, { Component, PropTypes } from 'react';

export default class Experiment extends Component {
    render() {
        return (
            <div className="exp">
                <div className="header">
                    <div className="title">
                        <h3>Polarization Response of Invasive Species</h3>
                    </div>
                    <hr/>
                    <span className="exp-date">10.24.17</span>
                    <span className="exp-id">ID: 00001</span>
                </div>
                <div className="exp-introduction">
                    <p>
                        This exploratory study into how invasive Species utilize
                        polarization to perform certain actics within nature.
                        It is shown tyhat the longer a weed remains in the sun,
                        the more it adjusts its ability to absord polarized light.
                    </p>
                </div>
            </div>
        );
    }
}
