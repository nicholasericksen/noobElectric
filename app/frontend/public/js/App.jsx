import React, { Component, PropTypes } from 'react';

import Experiment from './Experiment';
import Menu from './Menu';

import '../style.less';

export default class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            activeTab: 0,
        }

        this.handleMenuButtonClick = this.handleMenuButtonClick.bind(this);
        // this.renderContent = this.renderContent.bind(this);
    }
    handleMenuButtonClick(index) {
        this.setState({activeTab: index});
        console.log("STASTE", this.state.activeTab);
    }

    renderContent() {
        // const TABS = ['Main', 'Experiment'];
        //
        // let content;
        //
        // switch(TABS[this.state.activeTab]) {
        //     case('Main'): {
        //         this.setState({activeTab: 0});
        //         content = <HomeMenu />;
        //     }
        //     case('Experiment'): {
        //         this.setState({activeTab: 1});
        //         content = <Experiment />;
        //     }
        //     default: {
        //         this.setState({activeTab: 0});
        //         content = <HomeMenu />;
        //     }
        // }
        //
        // return content;
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
                <Experiment />
            </div>
        );
    }
}
