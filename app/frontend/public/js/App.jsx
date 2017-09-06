import React, { Component, PropTypes } from 'react';

import Experiments from './Experiments';
import Menu from './Menu';

import '../style.less';

export default class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            activeTab: 0,
            data: null
        }

        this.handleMenuButtonClick = this.handleMenuButtonClick.bind(this);
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
          } else {
            // We reached our target server, but it returned an error
          }
        };

        request.onerror = function() {
          // There was a connection error of some sort
        };

        request.send();
    }

    handleMenuButtonClick(index) {
        this.setState({activeTab: index});
    }

    render() {
        const HOME_MENU = ['Data Acquisition', 'Experimental Results', 'Information', 'About'];
        return (
            <div className="noobelectric">
                <div className="header">
                    <span className="title">noobelectric</span>
                    <span className="glyphicon glyphicon-home home-btn"></span>
                </div>
                <div className="main-content">
                    <p className="quote">
                        "The motion of a pendulum has exerted a fascination for human minds, \
                        since the first savage watched the swaying of the first tree branch.\
                        The smooth sinusoidal motion, back and forth, seems to express some\
                        secret of the universe..."
                    </p>
                    <Menu
                        onClick={this.handleMenuButtonClick}
                        labels={HOME_MENU}
                    />
                </div>
                {
                    this.state.data ?
                    <Experiments
                        data={this.state.data}
                    /> : null
                }
            </div>
        );
    }
}
