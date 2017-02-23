import React from 'react';

import { Link } from 'react-router';

import '../css/style.less';

export default class Form extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            date: new Date(),
            file: null,
            sensorValue: null
        };

        this.submitFile = this.submitFile.bind(this);
        this.fileUpload = this.fileUpload.bind(this);
        this.getSensorReading = this.getSensorReading.bind(this);
        this.moveWheel = this.moveWheel.bind(this);
    }

    componentDidMount() {
        this.timerID = setInterval(
            () => this.tick(),
            1000
        );
        // var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
        // socket.on('connect', function() {
        //     socket.emit('sensor reading', {data: 'I\'m connected!'});
        // });
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

    getSensorReading() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = () => {
        if (xhr.readyState == XMLHttpRequest.DONE) {
                // alert(xhr.responseText);
                this.setState({sensorValue: xhr.responseText});
            }
        }

        xhr.open('GET', 'http://localhost:5000/lightsensor', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        xhr.send(null);
    }

    moveWheel(dir) {
        var xhr = new XMLHttpRequest();
        console.log("moving");

        xhr.open('POST', 'http://localhost:5000/motor', true);
        xhr.setRequestHeader('Content-Type', 'application/json charset=UTF-8');
        xhr.send(JSON.stringify({dir: dir}));
    }

    render() {
        return (
            <div>
                <div className='header-container'>
                    <h1 className='header'>Optics Dashboard</h1>
                    <span className='date-time'>Date: {this.state.date.toLocaleTimeString()}</span>
                </div>

                <div className='container'>
                    <h3>Image Processing</h3>
                    <form method='post' encType='multipart/form-data' action='http://localhost:5000/upload'>
                        <input type='file' name='file' ref='file' onChange={this.fileUpload}></input>
                        <input type='submit' value='Upload' onClick={this.submitFile}></input>
                    </form>
                </div>

                <div className='container'>
                    <h3>Polarimeter</h3>
                    <input className='btn sensor-btn' type='submit' value='Read' onClick={() => this.getSensorReading()}></input>
                    <div className='sensor-value' >Sensor Value: {this.state.sensorValue}</div>
                </div>

                <div className='container'>
                    <h3>Wheel Movement</h3>
                    <div className='btn left-btn' onClick={() => this.moveWheel('left')}>left</div>
                    <div className='btn right-btn' onClick={() => this.moveWheel('right')}>right</div>
                </div>


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
