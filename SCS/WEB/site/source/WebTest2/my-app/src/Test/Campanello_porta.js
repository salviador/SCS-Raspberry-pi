import { useState, useEffect } from 'react';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';

import "./../App.css";


function Campanello_porta({ device, valuedataRT, clientMWTT }) {
    //Stato
    const [statoONOFF, setstatoONOFF] = useState("bell_off.jpg");

    useEffect(() => {
        if (device.nome_attuatore === valuedataRT.nome_attuatore) {
            if ((valuedataRT.stato.localeCompare("on") == 0) || (valuedataRT.stato.localeCompare("1") == 0)) {
                setstatoONOFF("bell_on.jpg");
            } else {
                setstatoONOFF("bell_off.jpg");
            }
        }
    }, [valuedataRT]);


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
                                    Citofono interno: {device.indirizzo_PL}
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
                                        <Col lg={12}><i>Stato</i></Col>
                                        <Col lg={12}>
                                            <img data-icon="switch" src={"/site/image/" + statoONOFF} style={{ width: "32px" }} />
                                        </Col>
                                    </Row>
                        </Container>
                    </Card.Body>
                    <Card.Footer className="text-muted" style={{ textAlign: "center"  }}>
                        <p style={{ fontSize: "9px", margin: 0, padding: "0%" }}>-Tipo-</p>
                        <p style={{ fontSize: "15px", margin: 0, padding: "0%" }}>CAMPANELLO</p>
                    </Card.Footer>
                </Card>
            </Container>
























        </>
    );
}


export default Campanello_porta;