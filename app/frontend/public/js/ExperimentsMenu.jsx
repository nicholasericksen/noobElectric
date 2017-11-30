import React, { Component } from 'react';

import classNames from 'classnames';

import { Link } from 'react-router-dom';

export default class ExperimentsMenu extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: [],
            compareList: []
        }

        this.requestData = this.requestData.bind(this);
        this.exportGlcmData = this.exportGlcmData.bind(this);
        this.exportBGRHistograms = this.exportBGRHistograms.bind(this);
    }

    componentDidMount() {
        this.requestData();
    }

    requestData() {
        var request = new XMLHttpRequest();
        request.open('GET', 'http://localhost:5000/api', true);

        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            const rawdata = JSON.parse(request.responseText);
            const data = rawdata.exp;

            this.setState({
                data: data
            });
        // console.log("this.state.data", this.state.data);
          } else {
            // We reached our target server, but it returned an error
          }

        };
        request.onerror = function() {
          // There was a connection error of some sort
        };

        request.send();
    }
    addCompare(experiment) {
        const id = experiment._id.$oid;
        const list = this.state.compareList;
        const exportList = this.state.exportList;

        if (list.includes(id)) {
            const i = list.indexOf(id);
            list.splice(i, 1);
        } else {
            list.push(id);
        }
        this.setState({
            compareList: list
        });
    }
    exportBGRHistograms() {
        const idArray = this.state.compareList;


        var csvContent = "data:text/csv;charset=utf-8,";
        csvContent += 'RWC,S1bmean,S1bstd,S1gmean,S1gstd,S1rmean,S1rstd,S2bmean,S2bstd,S2gmean,S2gstd,S2rmean,S2rstd' + "\n";
        var successCounter = 0;
        idArray.map((id, index) => {
            // var request = new XMLHttpRequest();

            let params =  {
                id: id
            };
            fetch('http://localhost:5000/api/experiments/histograms/bgr', {method: 'POST', body: JSON.stringify(params)})
            .then((response) => {
                return response.json();
            })
            .then((rawdata) => {
                var data = rawdata.exp;
                var bgr = data.histograms;
                if(bgr) {
                    // glcm.map((sample, index) => {

                    // const all = [successCounter, bgr.S1.b.stats.mean, bgr.S1.b.stats.std, bgr.S1.g.stats.mean, bgr.S1.g.stats.std,bgr.S1.r.stats.mean, bgr.S1.r.stats.std, bgr.S2.b.stats.mean, bgr.S2.b.stats.std, bgr.S2.g.stats.mean, bgr.S2.g.stats.std,bgr.S2.r.stats.mean, bgr.S2.r.stats.std];
                    // console.log("ALL", all);
                    const all = [successCounter, [bgr.S1.b.data], [bgr.S1.g.data], [bgr.S1.r.data]];
                    console.log("ALL", all);
                    var dataString = all.join(",");
                    csvContent += dataString+ "\n";
                    successCounter += 1;
                    // })
                    //  console.log("index", successCounter);
                    if (successCounter === idArray.length) {

                        console.log('length', idArray.length);
                        console.log("sail away", csvContent);
                        var encodedUri = encodeURI(csvContent);
                        window.open(encodedUri);
                    }
                }


            })

        });
    }
    exportGlcmData() {
        // var ids = `${this.props.match.params.ids}`;
        const idArray = this.state.compareList;


        var csvContent = "data:text/csv;charset=utf-8,";
        csvContent += 'Type,Color,Age,Direction,S1mean,S1std,S2mean,S2std,Corr,Diss,Contrast,Energy,ASM' + "\n";


        idArray.map((id, index) => {
            // var request = new XMLHttpRequest();

            let params =  {
                id: id
            };
            fetch('http://localhost:5000/api/experiments/glcm', {method: 'POST', body: JSON.stringify(params)})
            .then((response) => {
                return response.json();
            })
            .then((rawdata) => {
                var data = rawdata.exp;
                console.log("DASDF", data);
                var glcm = data.glcm;
                console.log("GLCM", glcm);
                if(glcm) {
                    glcm.map((sample, index) => {
                        const S1 = sample.stokes.S1.stats;
                        const S2 = sample.stokes.S2.stats;

                        const S1mean = S1.mean;
                        const S1std = S1.std;
                        const S2mean = S2.mean;
                        const S2std = S2.std;
                        const corr = sample.data.correlation;
                        const diss = sample.data.dissimilarity;
                        const contrast = sample.data.contrast;
                        const energy = sample.data.energy;
                        const asm = sample.data.asm;

                        const file = sample.stokes.filename.split('/');
                        const info = file[0].split('-')
                        // console.log("INFo", info);
                        const color = info[3];
                        const direction = info[4];

                        const age = info[5] ? info[5] : '0wk';
                        const type = info[0] + '-' + info[1];

                        const all = [type, color, age, direction, S1mean, S1std, S2mean, S2std, corr, diss, contrast, energy, asm];
                        // console.log("ALL", all);

                        var dataString = all.join(",");
                        csvContent += dataString+ "\n";
                    })
                }
                console.log("index", index);
                console.log("idlength", idArray.length);
                if (index === idArray.length - 1) {
                    console.log("sail away", csvContent);
                    var encodedUri = encodeURI(csvContent);
                    window.open(encodedUri);
                }
            })

        //     request.open('POST', 'http://localhost:5000/api/experiments/glcm', true);
        //
        //     request.onload = () => {
        //       if (request.status >= 200 && request.status < 400) {
        //         var rawdata = JSON.parse(request.responseText);
        //         var data = rawdata.exp;
        //         console.log("DASDF", data);
        //         var glcm = data.glcm;
        //         if(glcm) {
        //             glcm.map((sample, index) => {
        //                 const S1 = sample.stokes.S1.stats;
        //                 const S2 = sample.stokes.S2.stats;
        //
        //                 const S1mean = S1.mean;
        //                 const S1std = S1.std;
        //                 const S2mean = S2.mean;
        //                 const S2std = S2.std;
        //                 const corr = sample.data.correlation;
        //                 const diss = sample.data.dissimilarity;
        //                 const contrast = sample.data.contrast;
        //                 const energy = sample.data.energy;
        //                 const asm = sample.data.asm;
        //
        //                 const file = sample.stokes.filename.split('/');
        //                 const info = file[0].split('-')
        //
        //                 const color = info[3];
        //                 const direction = info[4];
        //
        //                 const age = info[5] ? info[5] : '0wk';
        //                 const type = info[0] + '-' + info[1];
        //
        //                 const all = [type, color, age, direction, S1mean, S1std, S2mean, S2std, corr, diss, contrast, energy, asm];
        //                 // console.log("ALL", all);
        //
        //                 var dataString = all.join(",");
        //                 csvContent += dataString+ "\n";
        //             })
        //         }
        //
        //
        //         console.log('experiments', glcm);
        //
        //
        //
        //       } else {
        //         // We reached our target server, but it returned an error
        //       }
        // // console.log("CSV", csvContent);
        //
        //     };
        //     request.onerror = function() {
        //       // There was a connection error of some sort
        //     };
        //     request.send(JSON.stringify(params));
        });
        // this.setState({compareList: []});
        //

    }

    render() {
        const data = this.state.data ? this.state.data : [];
        const inactive = this.state.compareList.length === 0 ? true : false;

        return (
            <div>
                <Link className="subheading btn-primary btn" to={'/experiments/new'}>
                    { /*<div className="experiment-button">
                        <span className="glyphicon glyphicon-plus" aria-hidden="true"></span>
                    </div> */}
                    new
                </Link>
                <Link className={classNames({'inactive': inactive}, "subheading","btn-primary","btn")} to={`/experiments/compare/${this.state.compareList}`}>compare</Link>
                <span onClick={this.exportBGRHistograms} className={classNames({'inactive': inactive}, "subheading","btn-primary","btn")}>export</span>
                {data ?
                    data.map((experiment, index) => {
                        const active = this.state.compareList.includes(experiment._id.$oid);

                        return(
                            <div key={index} className="exp-menu-item-container">
                                <h3 className="" key={index}>
                                    {experiment.title}
                                </h3>
                                <div className="exp-description">
                                    {experiment.summary}
                                </div>
                                <div className="exp-buttons">
                                    <Link className="button" key={index} to={`/experiments/${experiment._id.$oid}`}>more</Link>
                                    <span key={experiment._id.$oid} onClick={() => this.addCompare(experiment)} className={classNames({'active': active}, "compare", "button")}>select</span>
                                    {/*<span className="exp-menu-compare exp-btn">compare</span> */}
                                </div>
                                <hr />
                            </div>
                        )
                    })
                : null
                }
            </div>
        )
    }
}
