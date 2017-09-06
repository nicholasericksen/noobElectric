import React from 'react';

import { Link } from 'react-router';

export default class Error extends React.Component {
    render() {
        return (
            <div>
                <div>Something went wrong, there was an Error!</div>
                <Link to={'/'}>Back</Link>
            </div>
        )
    }
}