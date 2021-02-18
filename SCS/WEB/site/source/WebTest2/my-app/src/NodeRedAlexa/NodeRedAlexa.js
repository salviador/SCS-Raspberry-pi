import { useState, useEffect, useRef } from 'react';
import { Container, Navbar, Form, Button, Control, Row, Col, Modal } from 'react-bootstrap';

import "./../App.css";


//const ADDRESS_SERVER = "http://192.168.1.118/";
const ADDRESS_SERVER = "/";


function NoderedAlexa() {
    //const [startNodered_enable, setstartNodered_enable] = useState(true);
    const [stato_esporta, setstato_esporta] = useState(true);
    const [stato_startNode, setstato_startNode] = useState(false);
    const [link_nodered, setlink_nodered] = useState("");

    const [flow_anuale, setflow_anuale] = useState("");
    const textAreaRef = useRef(null);
    const [stato_startmanuale, setstato_startmanuale] = useState(false);


    const [secondu, setsecondu] = useState(30);
    const [over, setover] = useState(false);
    const [timerID, settimerID] = useState(null);

    var second = 30;

    useEffect(() => {
        if (secondu === 0) {
            clearTimeout(timerID);
        }

        return () => {
            //console.log("returnnnnnn");
            // clearTimeout(timerID);
        };
    }, [secondu]);


    const tick = () => {
        console.log('tick ' + second);
        if (second === 0) setover(true);
        else {
            console.log(second);
            second = (second - 1);
            setsecondu(second);


        }
    };

    const handle_count = () => {
        if (stato_startNode === false) {
            return (
                <>
                    <p></p>
                </>
            );
        }
        if (secondu === 0) {
            return (
                <>
                    <a href={link_nodered} target="_blank">{link_nodered} </a>
                </>
            );
        } else {
            console.log("countdown " + secondu);

            return (
                <>
                    <p> Wait NodeRed start: {secondu} sec</p>
                </>
            );

        }





    };

    const handle_Esporta = () => {
        setstato_esporta(false);
        var add = window.location.host.split(":");
        setlink_nodered('http://' + add[0] + ':1880');
        const fetchData = async () => {
            await fetch(ADDRESS_SERVER + 'Send_to_NodeRed.json')
                .then(res => res.json())
                .then((data) => {
                    console.log(data);
                });
        };
        fetchData();
        handle_startNodered();
    };


    const handle_startNodered = () => {

        const t = setInterval(() => tick(), 1000);
        settimerID(t);
        //        clearTimeout(timerID);

        setstato_startNode(true);

    };


    const handle_GeneraManuale = () => {

        const fetchData = async () => {
            await fetch(ADDRESS_SERVER + 'Get_NodeRed_manual_flow.json')
                .then(res => res.text())
                .then((data) => {
                    console.log(data);
                    setflow_anuale(data);
                });
        };
        fetchData();

    };

    const handle_codeflow_manuale = () => {
        if (flow_anuale === '') {
            return (
                <>


                </>
            );
        }

        return (
            <>
                <Form.Control as="textarea" rows={10} value={flow_anuale} readonly ref={textAreaRef} />
                <Button variant="outline-primary" onClick={handle_CopyClipboard}>Copy</Button>
            </>
        );
    };

    const handle_CopyClipboard = (e) => {
        textAreaRef.current.select();
        document.execCommand('copy');
        // This is just personal preference.
        // I prefer to not show the whole text area selected.
        e.target.focus();
        setstato_startmanuale(true);
    }




    const handle_codeflow_manuale_incolla = () => {
        var add = window.location.host.split(":");
        var add2 = ('http://' + add[0] + ':1880');
        if (stato_startmanuale === false) {
            return (
                <>
                    <p></p>
                </>
            );
        }
        return (
            <>
                <ul style={{ listStyleType: 'none' }} >
                    <li>Apri node-red</li>
                    <li>Importa Flow</li>
                    <li>Incolla il contenuto generato</li>
                </ul>


                <a href={add2} target="_blank">{add2} </a>

            </>
        );
    };























    return (
        <>



            <Container className="justify-content-md-center" style={{}}>
                <div className="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
                    <h1 className="display-4">Node-Red configurazione con Alexa</h1>
                </div>


                <div className="card-deck text-center" >
                    <div className="card mb-4 shadow-sm" style={{ border: "1px solid black" }}>
                        <div className="card-header">
                            <h4 className="my-0 font-weight-normal">Configurazione Automatica</h4>
                        </div>
                        <div className="card-body">
                            <div className="container"><i style={{ color: "red" }} >Eseguire i seguenti passaggi descritti in seguito:</i></div>
                            <h1 className="card-title "> <small className="text-muted"> </small></h1>
                            <ul className="list-unstyled mt-3 mb-4">
                                <li>
                                    <p>Esporta auto-configurazione</p>
                                    <Button variant="outline-primary" onClick={handle_Esporta} >1 - Esporta su Node-Red</Button>
                                </li>
                                <li style={{ marginTop: "20px" }}>
                                    {handle_count()}
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>





                <div className="card-deck text-center"  >
                    <div className="card mb-4 shadow-sm" style={{ border: "1px solid black" }}>
                        <div className="card-header">
                            <h4 className="my-0 font-weight-normal">Configurazione Manuale</h4>
                        </div>
                        <div className="card-body">
                            <div className="container"><i style={{ color: "red" }} >Eseguire i seguenti passaggi descritti in seguito:</i></div>
                            <h1 className="card-title "> <small className="text-muted"> </small></h1>
                            <ul className="list-unstyled mt-3 mb-4">
                                <li>
                                    <p>Genera NodeRed Flow</p>
                                    <Button variant="outline-primary" onClick={handle_GeneraManuale} >Genera</Button>
                                </li>
                                <li style={{ marginTop: "20px" }}>
                                    {handle_codeflow_manuale()}
                                </li>
                                <li style={{ marginTop: "20px" }}>
                                    {handle_codeflow_manuale_incolla()}
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>








            </Container>

        </>
    );
}



export default NoderedAlexa;