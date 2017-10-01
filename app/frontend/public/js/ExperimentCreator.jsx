import React, { Component, Proptypes } from 'react';

export default class ExperimentCreator extends Component {
    constructor(props) {
        super(props);

        this.state = {
            title: '',
            summary: '',
            description: '',
            image: '--',
            experiments: ['--']
        };

        this.handleTitleChange = this.handleTitleChange.bind(this);
        this.handleSummaryChange = this.handleSummaryChange.bind(this);
        this.handleDescriptionChange = this.handleDescriptionChange.bind(this);
        this.createExperiment = this.createExperiment.bind(this);
        this.handleImageChange = this.handleImageChange.bind(this);
    }

    componentDidMount() {
        var xhr = new XMLHttpRequest();

        xhr.open('GET', 'http://localhost:5000/api/data', true);

        xhr.onload = () => {
            if(xhr.status >= 200 && xhr.status < 400) {
                var tmpArr = this.state.experiments;
                var rawdata = JSON.parse(xhr.responseText).data;
                var data = tmpArr.concat(rawdata);
                this.setState({
                    experiments: data
                });
            } else {
                console.log("An error was returned")
            }
        }

        xhr.onerror = function(err) {
            console.log("error: ", err);
        }

        xhr.send();
    }


    createExperiment() {
        console.log('actual', this.state.image);

        var request = new XMLHttpRequest();
        var params = {
            title: this.state.title,
            summary: this.state.summary,
            description: this.state.description,
            images: this.state.image
        };

        request.open('POST', 'http://localhost:5000/api/experiments/new', true);



        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            // var rawdata = JSON.parse(request.responseText);
            // var data = rawdata.exp;
        // console.log("this.state.data", this.state.data);
            console.log("success", JSON.parse(request.responseText));
            // this.setState({directoryImages: JSON.parse(request.responseText)})
          } else {
            // We reached our target server, but it returned an error
          }
        };
        request.onerror = function() {
          // There was a connection error of some sort
        };

        request.send(JSON.stringify(params));
    }

    handleTitleChange(event) {
        this.setState({title: event.target.value})
    }

    handleSummaryChange(event) {
        this.setState({summary: event.target.value})
    }

    handleDescriptionChange(event) {
        this.setState({description: event.target.value})
    }

    handleImageChange(event) {
        this.setState({
            image: event.target.value
        });
    }

    render() {
        return(
            <div>
                <form>
                    <h3>Title</h3>
                    <input value={this.state.title} onChange={this.handleTitleChange} className="form-control" />
                    <hr />
                    <h3>Summary</h3>
                    <textarea value={this.state.summary} onChange={this.handleSummaryChange} className="form-control"></textarea>
                    <hr />
                    <h3>Description</h3>
                    <textarea value={this.state.description} onChange={this.handleDescriptionChange} className="form-control"></textarea>
                    <hr />
                    <h3>Images</h3>
                    <span>
                        <select className="form-control" value={this.state.image} onChange={this.handleImageChange}>
                            {this.state.experiments.map((experiment, index) => {
                                return (
                                    <option key={index} value={experiment}>{experiment}</option>
                                );
                            })}
                        </select>
                    </span>
                </form>
                <div className="btn btn-primary" onClick={() => this.createExperiment()}>Create</div>
            </div>
        )
    }
}
