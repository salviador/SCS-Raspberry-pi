import { useState, useEffect, useRef } from 'react';
import { Container, Navbar, Button, Card, Row, Col } from 'react-bootstrap';

import "./../App.css";


//const ADDRESS_SERVER = "http://192.168.1.16/";
const ADDRESS_SERVER = "/";


function NodeRedAWSDispositivi({ device }) {
    // EndPoint
    const [name_EndPoint, setname_EndPoint] = useState("");

    useEffect(() => {
        setname_EndPoint(device.nome_endpoint);
    }, [device]);


    //POST ---->OK<----
    const post_request_update_database = (datas) => {
        var data = JSON.stringify(datas);
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: data
        };
        fetch(ADDRESS_SERVER + 'SetDeviceEndPointAWS.json', requestOptions)
            .then(response => response.json())
            .then(data => {
                console.log("OKKKKKKKKKKKKKKKKK");
                console.log(data);
            }
            );
    }

        

    //******************Device ENDPOINT******************
    //change
    const handleChangeAWSDeviceENDPOINT = (event) => {
        setname_EndPoint(event.target.value);
    }
    const handleBlurAWSDeviceENDPOINT = (event) => {
        //Qui ho il nome Attuatore Completo
        //Update SERVER!
        var datas = { 'nome_attuatore': device.nome_attuatore , 'nome_endpoint': event.target.value };
        post_request_update_database(datas);
    }






    return (
        <>
            <Row>
                <Col className="text-primary text-center">
                    {device.nome_attuatore}
                </Col>
                <Col lg={6} className="text-center">
                </Col>
                <Col>
                    <input type="text" className="form-control" value={name_EndPoint} placeholder="Inserisci endpoint" onChange={handleChangeAWSDeviceENDPOINT} onBlur={handleBlurAWSDeviceENDPOINT} />
                </Col>
            </Row>
            <hr></hr>
        </>
    );
}



export default NodeRedAWSDispositivi;