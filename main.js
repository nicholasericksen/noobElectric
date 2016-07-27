import React from 'react';
import Router from 'react-router';
import { DefaultRoute, Link, Route, RouteHandler } from 'react-router';
require('./main.css');


let Main = React.createClass({
    render() {
      return(
        <div id='content'>
          <p>The Universe is a playground for electromagnetic forces.  It is one of four fundamental forces in the universe, and plays a role in
          in life everywhere.  You cannot escape the force. Embrace it. Learn to live with it.  Here is only the beginning.
          </p>
          <div id="fundamental">
            <h3>Fundamentals</h3>
            <p>Voltage, Current, Resistance.  These three ideas will provide the cornerstone
            for everything to come in the future.  They are not indeoendant of eachother, nor are
            they manmade.  Nature has divised a plan, one where everything works in perfect harmony.</p>
          </div>

          <div id="ohm">
            <h3>Ohms Law - </h3>
            <Link to="login">Take the Quiz</Link>
            <p>The relationship between voltage, current and resistance is known as Ohms Law.
            Nothing is more essential to understanding the electrical world.</p>
            <img src='./Ohms-Law.png' height='50px' width='75px' />
          </div>

          <div id="z">
            <h3>Impedance - </h3>
            <Link to="quiz2">Take the Quiz</Link>
            <p>Resistance is one type of impedance.  It forms a holy trinity with capacitance and
            inductance.  The componets of classical elctrical systems which are often coined RLC circuits.</p>
            <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Complex_Impedance.svg/200px-Complex_Impedance.svg.png' height='150px' width='150px' />
          </div>

          <div id="power">
          <h3>Power - </h3>
          <Link to="quiz3">Take the Quiz</Link>
          <p>This is what you get when you multiply voltage by current.  It is the rate at which
          electrical energy is transferred in an electrical circuit.  Electric generatoration and distribution companies charge for energy
          used per month, which is the power consumed per unit time.</p>
          <img src='Power.png' height='50px' width='75px' />
          </div>

        </div>
      );

    }
});

export default Main;
