import React from 'react';

import { Link } from 'react-router';

export default class Form extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            date: new Date(),
            file: null
        };

        this.submitFile = this.submitFile.bind(this);
        this.fileUpload = this.fileUpload.bind(this);
    }

    componentDidMount() {
        this.timerID = setInterval(
            () => this.tick(),
            1000
        );
    }

    componentWillUnmount() {
        clearInterval(this.timerID);
    }

    tick() {
        this.setState({
            date: new Date()
        });
    }

    submitFile(e) {
        console.log(this.state.file);

        var request = new XMLHttpRequest();
        request.open('POST', 'http://localhost:5000/upload', true);
        request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        request.send(this.state.file);
    }

    fileUpload() {
        //TODO: this throws a warning and should be fixed
        this.setState({file: this.refs.file.getDOMNode().files[0]});
    }

    render() {
        return (
            <div>
                <h1>Hello, {this.props.name}</h1>
                <h2>Date: {this.state.date.toLocaleTimeString()}</h2>

                <form method='post' encType='multipart/form-data'>
                    <input type='file' name='file' ref='file' onChange={this.fileUpload}></input>
                    <input type='submit' value='Upload' onClick={this.submitFile}></input>
                </form>
                hey
                <Link to={'error'}>hey hey hey hye </Link>
            </div>
        );
    }
}


Form.propTypes = {
    name: React.PropTypes.string
}

Form.defaultProps = {
    name: 'Nicholas'
}
