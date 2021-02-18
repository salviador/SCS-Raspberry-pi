import { useState, useEffect } from 'react';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';

import "./../App.css";



function Sensori_Temperatura({ device, valuedataRT, clientMWTT }) {
    //Stato
    const [statosensore, setstatosensore] = useState("--.-°");

    useEffect(() => {
        if (device.nome_attuatore === valuedataRT.nome_attuatore) {
            setstatosensore(valuedataRT.stato + "°");
        }
    }, [valuedataRT]);



    const aggiorna_button = () => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic =  "/scsshield/device/" + device.nome_attuatore + "/request";
                clientMWTT.publish(topic, " ")
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
                                        Ambiente: {device.indirizzo_Ambiente}
                                    </Col>
                                </Row>
                                <Row>
                                    <Col style={{ textAlign: 'right', marginRight: "12px" }}>
                                        Punto Luce: {device.indirizzo_PL}
                                </Col>
                                </Row>
                            </Col>
                        </Row>
                    </Card.Header>
                    <Card.Body>
                        <Container fluid>
                            <Row >
                                <Col lg={8} style={{ alignSelf: "center" }}>
                                    <Row >
                                        <Col lg={8}><i>Temp-Ambiente</i></Col>
                                        <Col lg={8}><b>{statosensore}</b></Col>
                                    </Row>
                                </Col>
                                <Col style={{ alignSelf: "center" }}>
                                    <div style={{ textAlign: "center", alignItems: "right" }}>
                                        <Button style={{ marginRight: "8px" }} size="md" variant="outline-primary" onClick={aggiorna_button} >Aggiorna</Button>
                                    </div>
                                </Col>
                            </Row>
                        </Container>
                    </Card.Body>
                    <Card.Footer className="text-muted" style={{ textAlign: "center" }}>
                        <p style={{ fontSize: "9px", margin: 0, padding: "0%" }}>-Tipo-</p>
                        <p style={{ fontSize: "15px", margin: 0, padding: "0%" }}>SENSORE-TEMPERATURA</p>
                    </Card.Footer>
                </Card>
            </Container>










        </>
    );
}

export default Sensori_Temperatura;