import { useState, useEffect } from 'react';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';
import Sensore1 from "./Sensore1"

import "./../App.css";





function ConfigurazioneDispositivi({ device , handle_CHANHE_NOME, handle_CHANHE_A, handle_CHANHE_PL, handle_TIPO, handle_TIMER_UP, handle_TIMER_DOWN, handle_ELIMINA}) {

    return (
        <>
            <Sensore1 device={device} handle_CHANHE_NOME={handle_CHANHE_NOME} handle_CHANHE_A={handle_CHANHE_A} 
                   handle_CHANHE_PL={handle_CHANHE_PL} handle_TIPO={handle_TIPO} handle_TIMER_UP={handle_TIMER_UP} handle_TIMER_DOWN={handle_TIMER_DOWN}
                   handle_ELIMINA={handle_ELIMINA} />
        </>
    );

}



export default ConfigurazioneDispositivi;


