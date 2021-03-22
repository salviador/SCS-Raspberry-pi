import { useState, useEffect, useRef } from 'react';
import { Container, Navbar, Form, Button, Control, Row, Col, Modal } from 'react-bootstrap';

import "./../App.css";


//const ADDRESS_SERVER = "http://192.168.1.118/";
const ADDRESS_SERVER = "/";


function NoderedHome() {

    return (
        <>
            <Container className="justify-content-md-center" style={{}}>
                <div className="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
                    <h1 className="display-4">Node-Red configurazione con Alexa</h1>
                </div>


                <div className="card-deck text-center" >
                    <div className="card mb-4 shadow-sm" style={{ border: "1px solid black" }}>
                        <div className="card-header">
                            <h4 className="my-0 font-weight-normal">NodeRed AWS</h4>
                        </div>
                        <div>
                            <p><i><small>Configurare prima AWS Server: <a href="http://scsshields.altervista.org/AWS_Skill_Bticino.html" target="_blank">Guida</a></small></i></p>
                        </div>
                        <div className="card-body">
                            <ul className="list-unstyled mt-3 mb-4">
                                <li>                                    
                                    <a href="/NoderedAlexaAWS.html"><Button variant="outline-primary"  >Entra</Button></a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>





                <div className="card-deck text-center"  >
                    <div className="card mb-4 shadow-sm" style={{ border: "1px solid black" }}>
                        <div className="card-header">
                            <h4 className="my-0 font-weight-normal">NodeRed "virtual-smart-home" library</h4>
                        </div>
                        <div className="card-body">
                            <ul className="list-unstyled mt-3 mb-4">
                                <li>
                                    <a href="/noderedAlexa.html"><Button variant="outline-primary"  >Entra</Button></a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>








            </Container>

        </>
    );
}



export default NoderedHome;