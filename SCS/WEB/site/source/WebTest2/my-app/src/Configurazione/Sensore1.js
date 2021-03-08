import { useState, useEffect } from 'react';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';

import "./../App.css";





function Sensore1({ device, handle_CHANHE_NOME, handle_CHANHE_A, handle_CHANHE_PL, handle_TIPO, handle_TIMER_UP, handle_TIMER_DOWN, handle_ELIMINA}) {
    const [optionsStateTipoAttuatori, setoptionsStateTipoAttuatori] = useState("on_off");
    const [optionsStateTipoAttuatoriTIMER, setoptionsStateTipoAttuatoriTIMER] = useState(false);

    const [nomeATTUATORE, setinomeATTUATORE] = useState("");
    const [indirizzo_A, setindirizzo_A] = useState(0);
    const [indirizzo_PL, setindirizzo_PL] = useState(0);
    const [TIMER_UP, setTIMER_UP] = useState(8000);
    const [TIMER_DOWN, setTIMER_DOWN] = useState(8000);


    useEffect(() => {
        setoptionsStateTipoAttuatori(device.tipo_attuatore);
        setindirizzo_A(device.indirizzo_Ambiente);
        setindirizzo_PL(device.indirizzo_PL);
        if ('timer_salita' in device)
        {
            setTIMER_UP(device.timer_salita);
        }
        if ('timer_discesa' in device)
        {
            setTIMER_DOWN(device.timer_discesa);
        }

        setinomeATTUATORE(device.nome_attuatore);

        if(device.tipo_attuatore === "serrande_tapparelle"){
            setoptionsStateTipoAttuatoriTIMER(true);
        }else{
            setoptionsStateTipoAttuatoriTIMER(false);
        }
    }, []);


    //Option change , tipo attuatore
    const handleoptionsStateTipoAttuatori = (event) =>{
        setoptionsStateTipoAttuatori (event.target.value);
        if(event.target.value === "serrande_tapparelle"){
            setoptionsStateTipoAttuatoriTIMER(true);
        }else{
            setoptionsStateTipoAttuatoriTIMER(false);
        }
        handle_TIPO({nome_attuatore: device.nome_attuatore , tipo_attuatore : event.target.value});
    }
    //change , Indirizzo Ambiente
    const handlChangeAMBIENTEind = (event) =>{
        setindirizzo_A(event.target.value);
        handle_CHANHE_A({nome_attuatore: device.nome_attuatore , indirizzo_Ambiente : event.target.value});
    }
    //change , Indirizzo Puno Luce
    const handlChangePUNTOLUCEind = (event) =>{
        setindirizzo_PL(event.target.value);
        handle_CHANHE_PL({nome_attuatore: device.nome_attuatore , indirizzo_PL : event.target.value});
    }
    //change , Timer Salita [se esiste]
    const handlChangeTIMER_UP = (event) =>{
        setTIMER_UP(event.target.value);
        handle_TIMER_UP({nome_attuatore: device.nome_attuatore , timer_salita : event.target.value});
    }
    //change , Timer Discesa [se esiste]
    const handlChangeTIMER_DOWN = (event) =>{
        setTIMER_DOWN(event.target.value);
        handle_TIMER_DOWN({nome_attuatore: device.nome_attuatore , timer_discesa : event.target.value});
    }
    //change , NOME ATTUATORE [se esiste]
    const handleChangeNOME_ATTUTATORE = (event) =>{
        setinomeATTUATORE(event.target.value);
    }

    const handleChangeNOME_ATTUTATOREupdateDATABASE = (event) =>{
        console.log("QUI CAMBIO IL NOME ATTUATORRE");
        handle_CHANHE_NOME({nome_attuatore: device.nome_attuatore , nuovonome : nomeATTUATORE});
    }


    //ELIMINA BUTTON
    const handleELIMINA = () =>{
        console.log("handleELIMINA");
        handle_ELIMINA({nome_attuatore: device.nome_attuatore});
    }






    const timer_salitadiscesa = () => {
        return (
            <>
                <Col lg={3}>
                    <Col >
                        <Row >
                            <Col ><i>Timer Salita [mS]</i></Col>
                            <Col lg={12}>
                                <input className="form-control" onChange={handlChangeTIMER_UP} min='1000'type="number" name="SetTemp" step="1" value={TIMER_UP}  />
                            </Col>
                        </Row>
                    </Col>
                    <Col >
                        <Row >
                            <Col ><i>Timer Discesa [mS]</i></Col>
                            <Col lg={12}>
                                <input className="form-control" onChange={handlChangeTIMER_DOWN} min='1000' type="number" name="SetTemp" step="1" value={TIMER_DOWN} />
                            </Col>
                        </Row>
                    </Col>
                </Col>
            </>
        );
    };



    const Address_Campanello = () => {
        //label = Citofono interno

        return(
            <>



            </>
        );

    };


    const Address_Select = () => {

        if(optionsStateTipoAttuatori === "campanello_porta"){
            return(
                <>
                    <Col lg={2}>
                        <Row >
                            <Col lg={8}><i>Citofono interno</i></Col>
                            <Col lg={8}>
                                <input onChange={handlChangePUNTOLUCEind} className="form-control" style={{ width: "90%" }} min='0' max='9' type="number" name="PuntoLuce" step="1" value={indirizzo_PL} />
                            </Col>
                        </Row>
                    </Col>
                    <Col lg={2}>
                        <Row>
                            <Col lg={8}><i></i></Col>
                            <Col lg={8}>
                            </Col>
                        </Row>
                    </Col>
    
                </>
            );
        }else if(optionsStateTipoAttuatori === "serrature"){
            return(
                <>
                    <Col lg={2}>
                        <Row >
                            <Col lg={8}><i>Posto Esterno</i></Col>
                            <Col lg={8}>
                                <input onChange={handlChangeAMBIENTEind} className="form-control" style={{ width: "90%" }} min='0' max='9' type="number" name="Ambiente" step="1" value={indirizzo_A} />
                            </Col>
                        </Row>
                    </Col>
                    <Col lg={2}>
                        <Row>
                            <Col lg={8}><i></i></Col>
                            <Col lg={8}>
                            </Col>
                        </Row>
                    </Col>
    
                </>
            );
        }else{
            return(
                <>
                    <Col lg={2}>
                        <Row >
                            <Col lg={8}><i>Ambiente</i></Col>
                            <Col lg={8}>
                                <input onChange={handlChangeAMBIENTEind} className="form-control" style={{ width: "90%" }} min='0' max='9' type="number" name="Ambiente" step="1" value={indirizzo_A} />
                            </Col>
                        </Row>
                    </Col>
                    <Col lg={2}>
                        <Row>
                            <Col lg={8}><i>Puno Luce</i></Col>
                            <Col lg={8}>
                                <input onChange={handlChangePUNTOLUCEind} className="form-control" style={{ width: "90%" }} min='0' max='9' type="number" name="PuntoLuce" step="1" value={indirizzo_PL} />
                            </Col>
                        </Row>
                    </Col>
    
                </>
            );
        }
    };






    return (
        <>
            <Container style={{ paddingTop: "20px" }} >
                <Card style={{ width: '100%', border: "1px solid black" }}>
                    <Card.Header>
                        <Row>
                            <Col lg={4} style={{ textAlign: 'left' }} className="text-primary">
                                <input type="text" className="form-control" value={nomeATTUATORE} onChange={handleChangeNOME_ATTUTATORE} onBlur={handleChangeNOME_ATTUTATOREupdateDATABASE} />
                            </Col>
                        </Row>
                    </Card.Header>
                    <Card.Body>
                        <Container fluid>
                            <Row >
                                {Address_Select()}

                                <Col lg={optionsStateTipoAttuatoriTIMER ? 3 : 6} >
                                    <Row >
                                        <Col lg={8}><i>Tipo Attuatore</i></Col>
                                        <Col lg={8}>
                                            <select id="cars" name="cars" value={optionsStateTipoAttuatori} onChange={handleoptionsStateTipoAttuatori}>>
                                                <option value="on_off">ON/OFF</option>
                                                <option value="dimmer">Dimmer</option>
                                                <option value="serrande_tapparelle">Serrande/Tapparelle</option>
                                                <option value="gruppi">Gruppi</option>
                                                <option value="sensori_temperatura">Sensori Temperatura</option>
                                                <option value="termostati">Termostati</option>
                                                <option value="serrature">Serrature</option>
                                                <option value="campanello_porta">Campanello porta</option>
                                            </select>
                                        </Col>
                                    </Row>
                                </Col>

                                {optionsStateTipoAttuatoriTIMER ? timer_salitadiscesa() : null}


                                <Col style={{ alignSelf: "center" }}>
                                    <div style={{ textAlign: "center", alignItems: "right" }}>
                                        <Button style={{ marginRight: "8px" }} size="md" variant="outline-danger" onClick={handleELIMINA} >ELIMINA</Button>
                                    </div>
                                </Col>
                            </Row>
                        </Container>
                    </Card.Body>
                </Card>
            </Container>
        </>
    );

}



export default Sensore1;


