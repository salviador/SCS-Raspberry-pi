function popola_Test_attuatori(key, val) {

    
    var Dimmer = "";
    var Serrande_Tapparelle = "";
    var Gruppi = "";
    var Sensori_Temperatura = "";
    var Termostati = "";
    var Serrature = "";
    var Campanello_porta = "";
    
        switch(val.tipo_attuatore) {
            case "ON_OFF":
                popola_tipo_onoff(key,val);
            break;
            case "Dimmer":
                popola_tipo_dimmer(key,val);
            break;
            case "Serrande_Tapparelle":
                popola_tipo_serrandatapparella(key,val);
            break;
            case "Gruppi":
                Gruppi = "selected";
            sbreak;
            case "Sensori_Temperatura":
                popola_tipo_Sensori_Temperatura(key,val);  
            break;
            case "Termostati":
                popola_tipo_Termostato(key,val);
            break;
            case "Serrature":
                Serrature = "selected";
            break;
            case "Campanello_porta":
                Campanello_porta = "selected";
            break;
          }



    



}




function popola_tipo_onoff(key, val) {
    $('#ChAudioTable').append('\
                    <div class="container-fluid attuatore_' + key + '" style="padding-top: 13px;"> \
                        <div class="row"> \
                            <div class="col-3"> \
                                <div class="float-left"> \
                                    <p class="text-left ' + key + '" > ' + val.nome_attuatore + '</p> \
                                </div> \
                            </div> \
                            <div class="col-2"> \
                                <div class="float-left"> \
                                    <p>ON/OFF</p> \
                                </div> \
                            </div> \
                            <div class="col-3"> \
                                <div class="float-center" style="width: 80%; text-align: center;"> \
                                    <div class="row"> \
                                        <div class="col-6"> \
                                            <div class="float-left"> \
                                                <p class="CLASS_T_ONOFF_ATTUATORE_A">' + val.indirizzo_Ambiente + '</p> \
                                            </div> \
                                        </div> \
                                        <div class="col-6"> \
                                            <div class="float-left"> \
                                                <p class="CLASS_T_ONOFF_ATTUATORE_PL">' + val.indirizzo_PL + '</p> \
                                            </div>\
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                            <div class="col-4"> \
                                <div class="float-center"> \
                                    <div class="row"> \
                                        <div class="col-4"> \
                                            <span class="mdl-form__icon"> \
                                                <img class="imgON_OFF_' + key + '" data-icon="switch" src="/site/image/lamp_accesa.svg" style="width:32px;"/> \
                                            </span> \
                                        </div> \
                                        <div class="col-8"> \
                                            <div class="float-center">\
                                                <button type="button" id="' + key + '" class="btn btn-success CLASS_T_ONOFF_ON">On</button> \
                                                <button type="button" id="' + key + '" class="btn btn-primary CLASS_T_ONOFF_TOGGLE">T</button> \
                                                <button type="button" id="' + key + '" class="btn btn-danger CLASS_T_ONOFF_OFF">Off</button>\
                                            </div> \
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                        </div> \
                    </div>');
}


function popola_tipo_serrandatapparella(key, val) {

    $('#ChAudioTable').append('\
                    <div class="container-fluid attuatore_' + key + '" style="padding-top: 13px;"> \
                        <div class="row"> \
                            <div class="col-3"> \
                                <div class="float-left"> \
                                    <p class="text-left ' + key + '" > ' + val.nome_attuatore + '</p> \
                                </div> \
                            </div> \
                            <div class="col-2"> \
                                <div class="float-left"> \
                                    <p>' + val.tipo_attuatore + '</p> \
                                </div> \
                            </div> \
                            <div class="col-3"> \
                                <div class="float-center" style="width: 80%; text-align: center;"> \
                                    <div class="row"> \
                                        <div class="col-6"> \
                                            <div class="float-left"> \
                                                <p class="CLASS_T_ONOFF_ATTUATORE_A">' + val.indirizzo_Ambiente + '</p> \
                                            </div> \
                                        </div> \
                                        <div class="col-6"> \
                                            <div class="float-left"> \
                                                <p class="CLASS_T_ONOFF_ATTUATORE_PL">' + val.indirizzo_PL + '</p> \
                                            </div>\
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                            <div class="col-4"> \
                                <div class="float-center"> \
                                    <div class="row"> \
                                        <div class="col-4"> \
                                            <span class="SERRANDAPERCENTUALE_' + key + '">30%</span> \
                                        </div> \
                                        <div class="col-8"> \
                                            <div class="float-center">\
                                                <div class="d-flex">\
                                                    <span class="indigo-text mr-1">0</span>\
                                                    <form class="range-field"> \
                                                        <input type="range" id=SERRANDA_RANGE_' + key + ' class="form-range CLASS_T_SERRANDA_RANGE" min="0" max="100" step="1" /> \
                                                    </form> \
                                                    <span class="indigo-text">100</span>\
                                                </div> \
                                            </div> \
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                        </div> \
                    </div>');
}






