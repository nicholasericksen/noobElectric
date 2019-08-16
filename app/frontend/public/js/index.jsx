
import React from 'react';
import ReactDOM from 'react-dom';
// import BrowserRouter from 'react-router-dom';

import App from './App';

// ReactDOM.render(
//     <App />, document.getElementById('reactEntry')
// );

// react-dom (what we'll use here)
import { BrowserRouter } from 'react-router-dom'

ReactDOM.render((
  <BrowserRouter>
    <App/>
  </BrowserRouter>
), document.getElementById('reactEntry'))
