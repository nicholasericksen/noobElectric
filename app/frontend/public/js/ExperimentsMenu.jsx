import React, { Component } from 'react';

import classNames from 'classnames';

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
        if (list.includes(id)) {
            const i = list.indexOf(id);
            list.splice(i, 1);
        } else {
            list.push(id);
        }
        this.setState({
            compareList: list
        });
    }

    render() {
        const data = this.state.data ? this.state.data : [];
        const inactive = this.state.compareList.length === 0 ? true : false;
        console.log("inactive", inactive);

        return (
            <div>
                <Link className="subheading btn-primary btn" to={'/experiments/new'}>
                    { /*<div className="experiment-button">
                        <span className="glyphicon glyphicon-plus" aria-hidden="true"></span>
                    </div> */}
                    new
                </Link>
                <Link className={classNames({'inactive': inactive}, "subheading","btn-primary","btn")} to={`/experiments/compare/${this.state.compareList}`}>compare</Link>
                <span className={classNames({'inactive': inactive}, "subheading","btn-primary","btn")}>export</span>
                {data ?
                    data.map((experiment, index) => {
                        const active = this.state.compareList.includes(experiment._id.$oid);

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
                                    <span key={experiment._id.$oid} onClick={() => this.addCompare(experiment._id.$oid)} className={classNames({'active': active}, "compare", "button")}>select</span>
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
