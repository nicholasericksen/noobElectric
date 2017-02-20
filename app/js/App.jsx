import React from 'react';
import Form from './Form';
import GeneralError from './Error'

import { Router, Route, Link, browserHistory } from 'react-router';

export default class App extends React.Component {
    render() {
        return (
            <Router history={browserHistory}>
                <Route path="/" component={Form} />
                <Route path="*" component={GeneralError} />
            </Router>
        );
    }
}
