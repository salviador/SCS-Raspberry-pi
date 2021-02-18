import React from "react";
import ON_OFF from "./Switch"
import Sensori_Temperatura from "./Sensori_Temperatura"
import Termostati from "./Termostati"
import Serrande_Tapparelle from "./Serrande_Tapparelle"
import Dimmer from "./Dimmer"


import "./../App.css";






function Dispositivi({ device, mqttdata, clientMWTT }) {

    if (device.tipo_attuatore === "on_off") {
        return (
            <>
                <ON_OFF device={device} valuedataRT={mqttdata} clientMWTT={clientMWTT} />
            </>
        );
    } else if (device.tipo_attuatore === "sensori_temperatura") {
        return (
            <>
                <Sensori_Temperatura device={device} valuedataRT={mqttdata} clientMWTT={clientMWTT} />
            </>
        );
    } else if (device.tipo_attuatore === "termostati") {
        return (
            <>
                <Termostati device={device} valuedataRT={mqttdata} clientMWTT={clientMWTT}/>
            </>
        );
    }else if (device.tipo_attuatore === "serrande_tapparelle") {
        return (
            <>
                <Serrande_Tapparelle device={device} valuedataRT={mqttdata} clientMWTT={clientMWTT}/>
            </>
        );
    }else if (device.tipo_attuatore === "dimmer") {
        return (
            <>
                <Dimmer device={device} valuedataRT={mqttdata} clientMWTT={clientMWTT}/>
            </>
        );
    }


    

    return (
        <>
        </>
    );

}


export default Dispositivi;










