import { useState, useEffect } from 'react';
import MYnavBar from './MYnavBar'
import Test from './Test/Test'
import Configurazione from './Configurazione/Configurazione'
import Homepage from './HomePage/Homepage'

import {BrowserRouter, Route, Switch} from "react-router-dom";

import "./App.css";
import noderedAlexa from './NodeRedAlexa/NodeRedAlexa';



function App() {




  return (
    <BrowserRouter>
      <div className="App">
        <MYnavBar />

        <Route exact path="/" component={Homepage}/>
        <Route exact path="/configurazione.html" component={Configurazione}/>
        <Route exact path="/test.html" component={Test}/>
        <Route exact path="/noderedAlexa.html" component={noderedAlexa}/>


      </div>
    </BrowserRouter>

  );
}

export default App;
