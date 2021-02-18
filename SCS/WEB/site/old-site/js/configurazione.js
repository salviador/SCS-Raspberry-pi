function popola_configurazione_attuatori(key, val) {
    var ON_OFF = "";
    var Dimmer = "";
    var Serrande_Tapparelle = "";
    var Gruppi = "";
    var Sensori_Temperatura = "";
    var Termostati = "";
    var Serrature = "";
    var Campanello_porta = "";
    
        switch(val.tipo_attuatore) {
            case "ON_OFF":
                ON_OFF = "selected";
              break;
            case "Dimmer":
                Dimmer = "selected";
              break;
            case "Serrande_Tapparelle":
                Serrande_Tapparelle = "selected";
            break;
            case "Gruppi":
                Gruppi = "selected";
            break;
            case "Sensori_Temperatura":
                Sensori_Temperatura = "selected";
            break;
            case "Termostati":
                Termostati = "selected";
            break;
            case "Serrature":
                Serrature = "selected";
            break;
            case "Campanello_porta":
                Campanello_porta = "selected";
            break;
          }

          var tipo_attuatore_html;

        //modifica interfaccia UI
        tipo_attuatore_html = html_x_tipo_attuatore(val.tipo_attuatore, key, val);
    

    $('#ChAudioTable').append('\
                <div class="container-fluid attuatore_' + key + '" style="padding-top: 13px;" > \
                    <div class="row"> \
                        <div class="col-2"> \
                            <div class="float-left"> \
                                <div class="form-group row"> \
                                    <input class="form-control CLASS_NOMEATTUATORE" type="text" value="' + val.nome_attuatore + '" id="' + key +'" name="fname" style="width: 100%;"> \
                                </div> \
                            </div> \
                        </div> \
                        <div class="col-3"> \
                            <select class="CLASS_TIPOATTUATORE" id="' + key + '" name="Tipi Attuatori"> \
                                <option ' + ON_OFF + ' value="ON_OFF">ON/OFF</option> \
                                <option ' + Dimmer + ' value="Dimmer">Dimmer</option> \
                                <option ' + Serrande_Tapparelle + ' value="Serrande_Tapparelle">Serrande/Tapparelle</option> \
                                <option ' + Gruppi + ' value="Gruppi">Gruppi</option> \
                                <option ' + Sensori_Temperatura + ' value="Sensori_Temperatura">Sensori Temperatura</option> \
                                <option ' + Termostati + ' value="Termostati">Termostati</option> \
                                <option ' + Serrature + ' value="Serrature">Serrature</option> \
                                <option ' + Campanello_porta + ' value="Campanello_porta">Campanello porta</option> \
                            </select> \
                        </div> \
                        <div class="col-3"> \
                            <div class="row" > \
                                <div class="col-6">\
                                    <div>\
                                        <input class="form-control CLASS_IND_ATTUATORE_A" type="number" value="' + val.indirizzo_Ambiente + '" id="' + key + '" style="width: 80%;"> \
                                    </div> \
                                </div>\
                                <div class="col-6"> \
                                    <div> \
                                        <input class="form-control CLASS_IND_ATTUATORE_PL" type="number" value="' + val.indirizzo_PL + '" id="' + key + '" style="width: 80%;"> \
                                    </div> \
                                </div> \
                            </div> \
                        </div> \
                        <div class="col-4"> \
                            <div class="float-center CLASS_BLOCK_TIPO_UI2 '+key+'">' + 
                            tipo_attuatore_html + '\
                            </div> \
                        </div> \
                    </div> \
                </div>' );
}


function setting_CLASS_BLOCK_TIPO_UI(val, nome, data){


    console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
    console.log(data);


    var htmlc = html_x_tipo_attuatore(val, nome, data);


    console.log("setting_CLASS_BLOCK_TIPO_UI");
    console.log(data);

    $('[class="row CLASS_BLOCK_TIPO_UI1 '+nome+'"]').remove();
    $('[class="float-center CLASS_BLOCK_TIPO_UI2 '+nome+'"]').append( htmlc);

}

function html_x_tipo_attuatore(val, nome, data){
    var htmlc;
    var value_timer_salita = 8000;
    var value_timer_discesa = 8000;


    if ('timer_salita' in data){
        value_timer_salita = data.timer_salita;
    }
    if ('timer_discesa' in data){
        value_timer_discesa = data.timer_discesa;
    }


        //modifica interfaccia UI
        if(val == "Serrande_Tapparelle"){
            htmlc = '<div class="row CLASS_BLOCK_TIPO_UI1 '+nome+'"> \
                            <div class="col-8"> \
                                <div class="float-left"> \
                                    <div class="row"> \
                                        <div class="col-6"> \
                                            <p style="font-size:0.8em">Timer ms<br>Salita  </p> \
                                        </div> \
                                        <div class="col-6"> \
                                            <input class="form-control CLASS_TIMER_SALITA" type="number" value="' + value_timer_salita + '" id="' + nome + '" > \
                                        </div> \
                                    </div> \
                                    <div class="row"> \
                                        <div class="col-6"> \
                                            <p style="font-size:0.8em">Timer ms<br>Discesa</p> \
                                        </div> \
                                        <div class="col-6"> \
                                            <input class="form-control CLASS_TIMER_DISCESA" type="number" value="'+value_timer_discesa+'" id="' + nome + '" > \
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                            <div class="col-4"> \
                                    <div class="float-right"> \
                                        <button type="button" id="nodi_remove_ch_1" class="btn btn-secondary btn-danger rowRemove">Elimina</button> \
                                    </div> \
                            </div> \
                        </div>';
        }else{
            htmlc = '<div class="row CLASS_BLOCK_TIPO_UI1 '+nome+'"> \
                            <div class="col-8"> \
                                <div class="float-left"> \
                                    <div class="row"> \
                                        <div class="col-6"> \
                                        </div> \
                                        <div class="col-6"> \
                                        </div> \
                                    </div> \
                                    <div class="row"> \
                                        <div class="col-6"> \
                                        </div> \
                                        <div class="col-6"> \
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                            <div class="col-4"> \
                                    <div class="float-right"> \
                                        <button type="button" id="'+ nome +'" class="btn btn-secondary btn-danger rowRemove">Elimina</button> \
                                    </div> \
                            </div> \
                        </div>';
        }
        return htmlc;
}



