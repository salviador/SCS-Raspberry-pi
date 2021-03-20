import react from 'react';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';
import Test from '../Test/Test';
import { useHistory } from "react-router-dom";

import "./../App.css";




function Homepage() {
    let history = useHistory();

    const handleClickConfigurazioni = () => {

        history.push("configurazione.html");

    };
    const handleClickTest = () => {
        history.push("test.html");
    };
    const handleClickNodeRed = () => {
        history.push("noderedHome.html");
    };

    

    return (
        <>
            <Container className="justify-content-md-center" style={{}}>
                <div className="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
                    <h1 className="display-4">SCS-bus Raspberry shield</h1>
                    <p className="lead">Benvenuti nella pagina di configurazione dei dispositivi del Bus SCS e Test</p>
                </div>


                <div className="card-deck text-center" >
                    <div className="card mb-4 shadow-sm">
                        <div className="card-header">
                            <h4 className="my-0 font-weight-normal">Configurazione</h4>
                        </div>
                        <div className="card-body">
                            <h1 className="card-title "> <small className="text-muted"> </small></h1>
                            <ul className="list-unstyled mt-3 mb-4">
                                <li>Attuatori on/off</li>
                                <li>Dimmer</li>
                                <li>Serrande/Tapparelle</li>
                                <li>Gruppi</li>
                                <li>Sensori Temperatura</li>
                                <li>Termostati</li>
                                <li>Serrature</li>
                                <li>Campanello porta</li>
                            </ul>
                            <button type="button" className="btn btn-lg btn-block btn-primary" onClick={handleClickConfigurazioni} >Entra</button>
                        </div>
                    </div>

                    <div className="card mb-4 shadow-sm">
                        <div className="card-header">
                            <h4 className="my-0 font-weight-normal">Test</h4>
                        </div>
                        <div className="card-body">
                            <h1 className="card-title pricing-card-title"> <small className="text-muted"> </small></h1>
                            <ul className="list-unstyled mt-3 mb-4">
                                <li>Attuatori on/off</li>
                                <li>Dimmer</li>
                                <li>Serrande/Tapparelle</li>
                                <li>Gruppi</li>
                                <li>Sensori Temperatura</li>
                                <li>Termostati</li>
                                <li>Serrature</li>
                                <li>Campanello porta</li>
                            </ul>
                            <button type="button" className="btn btn-lg btn-block btn-primary idTest" onClick={handleClickTest} >Entra</button>
                        </div>
                    </div>

                    <div class="card mb-4 box-shadow">
                        <div class="card-header">
                        <h4 className="my-0 font-weight-normal">Node-RED</h4>
                        </div>
                        <div class="card-body d-flex flex-column">
                            <ul className="list-unstyled mt-3 mb-4">
                                <li>AWS IoTs</li>
                                <li>Alexa virtual-smart-home</li>
                            </ul>
                            <button type="button" class="btn btn-lg btn-block btn-primary mt-auto" style={{marginBottom:'1em'}} onClick={handleClickNodeRed}>Entra</button>
                        </div>
                    </div>


                </div>



            </Container>
        </>
    );










}



export default Homepage;