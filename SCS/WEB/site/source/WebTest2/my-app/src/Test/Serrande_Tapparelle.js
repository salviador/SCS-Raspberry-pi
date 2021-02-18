import { useState, useEffect } from 'react';
import RangeSlider from 'react-bootstrap-range-slider';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';

import "./../App.css";



function Serrande_Tapparelle({ device, valuedataRT, clientMWTT }) {

    const [percentualeTapparelle, set_percentualeTapparelle] = useState(50);

    useEffect(() => {
        if (device.nome_attuatore === valuedataRT.nome_attuatore) {
            set_percentualeTapparelle(valuedataRT.stato);
        }
    }, [valuedataRT]);


    const update_percentuale = (event) => {
        set_percentualeTapparelle(event.target.value);
    };
    const update_mqtt_serrande = (event) => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic = "/scsshield/device/" + device.nome_attuatore + "/percentuale";
                clientMWTT.publish(topic, percentualeTapparelle);
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
                            <Row>
                                <Col sm={12}>
                                    <Row >
                                        <Col><i>Stato %</i></Col>
                                        <Col lg={6}>
                                            <RangeSlider tooltip='on' value={percentualeTapparelle} min="0" max="100" step="1"  onChange={update_percentuale} onAfterChange={update_mqtt_serrande} />
                                        </Col>
                                    </Row>
                                </Col>
                            </Row>
                        </Container>
                    </Card.Body>
                    <Card.Footer className="text-muted" style={{ textAlign: "center" }}>
                        <p style={{ fontSize: "9px", margin: 0, padding: "0%" }}>-Tipo-</p>
                        <p style={{ fontSize: "15px", margin: 0, padding: "0%" }}>SERRANDE/TAPPARELLE</p>
                    </Card.Footer>
                </Card>
            </Container>






        </>
    );
}


export default Serrande_Tapparelle;