function popola_mainNodi(key, val) {

    $('#ChAudioTable').append('\
                <div class="container-fluid' + key + '" style="padding-top: 13px;" > \
                <div class="row"> \
                    <div class="col-2"> \
                        <div class="float-left" > \
                            <div class="form-group row"style="margin-left: 1em;"> \
                                <p>' + key + '</p> \
                            </div> \
                        </div> \
                    </div> \
                    <div class="col-2"> \
                            <p>' + val.nome + '</p> \
                    </div> \
                    <div class="col-2"> \
                        <p>' +  val.chAudio +'</p> \
                    </div> \
                    <div class="col-2"> \
                        <p>' + val.nomeAudio + '</p> \
                    </div> \
                    <div class="col-4"> \
                        <div class="float-right" style="margin-right: 1em;"> \
                            <img src="/site/image/soundOFF.png" alt="Sound OFF" height="42" width="42"> \
                        </div> \
                    </div> \
                </div> \
            </div>' );
}
