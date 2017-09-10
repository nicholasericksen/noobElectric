import React, { Component, PropTypes } from 'react';

import { Route, Switch } from 'react-router-dom';

import Experiment from './Experiment';
import ExperimentsMenu from './ExperimentsMenu';

export default class Experiments extends Component {
    render() {
        return (
            <div className="exp">
                <Switch>
                    <Route exact path="/experiments" component={ExperimentsMenu} />
                    <Route path='/experiments/:experiment' component={Experiment} />
                </Switch>
            </div>
        );
    }
}
