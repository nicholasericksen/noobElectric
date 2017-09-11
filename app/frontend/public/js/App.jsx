import React, { Component, PropTypes } from 'react';

import Experiments from './Experiments';
import Menu from './Menu';
import Home from './Home';
import Header from './Header';

import Webcam from './Webcam';

import { Route, Link, Switch } from 'react-router-dom'

import '../style.less';

export default class App extends Component {
    render() {
        return (
            <div className="noobelectric">
                <Header/>
                <Switch>
                    <Route exact path='/index.html' component={Home} />
                    <Route path='/experiments' component={Experiments} />
                    <Route path='/daq' component={Webcam} />
                    <Route path='/documentation' component={Experiments} />
                    <Route path='/about' component={Experiments} />
                </Switch>
            </div>
        );
    }
}
