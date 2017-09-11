import React, { Component } from 'react';

export default class Webcam extends Component {
    constructor(props) {
        super(props);

        this.state = {
            videoSrc: null,
            deviceInfos: null
        };

        this.gotDevices = this.gotDevices.bind(this);
        this.errorCallback = this.errorCallback.bind(this);
        this.selectDevice = this.selectDevice.bind(this);
        this.startWebcam = this.startWebcam.bind(this);
        this.takePicture = this.takePicture.bind(this);
    }

    componentDidMount() {
        navigator.mediaDevices.enumerateDevices()
        .then(this.gotDevices)
        .catch(this.errorCallback);
        this.selectDevice(null);
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

        context.drawImage(video, 0, 0, 620, 520);

        const data = canvas.toDataURL('image/png');
    }

    selectDevice(id) {
        // The id is not being used right now as the browser seems to be ignoring it
        // Ideally we should be able to select wwhich webcam we want prior to starting the stream
        navigator.mediaDevices.getUserMedia({ deviceId: {exact: 'c3ec354d9a5076b46d71b300edaa870b37971619e2ec441943ed0761fe8ffbff'}, audio: false, video: true}).then(this.startWebcam).catch(this.errorCallback);
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
            <div>
                <video ref="webcam" src={this.state.videoSrc} autoPlay="true"></video>
                <div className="button" onClick={() => this.takePicture()}>Take Picture</div>
                <canvas ref="preview" width={620} height={520} />
            </div>
        </div>
        )
    }
}
