import React from 'react';
import Dashboard from './Dashboard/Dashboard';
import Form from './Form';
import GeneralError from './Error'

import { Router, Route, Link, browserHistory } from 'react-router';

export default class App extends React.Component {
    render() {
        return (
            <Router history={browserHistory}>
                <Route path="/" component={Dashboard} />
                <Route path="*" component={GeneralError} />
            </Router>
        );
    }
}
