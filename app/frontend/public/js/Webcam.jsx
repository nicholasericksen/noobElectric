import React, { Component } from 'react';

import io from 'socket.io-client';


export default class Webcam extends Component {
    constructor(props) {
        super(props);

        this.state = {
            videoSrc: null,
            deviceInfos: null,
            showSaveButtons: false,
            filename: '',
            directory: '',
            data: '',
            directoryImages: null,
            voltage: 0
        };
        this.socket = io(`http://localhost:5000`);

        this.gotDevices = this.gotDevices.bind(this);
        this.errorCallback = this.errorCallback.bind(this);
        this.selectDevice = this.selectDevice.bind(this);
        this.startWebcam = this.startWebcam.bind(this);
        this.takePicture = this.takePicture.bind(this);
        this.savePicture = this.savePicture.bind(this);
        this.clearPicture = this.clearPicture.bind(this);
        this.handleFilenameChange = this.handleFilenameChange.bind(this);
        this.handleDirctoryChange = this.handleDirctoryChange.bind(this);

        this.requestData = this.requestData.bind(this);
        this.setVoltage = this.setVoltage.bind(this);
    }

    componentDidMount() {
        navigator.mediaDevices.enumerateDevices()
        .then(this.gotDevices)
        .catch(this.errorCallback);
        this.selectDevice(null);
        this.requestData();

    //     this.socket.on(`value`, (data) => {
    //             // console.log(data);
    //             console.log("DATATATA", data);
    //             this.setVoltage(data);
    //             // socket.emit(`message`, 'hey');
    //     });
    //
    //
    //
    //     this.interval = setInterval(() => {
    //         console.log("EMIT");
    //     this.socket.emit(`message`, 'hey');
    //
    // }, 2000)
    }
    setVoltage(voltage){

            this.setState({ voltage: voltage });
    }
    componentWillUnmount(){
        this.socket.emit('close');
        clearInterval(this.interval);
        this.socket.destroy();
    }

    requestData(props) {

        // console.log("SoCKERET", socket);


        var request = new XMLHttpRequest();

        request.open('GET', 'http://localhost:5000/lightsensor', true);

        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            var rawdata = JSON.parse(request.responseText);
            var data = rawdata.data;
            // var dataset = [];
            // const S1 = {data: data.histograms.stokes.S1.data, title: data.title};
            // const S2 = {data: data.histograms.stokes.S2.data, title: data.title};
            // dataset.push(S1);

            // dataset.push(S2);

            this.setState({
                voltage: data
            });
            console.log("voltage", this.state.voltage);
          } else {
            // We reached our target server, but it returned an error
          }
        };
        request.onerror = function() {
          // There was a connection error of some sort
        };
        // request.send();
    }

    errorCallback(err) {
        console.log("There was n error accessing the webcam", err);
    }

    gotDevices(deviceInfos) {
        this.setState({
            deviceInfos: deviceInfos
        });
    }

    startWebcam(stream) {
        this.setState({ isLoading: false });
        // const video = this.refs.video;
        const vendorURL = window.URL || window.webkitURL;

        // video.src = vendorURL.createObjectURL(stream);
        // video.play();
        this.setState({
            videoSrc: vendorURL.createObjectURL(stream)
        })
    }

    takePicture() {
        const canvas = this.refs.preview;
        const context = canvas.getContext('2d');

        const video = this.refs.webcam;
        // const photo = document.getElementById('photo');

        context.drawImage(video, 0, 0, 640, 480);

        const data = canvas.toDataURL('image/png');
        this.setState({showSaveButtons: true, data: data});
    }

    selectDevice(id) {
        // The id is not being used right now as the browser seems to be ignoring it
        // Ideally we should be able to select wwhich webcam we want prior to starting the stream
        navigator.mediaDevices.getUserMedia({ deviceId: {exact: 'c3ec354d9a5076b46d71b300edaa870b37971619e2ec441943ed0761fe8ffbff'}, audio: false, video: true}).then(this.startWebcam).catch(this.errorCallback);
    }

    savePicture() {
        console.log(this.state.directory, this.state.filename);

        var request = new XMLHttpRequest();
        var params = {
            directory: this.state.directory,
            filename: this.state.filename,
            data: this.state.data
        };

        request.open('POST', 'http://localhost:5000/api/saveimage', true);



        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            // var rawdata = JSON.parse(request.responseText);
            // var data = rawdata.exp;
        // console.log("this.state.data", this.state.data);
            console.log("success", JSON.parse(request.responseText));
            this.setState({directoryImages: JSON.parse(request.responseText)})
          } else {
            // We reached our target server, but it returned an error
          }
        };
        request.onerror = function() {
          // There was a connection error of some sort
        };

        request.send(JSON.stringify(params));

        this.setState({
            showSaveButtons: !this.state.showSaveButtons,
            filename: ''
        });
        this.clearPicture();
    }

    clearPicture() {
        const canvas = this.refs.preview;
        const context = canvas.getContext('2d');

        context.clearRect(0, 0, canvas.width, canvas.height);

        this.setState({showSaveButtons: !this.state.showSaveButtons});
    }

    handleFilenameChange(event) {
        this.setState({filename: event.target.value});
    }

    handleDirctoryChange(event) {
        this.setState({directory: event.target.value});
    }

    render() {
        return (
            <div>
            {/* this.state.deviceInfos ? this.state.deviceInfos.map((device, index) => {
                if (device.kind === 'videoinput') {
                    return(
                        <div>
                            <div onClick={() => this.selectDevice(device.deviceId)} key={device.deviceId}>{device.label}</div>
                        </div>
                    )
                }
            }) : null */}
            <div className="voltage-container">
                voltage: {this.state.voltage}
            </div>
            <div>
                <div className="webcam-container">
                    <video ref="webcam" src={this.state.videoSrc} autoPlay="true"></video>
                    <canvas className="webcam-capture-preview" ref="preview" width={640} height={480} />
                    <div className="current-directory-images">
                        <div className="directory-heading">
                            <div>Current Directory:
                                <span>{this.state.directoryImages ? this.state.directoryImages.directory : 'none'}</span>
                            </div>
                        </div>
                        {this.state.directoryImages ? this.state.directoryImages.images.map((image, index) => {
                            const imgSrc = 'http://localhost:8090/data/' + this.state.directoryImages.directory + '/' + image;
                            return (
                                <div className="directory-image-container">
                                    <img src={imgSrc} />
                                    <span className="directory-image-name">{image}</span>
                                </div>
                            );
                        }) : null}
                    </div>
                </div>

                <div className="webcam-control-container">
                    {!this.state.showSaveButtons ? <div className="btn btn-primary" onClick={() => this.takePicture()}>Take Picture</div> : null}
                    {this.state.showSaveButtons ?
                        <div>
                            <div className="btn btn-success" onClick={() => this.savePicture()}>Save Picture</div>
                            <span>filename: <input value={this.state.filename} onChange={this.handleFilenameChange} type='text' className="filename input"></input></span>
                            <span>directory: <input value={this.state.directory} onChange={this.handleDirctoryChange} type='text' className="directory input"></input></span>
                            <div className="btn btn-warning" onClick={() => this.clearPicture()}>Clear Picture</div>
                        </div>
                    : null}
                </div>
            </div>
        </div>
        )
    }
}
