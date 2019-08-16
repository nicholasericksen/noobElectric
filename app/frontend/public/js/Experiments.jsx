import React, { Component, PropTypes } from 'react';

import { Route, Switch } from 'react-router-dom';

import Experiment from './Experiment';
import ExperimentsMenu from './ExperimentsMenu';
import ExperimentCreator from './ExperimentCreator';
import ExperimentComparison from './ExperimentComparision';

export default class Experiments extends Component {
    render() {
        return (
            <div className="exp">
                <Switch>
                    <Route exact path="/experiments" component={ExperimentsMenu} />
                    <Route path='/experiments/new' component={ExperimentCreator} />
                    <Route path='/experiments/compare/:ids' component={ExperimentComparison} />
                    <Route path='/experiments/:experiment' component={Experiment} />
                </Switch>
            </div>
        );
    }
}
