import { useState, useEffect } from 'react';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';

import "./../App.css";





function AggiungiAttuatore({handel_AGIUNGInew} ) {
    var timersalitadiscesa = false;

    const [nomeATTUATORE, setinomeATTUATORE] = useState("");
    const [indirizzo_A, setindirizzo_A] = useState(0);
    const [indirizzo_PL, setindirizzo_PL] = useState(0);

    const [optionsStateTipoAttuatori, setoptionsStateTipoAttuatori] = useState("on_off");
    const [optionsStateTipoAttuatoriTIMER, setoptionsStateTipoAttuatoriTIMER] = useState(false);

    const [TIMER_UP, setTIMER_UP] = useState(8000);
    const [TIMER_DOWN, setTIMER_DOWN] = useState(8000);


    //change , NOME ATTUATORE [se esiste]
    const handleChangeNOME_ATTUTATORE = (event) =>{
        setinomeATTUATORE(event.target.value);
    }
    const handleChangeNOME_ATTUTATOREupdateDATABASE = (event) =>{
        //Qui ho il nome Attuatore Completo
    }

     //change , Indirizzo Ambiente
     const handlChangeAMBIENTEind = (event) =>{
        setindirizzo_A(event.target.value);
    }
    //change , Indirizzo Puno Luce
    const handlChangePUNTOLUCEind = (event) =>{
        setindirizzo_PL(event.target.value);
    }

    //Option change , tipo attuatore
    const handleoptionsStateTipoAttuatori = (event) =>{

        setoptionsStateTipoAttuatori (event.target.value);
        if(event.target.value === "serrande_tapparelle"){
            setoptionsStateTipoAttuatoriTIMER(true);
        }else{
            setoptionsStateTipoAttuatoriTIMER(false);
        }
    }
    //change , Timer Salita [se esiste]
    const handlChangeTIMER_UP = (event) =>{
        setTIMER_UP(event.target.value);
    }
    //change , Timer Discesa [se esiste]
    const handlChangeTIMER_DOWN = (event) =>{
        setTIMER_DOWN(event.target.value);
    }

    //CLICK AGGIUNGI
    const handlClickAGGIUNGI = (event) =>{
        if(optionsStateTipoAttuatori === "serrande_tapparelle"){
            handel_AGIUNGInew({nome_attuatore: nomeATTUATORE, indirizzo_Ambiente : indirizzo_A,
                indirizzo_PL : indirizzo_PL, tipo_attuatore : optionsStateTipoAttuatori, 
                timer_salita : TIMER_UP, timer_discesa: TIMER_DOWN });
        }else{
            handel_AGIUNGInew({nome_attuatore: nomeATTUATORE, indirizzo_Ambiente : indirizzo_A,
                indirizzo_PL : indirizzo_PL, tipo_attuatore : optionsStateTipoAttuatori});
        }
        setinomeATTUATORE("");
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


    const Address_Select = () => {

        if(optionsStateTipoAttuatori === "campanello_porta"){
            return(
                <>
                    <Col lg={2}>
                        <Row >
                            <Col lg={8}><i>Citofono interno</i></Col>
                            <Col lg={8}>
                                <input className="form-control" style={{ width: "90%" }} type="number" name="SetTemp" min="0" max="9" step="1" value={indirizzo_PL} onChange={handlChangePUNTOLUCEind} />
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
                                <input className="form-control" style={{ width: "90%" }} type="number" name="SetTemp" min="0" max="9" step="1" value={indirizzo_A} onChange={handlChangeAMBIENTEind} />
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
                               <input className="form-control" style={{ width: "90%" }} type="number" name="SetTemp" min="0" max="9" step="1" value={indirizzo_A} onChange={handlChangeAMBIENTEind} />
                            </Col>
                        </Row>
                    </Col>
                    <Col lg={2}>
                        <Row>
                            <Col lg={8}><i>Puno Luce</i></Col>
                            <Col lg={8}>
                               <input className="form-control" style={{ width: "90%" }} type="number" name="SetTemp" min="0" max="9" step="1" value={indirizzo_PL} onChange={handlChangePUNTOLUCEind} />
                            </Col>
                        </Row>
                    </Col>
    
                </>
            );
        }
    };





    return (
        <>
            <Container style={{ paddingTop: "2rem" }}>
            <hr></hr>

            <div>
                <h3>Aggiungi Attuatore</h3>
            </div>
            </Container>

            <Container style={{ paddingTop: "20px", marginBottom:'100px' }} >
                <Card  style={{ width: '100%', border: "2px solid blue" }}>
                    <Card.Header className="bg-secondary ">
                        <Row>
                            <Col lg={4} style={{ textAlign: 'left' }} className="text-primary">
                                <input type="text" className="form-control" value={nomeATTUATORE} placeholder="Inserisci il nome dell'Attuatore" onChange={handleChangeNOME_ATTUTATORE} onBlur={handleChangeNOME_ATTUTATOREupdateDATABASE} />
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
                                            <select name="tipiattuatori" value={optionsStateTipoAttuatori} onChange={handleoptionsStateTipoAttuatori}> 
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
                                        <Button style={{ marginRight: "8px" }} size="md" className="btn-primary" onClick={handlClickAGGIUNGI} >AGGIUNGI</Button>
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



export default AggiungiAttuatore;


