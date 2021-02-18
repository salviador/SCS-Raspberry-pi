import { useState, useEffect } from 'react';
import RangeSlider from 'react-bootstrap-range-slider';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';

import "./../App.css";



function Dimmer({ device, valuedataRT, clientMWTT }) {

    //Stato
    const [statodimmerONOFF, setstatodimmerONOFF] = useState("lamp_disabilitata.svg");
    const [statodimmerPercent, setstatodimmerPercent] = useState("--%");

    //Comando
    const [percentualeDimmer, set_percentualeDimmer] = useState(50);


    useEffect(() => {
        if (device.nome_attuatore === valuedataRT.nome_attuatore) {
            var m = (valuedataRT.topic).split("/");
            if (m[5] != null) {
                setstatodimmerPercent(valuedataRT.stato + "%");
                set_percentualeDimmer(valuedataRT.stato);
            } else {
                if ((valuedataRT.stato.localeCompare("on") == 0) || (valuedataRT.stato.localeCompare("1") == 0)) {
                    setstatodimmerONOFF("lamp_accesa.svg");
                } else {
                    setstatodimmerONOFF("lamp_spenta.svg");
                }
            }
        }
    }, [valuedataRT]);



    const update_percentuale = (event) => {
        setstatodimmerPercent(valuedataRT.stato + "%");
        set_percentualeDimmer(event.target.value);
    };
    const update_mqtt_dimmer = () => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic = "/scsshield/device/" + device.nome_attuatore + "/dimmer";
                clientMWTT.publish(topic, "on");

                topic = "/scsshield/device/" + device.nome_attuatore + "/dimmer";
                clientMWTT.publish(topic, percentualeDimmer);
            }
        }
    };


    const on_button = () => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic = "/scsshield/device/" + device.nome_attuatore + "/dimmer";
                clientMWTT.publish(topic, "on")
            }
        }
    };
    const t_button = () => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic = "/scsshield/device/" + device.nome_attuatore + "/dimmer";
                clientMWTT.publish(topic, "t")
            }
        }
    };
    const off_button = () => {
        if (clientMWTT) {
            if (clientMWTT.connected) {
                let topic = "/scsshield/device/" + device.nome_attuatore + "/dimmer";
                clientMWTT.publish(topic, "off")
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
                        <Container fluid >
                            <Row>
                                <Col lg={4} >
                                    <Row>
                                        <Col lg={8}><i>Stato Percentuale	</i></Col>
                                        <Col lg={8}><b>{statodimmerPercent}</b></Col>
                                    </Row>
                                </Col>
                                <Col lg={2} style={{ alignSelf: "center" }}>
                                    <Row>
                                        <Col lg={8}><i>Stato</i></Col>
                                        <Col lg={8}>
                                            <img data-icon="switch" src={"/site/image/" + statodimmerONOFF} style={{ width: "32px" }} />
                                        </Col>
                                    </Row>
                                </Col>
                                <Col lg={3}>
                                    <Row >
                                        <Col lg={6}><i>Set Dimmer</i></Col>
                                        <Col lg={8}>
                                            <div className="col-xs-1">
                                                <RangeSlider tooltip='off' value={percentualeDimmer} min="10" max="100" step="10" onChange={update_percentuale} onAfterChange={update_mqtt_dimmer} />
                                            </div>
                                        </Col>
                                    </Row>
                                </Col>
                                <Col style={{ alignSelf: "center" }}>
                                    <div style={{ textAlign: "center", alignItems: "right" }}>
                                        <button style={{ marginRight: "5px" }} type="button" className="btn btn-success btn-md" onClick={on_button}>ON</button>
                                        <button style={{ marginRight: "5px" }} type="button" className="btn btn-primary btn-md" onClick={t_button} >T</button>
                                        <button type="button" className="btn btn-danger btn-md" onClick={off_button}>OFF</button>
                                    </div>
                                </Col>
                            </Row>
                        </Container>
                    </Card.Body>
                    <Card.Footer className="text-muted" style={{ textAlign: "center" }}>
                        <p style={{ fontSize: "9px", margin: 0, padding: "0%" }}>-Tipo-</p>
                        <p style={{ fontSize: "15px", margin: 0, padding: "0%" }}>Dimmer</p>
                    </Card.Footer>
                </Card>
            </Container>
        </>
    );
}


export default Dimmer;