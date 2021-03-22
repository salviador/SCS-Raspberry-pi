import { useState, useEffect, useRef } from 'react';
import { Container, Form, Navbar, Button, Card, Row, Col } from 'react-bootstrap';
import NodeRedAWSDispositivi from "./NodeRedAWSDispositivi"



import "./../App.css";
//https://www.pluralsight.com/guides/uploading-files-with-reactjs


//const ADDRESS_SERVER = "http://192.168.1.16/";
const ADDRESS_SERVER = "/";


function NoderedAlexaAWS() {
    //Indirizzo EndPoint
    const [add_EndPoint, setadd_EndPoint] = useState("");
    //File name Certificati
    const [FILE_private_key, setFILE_private_key] = useState("");
    const [FILE_cert_pem, setFILE_cert_pem] = useState("");
    const [FILE_root_CA, setFILE_root_CA] = useState("");
    //Dispositivi e ENDPOINT
    const [lista_dispositivi, setListaDispositivi] = useState([]);

    const [flow_anuale, setflow_anuale] = useState("");
    const textAreaRef = useRef(null);
    const [stato_startmanuale, setstato_startmanuale] = useState(false);


    useEffect(() => {
        setListaDispositivi([]);

        const fetchDataDispositivi = async () => {
            await fetch(ADDRESS_SERVER + 'GetConfigurazionereact.json')
                .then(res => res.json())
                .then((data) => {
                    setListaDispositivi(data);
                });
        };


        fetchData();
        fetchDataDispositivi();

    }, []);

    const fetchData = async () => {
        await fetch(ADDRESS_SERVER + 'GetConfigurazionereactAWS.json')
            .then(res => res.json())
            .then((data) => {
                setadd_EndPoint(data.EndPoint);
                setFILE_private_key(data.PRIVATE_KEY);
                setFILE_cert_pem(data.CERT_PEM);
                setFILE_root_CA(data.CRT);
            });
    };


    //POST ---->OK<----
    const post_request_update_database = (datas) => {
        var data = JSON.stringify(datas);
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: data
        };
        fetch(ADDRESS_SERVER + 'GetConfigurazionereactAWS.json', requestOptions)
            .then(response => response.json())
            .then(data => {
                console.log("OKKKKKKKKKKKKKKKKK");
                console.log(data);
            }
            );
    }


    const [selectedFile, setSelectedFile] = useState();

    const changeHandler = (event) => {
        setSelectedFile(event.target.files[0]);
        //setIsSelected(true);
    };

    const handleSubmission = (tipo) => {
        const formData = new FormData();
        formData.append('File', selectedFile);
        fetch(
            ADDRESS_SERVER + 'AWSCertificatiploadHandler.html?tipo=' + tipo,
            {
                method: 'POST',
                body: formData,
            }
        )
            .then((response) => response.json())
            .then((result) => {
                console.log('Success:', result);
                fetchData();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };







    //******************Indirizzo ENDPOINT******************
    //change
    const handleChangeEndPoint = (event) => {
        setadd_EndPoint(event.target.value);
    }
    const handleBlurEndPoint = (event) => {
        //Qui ho il nome Attuatore Completo
        //Update SERVER!
        var datas = { 'EndPoint': event.target.value };
        post_request_update_database(datas);
    }



    const handle_GeneraManuale = () => {

        const fetchData = async () => {
            await fetch(ADDRESS_SERVER + 'Get_NodeRedAWS_manual_flow.json')
                .then(res => res.text())
                .then((data) => {
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

    const handle_CopyClipboard = (e) => {
        textAreaRef.current.select();
        document.execCommand('copy');
        // This is just personal preference.
        // I prefer to not show the whole text area selected.
        e.target.focus();
        setstato_startmanuale(true);
    }


    return (
        <>

            <div className="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
                <h1 className="display-5">Configurazione AWS-IoT</h1>
            </div>


            <Container style={{ paddingTop: "20px" }} >
                <Card style={{ width: '100%', border: "1px solid black" }}>
                    <Card.Header>
                        EndPoint
                    </Card.Header>
                    <Card.Body>
                        <Container fluid>
                            <Row>
                                <Col lg={3} className="text-primary text-center">
                                </Col>
                                <Col lg={6} className="text-primary text-center">
                                    <input type="text" className="form-control" value={add_EndPoint} placeholder="Inserire indirizzo EndPoint AWS IoT" onChange={handleChangeEndPoint} onBlur={handleBlurEndPoint} />
                                </Col>
                            </Row>
                        </Container>
                    </Card.Body>
                </Card>
            </Container>


            <Container style={{ paddingTop: "20px" }} >
                <Card style={{ width: '100%', border: "1px solid black" }}>
                    <Card.Header>
                        Certificati AWS-IoT
                    </Card.Header>
                    <Card.Body>
                        <Container fluid>

                            <Row>
                                <Col lg={3} className="text-primary text-center">
                                    PRIVATE_KEY
                                </Col>
                                <Col lg={3} className="text-center">
                                    "{FILE_private_key}"
                                </Col>
                                <Col lg={3} className="text-center">
                                    <input type="file" name="file" accept=".pem.key" onChange={changeHandler} />
                                </Col>
                                <Col className="text-center">
                                    <button onClick={() => handleSubmission('PRIVATE_KEY')}>Submit</button>
                                </Col>
                            </Row>
                            <hr></hr>
                            <Row>
                                <Col lg={3} className="text-primary text-center">
                                    CERT_PEM
                                </Col>
                                <Col lg={3} className="text-center">
                                    "{FILE_cert_pem}"
                                </Col>
                                <Col lg={3} className="text-center">
                                    <input type="file" name="file" accept=".pem.crt" onChange={changeHandler} />
                                </Col>
                                <Col className="text-center">
                                    <button onClick={() => handleSubmission('CERT_PEM')}>Submit</button>
                                </Col>
                            </Row>
                            <hr></hr>
                            <Row>
                                <Col lg={3} className="text-primary text-center">
                                    root-CA
                                </Col>
                                <Col lg={3} className="text-center">
                                    "{FILE_root_CA}"
                                </Col>
                                <Col lg={3} className="text-center">
                                    <input type="file" name="file" accept=".pem,.txt" onChange={changeHandler} />
                                </Col>
                                <Col className="text-center">
                                    <button onClick={() => handleSubmission('root-CA')}>Submit</button>
                                </Col>
                            </Row>

                        </Container>
                    </Card.Body>
                </Card>
            </Container>


            <Container style={{ paddingTop: "20px" }} >
                <Card style={{ width: '100%', border: "1px solid black" }}>
                    <Card.Header>
                        Assegnazione endpoint AWS lambda ai Dispositivi
                    </Card.Header>
                    <Card.Body>
                        <Container fluid>

                                {lista_dispositivi.map((device, i) => (
                                    <div key={i} className="container-fluid">
                                        <NodeRedAWSDispositivi device={device}  />
                                    </div>
                                ))}

                        </Container>
                    </Card.Body>
                </Card>
            </Container>





            <Container style={{ paddingTop: "20px", paddingBottom: '40px' }} >
                <Card style={{ width: '100%', border: "1px solid black" }}>
                    <Card.Header>
                        Genera Flow NodeRed
                    </Card.Header>
                    <Card.Body>
                        <Container fluid className='text-center'>

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

                        </Container>
                    </Card.Body>
                </Card>
            </Container>












        </>
    );
}



export default NoderedAlexaAWS;