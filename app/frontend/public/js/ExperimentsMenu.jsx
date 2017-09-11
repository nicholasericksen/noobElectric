import React, { Component } from 'react';

import { Link } from 'react-router-dom';

export default class ExperimentsMenu extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null
        }

        this.requestData = this.requestData.bind(this);
    }

    componentWillMount() {
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
    render() {
        return (
            <div>
                {this.state.data ?
                    this.state.data.map((experiment, index) => {
                        return(
                            <div className="exp-menu-item-container">
                                <h3 className="" key={index}>
                                    {experiment.title}
                                </h3>
                                <div className="exp-description">
                                    {experiment.summary}
                                </div>
                                <div className="exp-buttons">
                                    <Link className="button" key={index} to={`/experiments/${experiment._id.$oid}`}>more</Link>
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
