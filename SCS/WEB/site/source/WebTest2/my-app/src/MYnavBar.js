import React from 'react';
import { Container, Navbar, Nav, Button, Card, Row, Col } from 'react-bootstrap';

import "./App.css"



function MYnavBar() {
    return (
        <>
            <Container>
                <Navbar bg="light" expand="lg">
                    <Navbar.Brand href="">SCSshield</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="mr-auto">
                            <Nav.Link href="/">Home</Nav.Link>
                            <Nav.Link href="configurazione.html">Configurazioni</Nav.Link>
                            <Nav.Link href="test.html">Test</Nav.Link>
                            <Nav.Link href="noderedHome.html">Node-Red</Nav.Link>                           
                        </Nav>
                    </Navbar.Collapse>
                </Navbar>
            </Container>
        </>
    );
}


export default MYnavBar;