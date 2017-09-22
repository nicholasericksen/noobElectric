import React, { Component } from 'react';

import { Link } from 'react-router-dom';

export default class ExperimentsMenu extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: [],
            compareList: []
        }

        this.requestData = this.requestData.bind(this);
    }

    componentDidMount() {
        this.requestData();
    }

    requestData() {
        var request = new XMLHttpRequest();
        request.open('GET', 'http://localhost:5000/api', true);

        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            var rawdata = JSON.parse(request.responseText);
            var data = rawdata.exp;
            this.setState({
                data: data
            });
        // console.log("this.state.data", this.state.data);
          } else {
            // We reached our target server, but it returned an error
          }

        };
        request.onerror = function() {
          // There was a connection error of some sort
        };

        request.send();
    }
    addCompare(id) {
        let list = this.state.compareList;
        list.push(id);
        this.setState({
            compareList: list
        });
        console.log("compare list", this.state.compareList);
    }

    render() {
        const data = this.state.data ? this.state.data : [];

        return (
            <div>
                <Link className="button" to={'/experiments/new'}>
                    { /*<div className="experiment-button">
                        <span className="glyphicon glyphicon-plus" aria-hidden="true"></span>
                    </div> */}
                    new
                </Link>
                <Link className="button" to={`/experiments/compare/${this.state.compareList}`}>compare</Link>
                {data ?
                    data.map((experiment, index) => {
                        return(
                            <div key={index} className="exp-menu-item-container">
                                <h3 className="" key={index}>
                                    {experiment.title}
                                </h3>
                                <div className="exp-description">
                                    {experiment.summary}
                                </div>
                                <div className="exp-buttons">
                                    <Link className="button" key={index} to={`/experiments/${experiment._id.$oid}`}>more</Link>
                                    <span className="button" onClick={() => this.addCompare(experiment._id.$oid)}>compare</span>
                                    {/*<span className="exp-menu-compare exp-btn">compare</span> */}
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
