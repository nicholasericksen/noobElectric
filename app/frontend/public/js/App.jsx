import React, { Component, PropTypes } from 'react';

import Experiments from './Experiments';
import Menu from './Menu';
import Home from './Home';
import Header from './Header';

import '../style.less';

export default class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            activeIndex: false,
            data: null
        }
        this.handleMenuButtonClick = this.handleMenuButtonClick.bind(this);
        this.renderContent = this.renderContent.bind(this);
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
        this.setState({activeIndex: index});
    }



    renderContent() {
        let content;

        if (this.state.activeIndex === 1) {
            return <Home />;
        } else if (this.state.activeIndex === 0) {
            return (
                <Experiments
                    data={this.state.data}
                />
            );
        } else {
            return <Home />;
        }
    }

    render() {


        return (
            <div className="noobelectric">
                <Header
                    onClick={this.handleMenuButtonClick}
                />
                {this.renderContent()}

            </div>
        );
    }
}
