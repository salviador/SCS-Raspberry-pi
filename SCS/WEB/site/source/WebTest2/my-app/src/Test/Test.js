import { useState, useEffect } from 'react';
import Dispositivi from './Dispositivi';

import mqtt from "mqtt";
import "./../App.css";


//https://levelup.gitconnected.com/mqtt-over-websocket-in-a-react-app-35ce96cd0844



//const websocketUrl = "ws://192.168.1.16:9001";
var loc = window.location, new_uri;
const websocketUrl = "ws://" + loc.host + ":9001";

//const ADDRESS_SERVER = "http://192.168.1.16/";
const ADDRESS_SERVER = "/";




function Test() {
    const [lista_dispositivi, setListaDispositivi] = useState([]);
    const [MqttClient, setMqttClient] = useState([]);

    const [MQTT_data, setMQTT_data] = useState("");

    const [DebugSCSbus, setDebugSCSbus] = useState("");

    useEffect(() => {
        var client = null;

        setListaDispositivi([]);
        console.log("**** FETCH DATA ****");

        const fetchData = async () => {
            await fetch(ADDRESS_SERVER + 'GetConfigurazionereact.json')
                .then(res => res.json())
                .then((data) => {
                    setListaDispositivi(data);
                });
        };


        const mqttconnect = () => {
            if (client == null) {

            } else {
                console.log("CLOSEEEE era aperto");
                client.unsubscribe("/scsshield/device/+/status");
                client.unsubscribe("/scsshield/device/+/status/percentuale");
                client.unsubscribe("/scsshield/device/+/modalita_termostato_impostata");
                client.unsubscribe("/scsshield/device/+/temperatura_termostato_impostata");
               // client.unsubscribe("/scsshield/debug/bus");
                client.end();
                client.close();
            }
            client = mqtt.connect(websocketUrl);
            setMqttClient(client);

            client.on('connect', function () {
                console.log("MQTT Connesso....ok!");
                client.subscribe("/scsshield/device/+/status");
                client.subscribe("/scsshield/device/+/status/percentuale");
                client.subscribe("/scsshield/device/+/modalita_termostato_impostata");
                client.subscribe("/scsshield/device/+/temperatura_termostato_impostata");
             //   client.subscribe("/scsshield/debug/bus");

            });
            client.on('error', function () {
                console.log("MQTT ERROR!");
                client.end();
            });
            client.on('message', function (topic, payload, packet) {
                const data = new TextDecoder("utf-8").decode(payload);

                if (topic.localeCompare("/scsshield/debug/bus") == 0) {
                    setDebugSCSbus(DebugSCSbus => [...DebugSCSbus, data + '\n']);
                } else {

                    var m = (topic).split("/");
                    var nomeDevice = m[3];

                    var mesg = (data).toLowerCase();

                    const dd = { "nome_attuatore": nomeDevice, "stato": mesg, "topic": topic };

                    setMQTT_data(dd);

                    console.log(dd.nome_attuatore);
                    console.log(dd.stato);
                }

            });
        };

        fetchData();
        mqttconnect();

        return () => {
            console.log("CLOSEEE");
            setListaDispositivi([]);

            client.unsubscribe("/scsshield/device/+/status");
            client.unsubscribe("/scsshield/device/+/status/percentuale");
            client.unsubscribe("/scsshield/device/+/modalita_termostato_impostata");
            client.unsubscribe("/scsshield/device/+/temperatura_termostato_impostata");
            client.end();
            //MqttClient.close();
            // cleaning up the listeners here
        }
    }, []);







    return (
        <>
            <div className="container-fluid">
                {lista_dispositivi.map((device, i) => (
                    <div key={i} style={{marginBottom:"50px"}} >
                        <Dispositivi device={device} mqttdata={MQTT_data} clientMWTT={MqttClient} />
                    </div>
                ))}
            </div>
            {
            /*<div className="DebugSCSbus" style={{ textAlign: "center" }}>
                <textarea style={{ width: "80%" }} value={DebugSCSbus} rows={12} cols={50} name="Debug Bus" placeholder='' />
            </div>
            */
            }
        </>
    );










}



export default Test;