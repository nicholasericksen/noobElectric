import React from 'react';

import { Link } from 'react-router';

import './styles.less';

export default class Dashboard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            experiments: []
        }

        this.listExperiments = this.listExperiments.bind(this);
    }

    componentDidMount() {

    }

    componentWillUnmount() {

    }

    listExperiments() {
        var xhr = new XMLHttpRequest();

        xhr.open('GET', 'http://localhost:5000/upload', true);
        xhr.setRequestHeader('Content-Type', 'application/json charset=UTF-8');
        xhr.send(null);

        xhr.onreadystatechange = () => {
            if(xhr.readyState == XMLHttpRequest.DONE) {
                var data = JSON.parse(xhr.responseText);

                this.setState({
                    experiments: data.exp
                });
            }
        }
    }

    render() {
        return (
            <div className="noobee-dashboard">
                <h1 className="dashboard-header">noobEE Dashboard</h1>
                <div className="main-menu">
                    <div className="data-acquisition menu-btn">Acquisition</div>
                    <div className="data-processing menu-btn">Processing</div>
                    <div
                        className="experiments menu-btn"
                        onClick={() => this.listExperiments()}
                    >
                        Experiments
                    </div>
                </div>
                <div className="workspace">
                    <div className="exp-list">
                        {this.state.experiments}
                    </div>

                </div>
            </div>
        );
    }
}


Dashboard.propTypes = {

}

Dashboard.defaultProps = {

}