function popola_tipo_dimmer(key, val) {

    $('#ChAudioTable').append('\
                    <div class="container-fluid attuatore_' + key + '" style="padding-top: 13px;"> \
                        <div class="row"> \
                            <div class="col-3"> \
                                <div class="float-left"> \
                                    <p class="text-left ' + key + '" > ' + val.nome_attuatore + '</p> \
                                </div> \
                            </div> \
                            <div class="col-2"> \
                                <div class="float-left"> \
                                    <p>' + val.tipo_attuatore + '</p> \
                                </div> \
                            </div> \
                            <div class="col-3"> \
                                <div class="float-center" style="width: 80%; text-align: center;"> \
                                    <div class="row"> \
                                        <div class="col-6"> \
                                            <div class="float-left"> \
                                                <p class="CLASS_T_ONOFF_ATTUATORE_A">' + val.indirizzo_Ambiente + '</p> \
                                            </div> \
                                        </div> \
                                        <div class="col-6"> \
                                            <div class="float-left"> \
                                                <p class="CLASS_T_ONOFF_ATTUATORE_PL">' + val.indirizzo_PL + '</p> \
                                            </div>\
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                            <div class="col-4"> \
                                <div class="float-center"> \
                                    <div class="row"> \
                                        <div class="col-4"> \
                                            <img id="'+key+'" class="CLASS_T_DIMMER_ONOFF imgON_OFF_' + key + '" data-icon="switch" src="/site/image/lamp_accesa.svg" style="width:32px;"/> \
                                            <span class="SERRANDAPERCENTUALE_' + key + '">30%</span> \
                                        </div> \
                                        <div class="col-8"> \
                                            <div class="float-center">\
                                                <div class="d-flex">\
                                                    <span class="indigo-text mr-1">0</span>\
                                                    <form class="range-field"> \
                                                        <input type="range" id=SERRANDA_RANGE_' + key + ' class="form-range CLASS_T_DIMMER_RANGE" min="10" max="100" step="10" /> \
                                                    </form> \
                                                    <span class="indigo-text">100</span>\
                                                </div> \
                                            </div> \
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                        </div> \
                    </div>');
}





function popola_tipo_Sensori_Temperatura(key, val) {
    $('#ChAudioTable').append('\
                    <div class="container-fluid attuatore_' + key + '" style="padding-top: 13px;"> \
                        <div class="row"> \
                            <div class="col-3"> \
                                <div class="float-left"> \
                                    <p class="text-left ' + key + '" > ' + val.nome_attuatore + '</p> \
                                </div> \
                            </div> \
                            <div class="col-2"> \
                                <div class="float-left"> \
                                    <p>' + val.tipo_attuatore + '</p> \
                                </div> \
                            </div> \
                            <div class="col-3"> \
                                <div class="float-center" style="width: 80%; text-align: center;"> \
                                    <div class="row"> \
                                        <div class="col-6"> \
                                            <div class="float-left"> \
                                                <p class="CLASS_T_ONOFF_ATTUATORE_A">' + val.indirizzo_Ambiente + '</p> \
                                            </div> \
                                        </div> \
                                        <div class="col-6"> \
                                            <div class="float-left"> \
                                                <p class="CLASS_T_ONOFF_ATTUATORE_PL">' + val.indirizzo_PL + '</p> \
                                            </div>\
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                            <div class="col-4"> \
                                <div class="float-center"> \
                                    <div class="row"> \
                                        <div class="col-4"> \
                                                <span class="SENSORE_TEMP_VALUE_' + key + '">--°</span> \
                                        </div> \
                                        <div class="col-8"> \
                                            <div class="float-center">\
                                                <button type="button" id="' + key + '" class="btn btn-primary CLASS_T_REFRESH_BUTTON_SENSTEMP">Aggiorna</button> \
                                            </div> \
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                        </div> \
                    </div>');
}









function popola_tipo_Termostato(key, val) {
    $('#ChAudioTable').append('\
                    <div class="container-fluid attuatore_' + key + '" style="padding-top: 13px;"> \
                        <div class="row"> \
                            <div class="col-3"> \
                                <div class="float-left"> \
                                    <p class="text-left ' + key + '" > ' + val.nome_attuatore + '</p> \
                                </div> \
                            </div> \
                            <div class="col-2"> \
                                <div class="float-left"> \
                                    <p>' + val.tipo_attuatore + '</p> \
                                </div> \
                            </div> \
                            <div class="col-3"> \
                                <div class="float-center" style="width: 80%; text-align: center;"> \
                                    <div class="row"> \
                                        <div class="col-6"> \
                                            <div class="float-left"> \
                                                <p class="CLASS_T_ONOFF_ATTUATORE_A">' + val.indirizzo_Ambiente + '</p> \
                                            </div> \
                                        </div> \
                                        <div class="col-6"> \
                                            <div class="float-left"> \
                                                <p class="CLASS_T_ONOFF_ATTUATORE_PL">' + val.indirizzo_PL + '</p> \
                                            </div>\
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                            <div class="col-4"> \
                                <div class="float-left container"> \
                                    <div class="row"> \
                                        <div class="col-10"> \
                                            <div class="sl-4 container">\
                                                <div class="row">\
                                                    <div class="col-4"> \
                                                        <span>Temp</span> \
                                                    </div> \
                                                    <div class="col-4"> \
                                                        <span>Set-Temp</span> \
                                                    </div> \
                                                    <div class="col-4"> \
                                                        <span>Modalità</span> \
                                                    </div>\
                                                </div> \
                                                <div class="row"> \
                                                    <div class="col-4"> \
                                                        <span class="TERMOSTATO_SENSOR_TEMP_VALUE_' + key + '">--°</span> \
                                                    </div> \
                                                    <div class="col-4"> \
                                                        <span class="TERMOSTATO_SETTING_TEMP_VALUE_' + key + '">--°</span> \
                                                    </div> \
                                                    <div class="col-4"> \
                                                        <span class="TERMOSTATO_MODALITA_VALUE_' + key + '">--°</span> \
                                                    </div>\
                                                </div> \
                                            </div> \
                                        </div> \
                                        <div class="col-2"> \
                                            <div class="float-right">\
                                                <button type="button" id="' + key + '" class="btn btn-primary CLASS_T_REFRESH_BUTTON_SENSTEMP">Aggiorna</button> \
                                            </div> \
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                        </div> \
                    </div>');
}





