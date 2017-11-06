import React, { Component } from 'react';

export default class ExperimentIntro extends Component {
    constructor(props) {
        super(props);

        this.state = {
            tags: ['polarizance', 'diattenuation', 'red-oak', 'american-ash', 'sugar-maple', 'red', 'broadband', '0wk', '1wk', 'specular', 'diffuse'],
            activeTags: []
        }

        this.handleTagClick = this.handleTagClick.bind(this);
        this.handleTagSave = this.handleTagSave.bind(this);
        this.handleTagCancel = this.handleTagCancel.bind(this);
    }
    handleTagClick(tag) {
        const activeTags = this.state.activeTags;
        const tags = this.state.tags;
        const tagIndexToRemove = tags.indexOf(tag);
        const activeTagIndexToRemove = activeTags.indexOf(tag);

        if (tagIndexToRemove > -1){
            tags.splice(tagIndexToRemove, 1);
            // console.log("newTags", newTags);
            activeTags.push(tag);

            this.setState({
                tags: tags,
                activeTags: activeTags
            });
        }
        else if (activeTagIndexToRemove > -1) {
            activeTags.splice(activeTagIndexToRemove, 1);
            // console.log("newTags", newTags);
            tags.push(tag);

            this.setState({
                tags: tags,
                activeTags: activeTags
            });
        }

    }
    handleTagSave() {
        // var expId = `${this.props.match.params.experiment}`;
        let params =  {
            id: this.props.id,
            tags: this.state.activeTags
        };
        console.log('params', JSON.stringify(params));

        const request = new XMLHttpRequest();

        request.open('POST', 'http://localhost:5000/api/experiments/tags', true);

        request.onload = () => {
          if (request.status >= 200 && request.status < 400) {
            var rawdata = JSON.parse(request.responseText);
            var data = rawdata.exp;
            var dataset = [];

            console.log("data", data);
                // this.setState({data: data});

          } else {
            // We reached our target server, but it returned an error
          }
        };
        request.onerror = function() {
          // There was a connection error of some sort
        };
        request.send(JSON.stringify(params));
    }

    handleTagCancel() {
        var expId = `${this.props.match.params.experiment}`;
        let params =  {
            id: expId,
        };


    }

    render() {

        const { activeTags } = this.state;
        console.log(typeof activeTags !== 'undefined' && activeTags.length > 0);
        console.log("tabfdgb", activeTags);

        return(
            <div className="exp-introduction">
                <p>
                    {this.props.summary}
                </p>
                <p>
                    {this.props.description}
                </p>
                <div className="tags-container">
                    <span onClick={this.handleTagSave}>save</span>
                    <span onClick={this.handleTagCancel}>cancel</span>
                    <div className="activeTags">
                        {typeof activeTags !== 'undefined' && activeTags.length > 0 ? activeTags.map((tag, index) => (
                            <span className="tag btn button" onClick={() => this.handleTagClick(tag)}>{tag}</span>
                        )): null}
                    </div>
                    <div className="tags">
                        {this.state.tags ? this.state.tags.map((tag, index) => (
                            <span className="tag btn button" onClick={() => this.handleTagClick(tag)}>{tag}</span>
                        )): null}
                    </div>
                </div>
            </div>
        )
    }
}
