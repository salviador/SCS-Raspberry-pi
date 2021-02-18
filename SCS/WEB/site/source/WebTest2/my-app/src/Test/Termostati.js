import { useState, useEffect } from 'react';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';

import "./../App.css";



function Termostati({ device, valuedataRT, clientMWTT }) {
    const [statosensore, setstatosensore] = useState("--.-°");
    const [temp_termostato, settemp_termostato] = useState("--.-°");
    const [modalita_termostato, setmodalita_termostato] = useState("----");
 //   const [temp_setting_termostato, set_temp_setting_termostato] = useState(10);


    useEffect(() => {
        if (device.nome_attuatore === valuedataRT.nome_attuatore) {

            var m = (valuedataRT.topic).split("/");
            if (m[4] != null) {
                if (m[4].localeCompare("status") == 0) {
                    setstatosensore(valuedataRT.stato + "°");
                } else if (m[4].localeCompare("temperatura_termostato_impostata") == 0) {
                    settemp_termostato(valuedataRT.stato);
                   // set_temp_setting_termostato(valuedataRT.stato);
                } else if (m[4].localeCompare("modalita_termostato_impostata") == 0) {
                    setmodalita_termostato(valuedataRT.stato);
                }
            }
        }
    }, [valuedataRT]);


    const settemp_setting_termostato = (event) => {
        settemp_termostato(event.target.value);
    };

    const send_settemp_setting_termostato = (event) => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic = "/scsshield/device/" + device.nome_attuatore + "/set_temp_termostato";
                clientMWTT.publish(topic, event.target.value)
            }
        }
    };
    

    const estate_button = () => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic = "/scsshield/device/" + device.nome_attuatore + "/set_modalita_termostato";
                clientMWTT.publish(topic, 'estate')
            }
        }
    };
    const off_button = () => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic = "/scsshield/device/" + device.nome_attuatore + "/set_modalita_termostato";
                clientMWTT.publish(topic, 'off')
            }
        }
    };
    const inverno_button = () => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic = "/scsshield/device/" + device.nome_attuatore + "/set_modalita_termostato";
                clientMWTT.publish(topic, 'inverno')
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
                                <Col lg={2}>
                                    <Row >
                                        <Col lg={8}><i>Temp-Ambiente</i></Col>
                                        <Col lg={8}><b>{statosensore}</b></Col>
                                    </Row>
                                </Col>
                                <Col lg={2}>
                                    <Row>
                                        <Col lg={8}><i>Temp-Termostato</i></Col>
                                        <Col lg={8}><b>{temp_termostato}</b></Col>
                                    </Row>
                                </Col>
                                <Col lg={2} style={{ alignSelf: "center" }}>
                                    <Row >
                                        <Col lg={8}><i>Modalita</i></Col>
                                        <Col lg={8}><b>{modalita_termostato}</b></Col>
                                    </Row>
                                </Col>
                                <Col lg={2}>
                                    <Row >
                                        <Col lg={6}><i>Set Temp</i></Col>
                                        <Col lg={8}>
                                            <div className="col-xs-1">
                                                <input className="form-control" style={{ width: "90%" }} type="number" name="SetTemp" step="0.5" value={temp_termostato} onChange={settemp_setting_termostato} onBlur={send_settemp_setting_termostato} />
                                            </div>
                                        </Col>
                                    </Row>
                                </Col>
                                <Col style={{ alignSelf: "center" }}>
                                    <div style={{ textAlign: "center", alignItems: "right" }}>
                                        <Button style={{ marginRight: "8px" }} size="md" variant="outline-primary" onClick={estate_button}>CALDO</Button>
                                        <Button style={{ marginRight: "8px" }} size="md" variant="outline-primary" onClick={off_button}>OFF</Button>
                                        <Button size="md" variant="outline-primary" onClick={inverno_button}>FREDDO</Button>
                                    </div>
                                </Col>
                            </Row>
                        </Container>
                    </Card.Body>
                    <Card.Footer className="text-muted" style={{ textAlign: "center" }}>
                        <p style={{ fontSize: "9px", margin: 0, padding: "0%" }}>-Tipo-</p>
                        <p style={{ fontSize: "15px", margin: 0, padding: "0%" }}>TERMOSTATO</p>
                    </Card.Footer>
                </Card>
            </Container>

        </>
    );
}


export default Termostati;