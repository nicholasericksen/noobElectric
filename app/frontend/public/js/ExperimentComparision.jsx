import React, { Component } from 'react';

import Histogram from './Histogram';

export default class ExperimentComparision extends Component {
    constructor(props) {
        super(props);

        this.state = {
            experiments : []
        }
    }

    componentDidMount() {
        var ids = `${this.props.match.params.ids}`;
        const idArray = ids.split(',');




        idArray.map((id, index) => {
            var request = new XMLHttpRequest();

            let params =  {
                id: id
            };

            request.open('POST', 'http://localhost:5000/api/experiments', true);

            request.onload = () => {
              if (request.status >= 200 && request.status < 400) {
                var rawdata = JSON.parse(request.responseText);
                var data = rawdata.exp;
                const experiments = this.state.experiments;
                experiments.push(data);

                this.setState({
                    experiments: experiments
                });
              } else {
                // We reached our target server, but it returned an error
              }
            };
            request.onerror = function() {
              // There was a connection error of some sort
            };
            request.send(JSON.stringify(params));
        });
    }
    render() {
        let S1 = [];
        let S2 = [];
        console.log("PIG", this.state.experiments);

        let stokes = this.state.experiments.length > 0 ? this.state.experiments.map((experiment, index) => {
            let experimentS1 = {data: experiment.histograms.stokes.S1.data, title: experiment.title};
            let experimentS2 = {data: experiment.histograms.stokes.S2.data, title: experiment.title};

            S1.push(experimentS1);
            S2.push(experimentS2);
        }) : null;

        return(
            <div>

                {this.state.experiments.length > 0  ?
                    <div>
                        <h4>S1 Parameter</h4>
                        <Histogram
                            data={S1}
                            targetElement={'exp-stokes-S1-histograms'}
                            width={600}
                            height={300}
                            yTicks={10}
                        />
                    <h4>S2 Parameter</h4>
                        <Histogram
                            data={S2}
                            targetElement={'exp-stokes-S2-histograms'}
                            width={600}
                            height={300}
                            yTicks={10}
                        />
                    </div>
                 : null}
            </div>
        )
    }
}
