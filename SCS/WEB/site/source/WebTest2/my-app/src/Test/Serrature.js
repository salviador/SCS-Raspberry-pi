import { useState, useEffect } from 'react';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';

import "./../App.css";


function Serrature({ device, valuedataRT, clientMWTT }) {

    const sblocca_button = () => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic = "/scsshield/device/" + device.nome_attuatore + "/sblocca";
                clientMWTT.publish(topic, "sblocca")
            }
        }
    };


    return (
        <>
           <Container style={{ paddingTop: "20px" }} >
                <Card style={{ width: '100%', border: "1px solid black" }}>
                    <Card.Header>
                        <Row>
                            <Col style={{ textAlign: 'left' }} className="text-primary">
                                <h5>{device.nome_attuatore}</h5>
                            </Col>
                            <Col style={{ textAlign: 'right', fontSize: "12px" }} >
                                <Row>
                                    <Col style={{ textAlign: 'right', marginRight: "12px" }}>
                                    Posto Esterno: {device.indirizzo_Ambiente}
                                    </Col>
                                </Row>
                                <Row>
                                    <Col style={{ textAlign: 'right', marginRight: "12px" }}>
                                    </Col>
                                </Row>
                            </Col>
                        </Row>
                    </Card.Header>
                    <Card.Body>
                        <Container fluid >
                            <Row>
                                <Col lg={8} >
                                    <Row>
                                        <Col lg={8}><i></i></Col>
                                        <Col lg={8}>
                                        </Col>
                                    </Row>
                                </Col>
                                <Col style={{ alignSelf: "center" }}>
                                    <div style={{ textAlign: "center", alignItems: "right" }}>
                                        <button type="button" className="btn btn-danger btn-md" onClick={sblocca_button}>SBLOCCA</button>
                                    </div>
                                </Col>
                            </Row>
                        </Container>
                    </Card.Body>
                    <Card.Footer className="text-muted" style={{ textAlign: "center"  }}>
                        <p style={{ fontSize: "9px", margin: 0, padding: "0%" }}>-Tipo-</p>
                        <p style={{ fontSize: "15px", margin: 0, padding: "0%" }}>SERRATURE</p>
                    </Card.Footer>
                </Card>
            </Container>
























        </>
    );
}


export default Serrature;