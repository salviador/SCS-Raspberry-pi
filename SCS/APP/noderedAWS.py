import time
import os
import databaseAttuatori
import uuid
import random
import json
import asyncio
import subprocess

class noderedAWS():
    def __init__(self) -> None:
        self.ID_tab = self.genera_random_ID()
        self.ID_MQTT_broker = self.genera_random_ID()

        self.x = 90
        self.y = 40 #60

        self.xswich = 90
        self.yswitch = 40 #60
        self.xdimmer = 90
        self.ydimmer = 40 #60
        self.xsensori_temperatura = 90
        self.ysensori_temperatura = 40 #60
        self.xtermostati = 90
        self.ytermostati = 40 #60
        self.xserrande_tapparelle = 90
        self.yserrande_tapparelle = 40 #60
        self.xgruppi = 90
        self.ygruppi = 40 #60
        self.xserrature = 90
        self.yserrature = 40 #60
        self.xcampanello = 90
        self.ycampanello = 40 #60

        
        self.dbm = databaseAttuatori.configurazione_database()

        

    def Tab(self) -> dict:
        w = dict()
        self.ID_tab = self.genera_random_ID()
        w["id"] = self.ID_tab
        w["type"] = "tab"
        w["label"] = "Flow 1"
        w["disabled"] = False
        w["info"] = ""
        return w
  
    def SubFlow(self, nome) -> dict:
        w = dict()
        self.ID_tab = self.genera_random_ID()
        w["id"] = self.ID_tab
        w["type"] = "subflow"
        w["name"] = nome
        w["info"] = ""
        w["category"] = ""
        w["in"] = []
        w["out"] = []
        w["env"] = []
        w["meta"] = {}
        w["color"] = "#DDAA99"
        return w

    def FLOW_SubFlow(self, id_sublow , id_flow , nome, x, y) -> dict:
        w = dict()
        self.ID_tab = self.genera_random_ID()
        w["id"] = self.ID_tab
        w["type"] = "subflow:" + id_sublow       
        w["z"] = id_flow
        w["name"] = nome
        w["env"] = []
        w["x"] = x
        w["y"] = y
        w["wires"] = []
        return w
        
    def Mqtt_in(self, Z, nome, topic, id_broker, x, y, id_dichie_connesso) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "mqtt in"
        w["z"] = Z #self.ID_tab
        w["name"] = nome
        w["topic"] = topic
        w["qos"] = "1"
        w["datatype"] = "auto"
        w["broker"] = id_broker
        w["x"] = x
        w["y"] = y
        w["wires"] = [[id_dichie_connesso]]
        return w

    def Mqtt_out(self, Z, nome, topic, id_broker, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "mqtt out"
        w["z"] = Z #self.ID_tab
        w["name"] = nome
        w["topic"] = topic
        w["qos"] = "1"
        w["retain"] = "false"
        w["broker"] = id_broker
        w["x"] = x
        w["y"] = y
        w["wires"] = [[]]
        return w
    
    def Mqtt_broker(self) -> dict:
        w = dict()
        self.ID_MQTT_broker = self.genera_random_ID()
        w["id"] = self.ID_MQTT_broker
        w["type"] = "mqtt-broker"
        w["name"] = ""
        w["broker"] = "localhost"
        w["port"] = "1883"
        w["clientid"] = ""
        w["usetls"] = False
        w["compatmode"] = False
        w["keepalive"] = "60"
        w["cleansession"] = True
        w["birthTopic"] = ""
        w["birthQos"] = "0"
        w["birthPayload"] = ""
        w["closeTopic"] = ""
        w["closeQos"] = "0"
        w["closePayload"] = ""
        w["willTopic"] = ""
        w["willQos"] = ""
        w["willPayload"] = ""
        return w
    
    def Debug(self, Z, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "debug"
        w["z"] = Z #self.ID_tab
        w["name"] = ""
        w["active"] = True
        w["tosidebar"] = True
        w["console"] = False
        w["tostatus"] = False
        w["complete"] = "payload"
        w["targetType"] = "msg"
        w["statusVal"] = ""
        w["statusType"] = "auto"
        w["x"] = x
        w["y"] = y
        w["wires"] = []
        return w


    def Aws_iot_device(self, endpoint, pathcertificati) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "aws-iot-device"
        w["name"] = "awsiot"
        w["mode"] = "broker"
        w["clientId"] = "awsiot"
        w["endpoint"] = endpoint
        w["awscerts"] = pathcertificati
        return w

    def Aws_mqtt_in(self, id_aws_iot_device, id_dichie_connesso, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "aws-mqtt in"
        w["z"] = self.ID_tab
        w["device"] = id_aws_iot_device
        w["topic"] = "ESP8266/out"
        w["x"] = x
        w["y"] = y
        w["wires"] = [[id_dichie_connesso]]
        return w
    
    def Aws_mqtt_out(self, id_aws_iot_device, topic, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "aws-mqtt out"
        w["z"] = self.ID_tab
        w["device"] = id_aws_iot_device
        w["topic"] = topic #"ESP8266/in"
        w["qos"] = 0       
        w["x"] = x
        w["y"] = y
        w["wires"] = [[]]
        return w

    def function(self, Z, funct, id_dichie_connesso, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "function"
        w["z"] = Z #self.ID_tab
        w["name"] = ""
        w["func"] = funct #"var value=msg.payload.directive;\n\nif(value === \"TurnOff\"){\nmsg.payload='off';\n}else{\nmsg.payload='on';\n}\n\nreturn msg;"
        w["outputs"] = 1
        w["noerr"] = 0
        w["initialize"] = ""
        w["finalize"] = ""
        w["x"] = x
        w["y"] = y
        w["wires"] = [[id_dichie_connesso]]
        return w

      
    def Comment(self, Z, name, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "comment"
        w["z"] = Z #self.ID_tab
        w["name"] = name
        w["x"] = x
        w["y"] = y
        w["wires"] = []
        return w
        
    
    def y_increment(self):
        self.y = self.y + 70 #80
        return self.y
    

    def y_increment_SWITCH(self):
        self.yswitch= self.yswitch + 60 #70
        return self.yswitch
    def y_increment_DIMMER(self):
        self.ydimmer = self.ydimmer + 60 #80
        return self.ydimmer
    def y_increment_SENSORI_TEMPERATURA(self):
        self.ysensori_temperatura = self.ysensori_temperatura + 60 #80
        return self.ysensori_temperatura
    def y_increment_TERMOSTATI(self):
        self.ytermostati = self.ytermostati + 60 #80
        return self.ytermostati
    def y_increment_SERRANDE_TAPPARELLE(self):
        self.yserrande_tapparelle = self.yserrande_tapparelle + 60 #80
        return self.yserrande_tapparelle
    def y_increment_GRUPPI(self):
        self.ygruppi = self.ygruppi + 60 #80
        return self.ygruppi
    def y_increment_SERRATURE(self):
        self.yserrature = self.yserrature + 60 #80
        return self.yserrature
    def y_increment_CAMPANELLO(self):
        self.ycampanello = self.ycampanello + 60 #80
        return self.ycampanello

    """
    def y_half_increment(self):
        self.y = self.y + 35 #80
        return self.y
    """

    def y_half_increment_SWITCH(self):
        self.y = self.yswitch + 25 #80
        return self.yswitch
    def y_half_increment_DIMMER(self):
        self.y = self.ydimmer + 25 #80
        return self.ydimmer
    def y_half_increment_SENSORI_TEMPERATURA(self):
        self.y = self.ysensori_temperatura + 25 #80
        return self.ysensori_temperatura
    def y_half_increment_TERMOSTATI(self):
        self.y = self.ytermostati + 25 #80
        return self.ytermostati
    def y_half_increment_SERRANDE_TAPPARELLE(self):
        self.y = self.yserrande_tapparelle + 25 #80
        return self.yserrande_tapparelle
    def y_half_increment_GRUPPI(self):
        self.y = self.ygruppi + 25 #80
        return self.ygruppi
    def y_half_increment_SERRATURE(self):
        self.y = self.yserrature + 25 #80
        return self.yserrature        
    def y_half_increment_CAMPANELLO(self):
        self.y = self.ycampanello + 25 #80
        return self.ycampanello

    def genera_random_ID(self) -> str:
        rd = random.Random()
        a = uuid.uuid1(rd.getrandbits(48))
        str_a = str(a)
        val = str(a)[:8] + "." + str(a)[9:12] + str(a)[26:29]
        return val












    def gennera_NodeRed_database(self):
        EndPoint = ''
        if(os.path.isfile('/home/pi/AWSConfig/EndPoint') == True):
            with open('/home/pi/AWSConfig/EndPoint') as fp:
                EndPoint = fp.readline()

        tab = self.Tab()
        broker = self.Mqtt_broker()
        aws_iot_device = self.Aws_iot_device(EndPoint, '/home/pi/AWSConfig')
        buildNode = [tab]

        mqqtout_aws = self.Mqtt_out(tab["id"], 'AWS-OUT', '/scsshield/AWSIOT/out', broker["id"], self.x + 220, self.y )
        aws_mqtt_in = self.Aws_mqtt_in( aws_iot_device['id'] , mqqtout_aws['id'], self.x + 60 , self.y)
        buildNode.append(mqqtout_aws)
        buildNode.append(aws_mqtt_in)

        aws_mqtt_out = self.Aws_mqtt_out( aws_iot_device['id'], "ESP8266/in", self.x + 640, self.y )
        fin = self.function(tab["id"], "msg.topic=\"ESP8266/in\";\n\nreturn msg;", aws_mqtt_out['id'], self.x + 500, self.y)
        in_mqtt = self.Mqtt_in(tab["id"], 'AWS-IN', '/scsshield/AWSIOT/in', broker["id"], self.x + 360, self.y, fin["id"] )
        buildNode.append(aws_mqtt_out)
        buildNode.append(fin)
        buildNode.append(in_mqtt)


        #genera subflow per ogni tipo
        subflow_switch = self.SubFlow("SWITCH")
        subflow_dimmer = self.SubFlow("DIMMER")
        subflow_sensori_temperatura = self.SubFlow("SENSORI_TEMPERATURA")
        subflow_termostati = self.SubFlow("TERMOSTATI")
        subflow_serrande_tapparelle = self.SubFlow("SERRANDE_TAPPARELLE")
        subflow_gruppi = self.SubFlow("GRUPPI")
        subflow_serrature = self.SubFlow("SERRATURE")
        subflow_campanello_porta = self.SubFlow("CAMPANELLO_PORTA")

        #self.y_increment()




        comment0_flag = True
        comment1_flag = True
        comment2_flag = True
        comment3_flag = True
        comment4_flag = True
        comment5_flag = True
        comment6_flag = True
        comment7_flag = True

        query = self.dbm.RICHIESTA_TUTTI_ATTUATORI()
        for q in query:
            if(q['tipo_attuatore'] == 'on_off'):
                if('nome_endpoint' in q):

                    nome_endpoint = q['nome_endpoint']

                    nome = q['nome_attuatore']
                    topicstatus = "/scsshield/device/" + nome + "/status"
                    topiccomando = "/scsshield/device/" + nome + "/switch"

                    #Commento
                    comment0 = self.Comment(subflow_switch["id"], "SWITCH", self.xswich + 10, self.yswitch)
                    if(comment0_flag):
                        self.y_increment_SWITCH() #100 , 110
                    comment1 = self.Comment(subflow_switch["id"], "Alexa, accendi " + nome, self.xswich + 570, self.yswitch)
                    comment2 = self.Comment(subflow_switch["id"], "Alexa, spegni " + nome , self.xswich + 570, self.yswitch+25)

                    #out
                    mqqtout = self.Mqtt_out(subflow_switch["id"], nome, topiccomando, broker["id"], self.xswich + 350, self.yswitch )
                    fout = self.function(subflow_switch["id"], "var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.PowerController\"){\nif(obj.stato.toLowerCase()==='turnon'){\nmsg.payload='on';\nreturn msg;\n}\nif(obj.stato.toLowerCase()==='turnoff'){\nmsg.payload='off';\nreturn msg;\n}\n}\n}\n\n", mqqtout['id'], self.xswich + 140, self.yswitch)
                    in_mqtt = self.Mqtt_in(subflow_switch["id"], 'AWS-OUT', '/scsshield/AWSIOT/out', broker["id"], self.xswich -20, self.yswitch, fout["id"] )

                    self.yswitch = self.yswitch + 30

                    mqqtout2 = self.Mqtt_out(subflow_switch["id"], 'AWS-IN', '/scsshield/AWSIOT/in', broker["id"], self.xswich + 340, self.yswitch )
                    fin = self.function(subflow_switch["id"], "var value=msg.payload.toLowerCase();\n\nif(value===\"on\"){\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"ON\",\n\"tipo\": \"Alexa.PowerController\"\n}\n}else{\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"OFF\",\n\"tipo\":\"Alexa.PowerController\"\n}\n}\nreturn msg;", mqqtout2['id'], self.xswich + 200, self.yswitch)
                    in_mqtt2 = self.Mqtt_in(subflow_switch["id"], nome, topicstatus, broker["id"], self.xswich - 20, self.yswitch, fin["id"] )

                    self.yswitch = self.yswitch + 50

                    if(comment0_flag):
                        buildNode.append(comment0)
                        comment0_flag = False
                    buildNode.append(comment1)
                    buildNode.append(comment2)
                    buildNode.append(mqqtout)
                    buildNode.append(fout)
                    buildNode.append(in_mqtt)
                    buildNode.append(mqqtout2)
                    buildNode.append(fin)
                    buildNode.append(in_mqtt2)
        

            elif(q['tipo_attuatore'] == 'dimmer'):
                if('nome_endpoint' in q):

                    nome_endpoint = q['nome_endpoint']

                    nome = q['nome_attuatore']
                    topicstatus = "/scsshield/device/" + nome + "/status"
                    topiccomando = "/scsshield/device/" + nome + "/dimmer"      #on , off, dimmer%
                    topicstatusPerc = "/scsshield/device/" + nome + "/status/percentuale"

                    #Commento
                    comment0 = self.Comment(subflow_dimmer["id"], "DIMMER", self.xdimmer + 10, self.ydimmer)
                    if(comment1_flag):
                        self.y_increment_DIMMER()
                    comment1 = self.Comment(subflow_dimmer["id"], "Alexa, accendi " + nome, self.xdimmer + 570, self.ydimmer)
                    comment2 = self.Comment(subflow_dimmer["id"], "Alexa, spegni " + nome , self.xdimmer + 570, self.ydimmer + 25)
                    comment3 = self.Comment(subflow_dimmer["id"], "Alexa, imposta " + nome + " 30%", self.xdimmer + 870, self.ydimmer)
                    self.y_increment_DIMMER()

                    #out
                    mqqtout_1 = self.Mqtt_out(subflow_dimmer["id"], nome, topiccomando, broker["id"], self.xdimmer + 510, self.ydimmer)
                    fout_1 = self.function(subflow_dimmer["id"], "var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.PowerController\"){\nif(obj.stato.toLowerCase()==='turnon'){\nmsg.payload='on';\nreturn msg;\n}\nif(obj.stato.toLowerCase()==='turnoff'){\nmsg.payload='off';\nreturn msg;\n}\n}\nif(tipo===\"Alexa.BrightnessController\"){\nif(obj.stato.toLowerCase()==='setbrightness'){\nvar val = parseInt(obj.p);\nmsg.payload=val;\nreturn msg;\n}\n}\n}\n\n", mqqtout_1['id'], self.xdimmer + 230, self.ydimmer )
                    in_mqtt_1 = self.Mqtt_in(subflow_dimmer["id"], 'AWS-OUT', "/scsshield/AWSIOT/out", broker["id"], self.xdimmer + 30, self.ydimmer, fout_1["id"] )
                    self.y_half_increment_DIMMER()
                    mqqtout_2 = self.Mqtt_out(subflow_dimmer["id"], 'AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.xdimmer + 510, self.ydimmer)
                    fout_2 = self.function(subflow_dimmer["id"], "var value=msg.payload.toLowerCase();\n\nif(value===\"on\"){\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"ON\",\n\"tipo\": \"Alexa.PowerController\"\n}\n}else{\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"OFF\",\n\"tipo\":\"Alexa.PowerController\"\n}\n}\nreturn msg;", mqqtout_2['id'], self.xdimmer + 330, self.ydimmer )
                    in_mqtt_2 = self.Mqtt_in(subflow_dimmer["id"], nome, topicstatus, broker["id"], self.xdimmer + 60, self.ydimmer, fout_2["id"] )
                    self.y_half_increment_DIMMER()
                    mqqtout_3 = self.Mqtt_out(subflow_dimmer["id"], 'AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.xdimmer + 510, self.ydimmer)
                    fout_3 = self.function(subflow_dimmer["id"], "var value=msg.payload.toLowerCase();\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "_S\",\n\"stato\": value.toString(),\n\"tipo\": \"Alexa.BrightnessController\"\n}\n\nreturn msg;", mqqtout_3['id'], self.xdimmer + 330, self.ydimmer )
                    in_mqtt_3 = self.Mqtt_in(subflow_dimmer["id"], nome + '-percentuale', topicstatusPerc, broker["id"], self.xdimmer + 60, self.ydimmer, fout_3["id"] )


                    self.y_increment_DIMMER()

                    if(comment1_flag):
                        buildNode.append(comment0)
                        comment1_flag = False
                    buildNode.append(comment1)
                    buildNode.append(comment2)
                    buildNode.append(comment3)                
                    buildNode.append(mqqtout_1)
                    buildNode.append(fout_1)
                    buildNode.append(in_mqtt_1)  
                    buildNode.append(mqqtout_2)
                    buildNode.append(fout_2)
                    buildNode.append(in_mqtt_2)
                    buildNode.append(mqqtout_3)
                    buildNode.append(fout_3)
                    buildNode.append(in_mqtt_3)


            elif(q['tipo_attuatore'] == 'serrande_tapparelle'):
                if('nome_endpoint' in q):

                    nome_endpoint = q['nome_endpoint']

                    nome = q['nome_attuatore']
                    topicstatus = "/scsshield/device/" + nome + "/status"       
                    topiccomando = "/scsshield/device/" + nome + "/percentuale" 

                    #Commento
                    comment0 = self.Comment(subflow_serrande_tapparelle["id"], "SERRANDE/TAPPARELLE", self.xserrande_tapparelle + 10, self.yserrande_tapparelle)
                    if(comment4_flag):
                        self.y_increment_SERRANDE_TAPPARELLE()
                    comment1 = self.Comment(subflow_serrande_tapparelle["id"], "Alexa, imposta le persiane " + nome + " al cinquanta percento" , self.xserrande_tapparelle + 570, self.yserrande_tapparelle)
                    comment2 = self.Comment(subflow_serrande_tapparelle["id"], "Alexa, apri " + nome , self.xserrande_tapparelle + 570, self.yserrande_tapparelle+25)
                    comment3 = self.Comment(subflow_serrande_tapparelle["id"], "Alexa, chiudi " + nome , self.xserrande_tapparelle + 870, self.yserrande_tapparelle)
                    self.y_increment_SERRANDE_TAPPARELLE()

                    #out
                    mqqtout_1 = self.Mqtt_out(subflow_serrande_tapparelle["id"], nome, topiccomando, broker["id"], self.xserrande_tapparelle + 510, self.yserrande_tapparelle)
                    fout_1 = self.function(subflow_serrande_tapparelle["id"], "var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.RangeController\"){\nvar val = parseInt(obj.stato);\n\nmsg.payload=val;\nreturn msg;\n\n}\n}\n\n", mqqtout_1['id'], self.xserrande_tapparelle + 230, self.yserrande_tapparelle )
                    in_mqtt_1 = self.Mqtt_in(subflow_serrande_tapparelle["id"], 'AWS-OUT', "/scsshield/AWSIOT/out", broker["id"], self.xserrande_tapparelle + 30, self.yserrande_tapparelle, fout_1["id"] )
                    self.y_half_increment_SERRANDE_TAPPARELLE()
                    mqqtout_2 = self.Mqtt_out(subflow_serrande_tapparelle["id"], 'AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.xserrande_tapparelle + 510, self.yserrande_tapparelle)
                    fout_2 = self.function(subflow_serrande_tapparelle["id"], "var value=msg.payload.toLowerCase();\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": value.toString(),\n\"tipo\": \"Alexa.RangeController\"\n}\n\nreturn msg;", mqqtout_2['id'], self.xserrande_tapparelle + 330, self.yserrande_tapparelle )
                    in_mqtt_2 = self.Mqtt_in(subflow_serrande_tapparelle["id"], nome, topicstatus, broker["id"], self.xserrande_tapparelle + 60, self.yserrande_tapparelle, fout_2["id"] )

                    self.y_increment_SERRANDE_TAPPARELLE()

                    if(comment4_flag):
                        buildNode.append(comment0)
                        comment4_flag = False
                    buildNode.append(comment1)
                    buildNode.append(comment2)
                    buildNode.append(comment3)              
                    buildNode.append(mqqtout_1)
                    buildNode.append(fout_1)
                    buildNode.append(in_mqtt_1)
                    buildNode.append(mqqtout_2)
                    buildNode.append(fout_2)
                    buildNode.append(in_mqtt_2)


            elif(q['tipo_attuatore'] == 'sensori_temperatura'):
                if('nome_endpoint' in q):

                    nome_endpoint = q['nome_endpoint']

                    nome = q['nome_attuatore']
                    topicstatus = "/scsshield/device/" + nome + "/status"

                    #Commento
                    comment0 = self.Comment(subflow_sensori_temperatura["id"], "SENSORE TEMPERATURA", self.xsensori_temperatura + 73, self.ysensori_temperatura)
                    if(comment2_flag):
                        self.y_increment_SENSORI_TEMPERATURA()
                    comment1 = self.Comment(subflow_sensori_temperatura["id"], "Alexa, qual è la temperatura del " + nome, self.xsensori_temperatura + 155, self.ysensori_temperatura)
                    self.y_increment_SENSORI_TEMPERATURA()

                    #out
                    mqqtout_2 = self.Mqtt_out(subflow_sensori_temperatura["id"], 'AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.xsensori_temperatura + 510, self.ysensori_temperatura)
                    fout_2 = self.function(subflow_sensori_temperatura["id"], "var value=msg.payload.toLowerCase();\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": value.toString(),\n\"tipo\": \"Alexa.TemperatureSensor\"\n}\n\nreturn msg;", mqqtout_2['id'], self.xsensori_temperatura + 330, self.ysensori_temperatura )
                    in_mqtt_2 = self.Mqtt_in(subflow_sensori_temperatura["id"], nome, topicstatus, broker["id"], self.xsensori_temperatura + 60, self.ysensori_temperatura, fout_2["id"] )

                    self.y_increment_SENSORI_TEMPERATURA()

                    if(comment2_flag):
                        buildNode.append(comment0)
                        comment2_flag = False
                    buildNode.append(comment1)
                    buildNode.append(mqqtout_2)
                    buildNode.append(fout_2)
                    buildNode.append(in_mqtt_2)


            elif(q['tipo_attuatore'] == 'termostati'):
                if('nome_endpoint' in q):

                    nome_endpoint = q['nome_endpoint']

                    nome = q['nome_attuatore']
                    topicstatus = "/scsshield/device/" + nome + "/status"       #temperatura ambiente misurata
                    topicTemp_Termostato = "/scsshield/device/" + nome + "/temperatura_termostato_impostata" #temperatura ambiente misurata
                    topiccomando = "/scsshield/device/" + nome + "/set_temp_termostato"      #set temp termostato
                    topiccomandomod = "/scsshield/device/" + nome + "/set_modalita_termostato"      #set modalita termostato
                    topicstatusmod = "/scsshield/device/" + nome + "/modalita_termostato_impostata"      #set modalita termostato

                    #Commento
                    comment0 = self.Comment(subflow_termostati["id"], "TERMOSTATO", self.xtermostati + 30, self.ytermostati)
                    if(comment3_flag):
                        self.y_increment_TERMOSTATI()
                    comment1 = self.Comment(subflow_termostati["id"], "Alexa, imposta la temperatura del " + nome + " a 20°" , self.xtermostati + 570, self.ytermostati)
                    comment2 = self.Comment(subflow_termostati["id"], "Alexa, qual è la temperatura del " + nome, self.xtermostati + 190, self.ytermostati)
                    comment3 = self.Comment(subflow_termostati["id"], "Alexa, imposta il " + nome + " su CALDO" , self.xtermostati + 570, self.ytermostati)
                    comment4 = self.Comment(subflow_termostati["id"], "Alexa, imposta il " + nome + " su FREDDO" , self.xtermostati + 950, self.ytermostati)
                    comment5 = self.Comment(subflow_termostati["id"], "Alexa, imposta il " + nome + " su OFF" , self.xtermostati + 1330, self.ytermostati)
                    self.y_increment_TERMOSTATI()

                    #out
                    mqqtout_1 = self.Mqtt_out(subflow_termostati["id"], nome, topiccomando, broker["id"], self.xtermostati + 510, self.ytermostati)
                    fout_1 = self.function(subflow_termostati["id"], "var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.ThermostatController\"){\nif(obj.stato.toLowerCase()==='temp'){\nvar val = parseFloat(obj.t);\nmsg.payload=val;\nreturn msg;\n}\n}\n}\n\n", mqqtout_1['id'], self.xtermostati + 230, self.ytermostati )
                    in_mqtt_1 = self.Mqtt_in(subflow_termostati["id"], 'AWS-OUT', "/scsshield/AWSIOT/out", broker["id"], self.xtermostati + 30, self.ytermostati, fout_1["id"] )
                    self.y_half_increment_TERMOSTATI()
                    mqqtout_2 = self.Mqtt_out(subflow_termostati["id"], nome, topiccomandomod, broker["id"], self.xtermostati + 510, self.ytermostati)
                    fout_2 = self.function(subflow_termostati["id"], "var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.ThermostatController\"){\nif(obj.stato.toLowerCase()==='mode'){\nvar val = obj.m;\nif(val === 'O'){\nmsg.payload='off';\nreturn msg;\n}else if(val === 'H'){\nmsg.payload='inverno';\nreturn msg;\n}else if(val === 'C'){\nmsg.payload='estate';\nreturn msg;\n}\n}\n}\n}\n\n", mqqtout_2['id'], self.xtermostati + 230, self.ytermostati )
                    in_mqtt_2 = self.Mqtt_in(subflow_termostati["id"], 'AWS-OUT', "/scsshield/AWSIOT/out", broker["id"], self.xtermostati + 30, self.ytermostati, fout_2["id"] )
                    self.y_half_increment_TERMOSTATI()
                    mqqtout_3 = self.Mqtt_out(subflow_termostati["id"], 'AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.xtermostati + 510, self.ytermostati)
                    fout_3 = self.function(subflow_termostati["id"], "var value=msg.payload.toLowerCase();\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\" + \"_T\",\n\"stato\": value.toString(),\n\"tipo\": \"Alexa.ThermostatController\"\n}\n\nreturn msg;", mqqtout_3['id'], self.xtermostati + 330, self.ytermostati )
                    in_mqtt_3 = self.Mqtt_in(subflow_termostati["id"], nome, topicstatus, broker["id"], self.xtermostati + 60, self.ytermostati, fout_3["id"] )
                    self.y_half_increment_TERMOSTATI()
                    mqqtout_4 = self.Mqtt_out(subflow_termostati["id"], 'AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.xtermostati + 510, self.ytermostati)
                    fout_4 = self.function(subflow_termostati["id"], "var value=msg.payload.toLowerCase();\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\" + \"_S\",\n\"stato\": value.toString(),\n\"tipo\": \"Alexa.ThermostatController\"\n}\n\nreturn msg;", mqqtout_4['id'], self.xtermostati + 330, self.ytermostati )
                    in_mqtt_4 = self.Mqtt_in(subflow_termostati["id"], nome, topicTemp_Termostato, broker["id"], self.xtermostati + 60, self.ytermostati, fout_4["id"] )
                    self.y_half_increment_TERMOSTATI()
                    mqqtout_5 = self.Mqtt_out(subflow_termostati["id"], 'AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.xtermostati + 510, self.ytermostati)
                    fout_5 = self.function(subflow_termostati["id"], "var value=msg.payload.toLowerCase();\n\nvar m=\"\";\n\nif(value === 'off'){\nm=\"5\";\n}else if(value === 'estate'){\nm=\"3\";\n}else if(value === 'inverno'){\nm=\"4\";\n}\n\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\" + \"_M\",\n\"stato\": m,\n\"tipo\": \"Alexa.ThermostatController\"\n}\n\nreturn msg;", mqqtout_5['id'], self.xtermostati + 330, self.ytermostati )
                    in_mqtt_5 = self.Mqtt_in(subflow_termostati["id"], nome, topicstatusmod, broker["id"], self.xtermostati + 60, self.ytermostati, fout_5["id"] )


                    self.y_increment()

                    if(comment3_flag):
                        buildNode.append(comment0)
                        comment3_flag = False
                    buildNode.append(comment1)
                    buildNode.append(comment2)
                    buildNode.append(comment3)
                    buildNode.append(comment4)
                    buildNode.append(comment5)                   
                    buildNode.append(mqqtout_1)
                    buildNode.append(fout_1)
                    buildNode.append(in_mqtt_1)
                    buildNode.append(mqqtout_2)
                    buildNode.append(fout_2)
                    buildNode.append(in_mqtt_2)
                    buildNode.append(mqqtout_3)
                    buildNode.append(fout_3)
                    buildNode.append(in_mqtt_3)
                    buildNode.append(mqqtout_4)
                    buildNode.append(fout_4)
                    buildNode.append(in_mqtt_4)
                    buildNode.append(mqqtout_5)
                    buildNode.append(fout_5)
                    buildNode.append(in_mqtt_5)


            elif(q['tipo_attuatore'] == 'campanello_porta'):
                if('nome_endpoint' in q):

                    nome_endpoint = q['nome_endpoint']

                    nome = q['nome_attuatore']
                    topicstatus = "/scsshield/device/" + nome + "/status"

                    #Commento
                    comment0 = self.Comment(subflow_campanello_porta["id"], "CAMPANELLO", self.xcampanello + 30, self.ycampanello)
                    if(comment6_flag):
                        self.y_increment_CAMPANELLO()

                    aws_mqtt_outcamp = self.Aws_mqtt_out( aws_iot_device['id'], "ESP8266/out/event", self.xcampanello + 480, self.ycampanello )
                    fout_1 = self.function(subflow_campanello_porta["id"], "var value=msg.payload.toLowerCase();\n\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"PHYSICAL_INTERACTION\"\n}\nmsg.topic = \"ESP8266/out/event\"\nreturn msg;", aws_mqtt_outcamp['id'], self.xcampanello + 310, self.ycampanello )
                    in_mqtt_1 = self.Mqtt_in(subflow_campanello_porta["id"], nome, topicstatus, broker["id"], self.xcampanello + 60, self.ycampanello, fout_1["id"] )

                    self.y_increment_CAMPANELLO()

                    if(comment6_flag):
                        buildNode.append(comment0)
                        comment6_flag = False

                    buildNode.append(aws_mqtt_outcamp)
                    buildNode.append(fout_1)
                    buildNode.append(in_mqtt_1)


            elif(q['tipo_attuatore'] == 'serrature'):
                if('nome_endpoint' in q):

                    nome_endpoint = q['nome_endpoint']

                    nome = q['nome_attuatore']
                    topiccomando = "/scsshield/device/" + nome + "/sblocca"

                    #Commento
                    comment0 = self.Comment(subflow_serrature["id"], "SERRATURE", self.xserrature + 10, self.yserrature)
                    if(comment7_flag):
                        self.y_increment_SERRATURE()

                    mqqtout_1 = self.Mqtt_out(subflow_serrature["id"], nome, topiccomando, broker["id"], self.xserrature + 510, self.yserrature)
                    fout_1 = self.function(subflow_serrature["id"], "var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.LockController\"){\nif(obj.stato.toLowerCase()==='unlock'){\n\nmsg.payload=\"sblocca\";\nreturn msg;\n}\n}\n}\n\n", mqqtout_1['id'], self.xserrature + 230, self.yserrature )
                    in_mqtt_1 = self.Mqtt_in(subflow_serrature["id"], 'AWS-OUT', "/scsshield/AWSIOT/out", broker["id"], self.xserrature + 30, self.yserrature, fout_1["id"] )

                    self.y_increment_SERRATURE()

                    if(comment7_flag):
                        buildNode.append(comment0)
                        comment7_flag = False

                    buildNode.append(mqqtout_1)
                    buildNode.append(fout_1)
                    buildNode.append(in_mqtt_1)


            elif(q['tipo_attuatore'] == 'gruppi'):
                if('nome_endpoint' in q):

                    nome_endpoint = q['nome_endpoint']

                    nome = q['nome_attuatore']
                    topicstatus = "/scsshield/device/" + nome + "/status"
                    topiccomando = "/scsshield/device/" + nome + "/switch"

                    #Commento
                    comment0 = self.Comment(subflow_gruppi["id"], "GRUPPI", self.xgruppi + 10, self.ygruppi)
                    if(comment5_flag):
                        self.y_increment_GRUPPI()
                    comment1 = self.Comment(subflow_gruppi["id"], "Alexa, accendi " + nome, self.xgruppi + 570, self.ygruppi)
                    comment2 = self.Comment(subflow_gruppi["id"], "Alexa, spegni " + nome , self.xgruppi + 570, self.ygruppi+25)
                    self.y_increment_GRUPPI()

                    #out

                    #out
                    mqqtout = self.Mqtt_out(subflow_gruppi["id"], nome, topiccomando, broker["id"], self.xgruppi + 500, self.ygruppi )
                    fout = self.function(subflow_gruppi["id"], "var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.PowerController\"){\nif(obj.stato.toLowerCase()==='turnon'){\nmsg.payload='on';\nreturn msg;\n}\nif(obj.stato.toLowerCase()==='turnoff'){\nmsg.payload='off';\nreturn msg;\n}\n}\n}\n\n", mqqtout['id'], self.xgruppi + 250, self.ygruppi)
                    in_mqtt = self.Mqtt_in(subflow_gruppi["id"], 'AWS-OUT', '/scsshield/AWSIOT/out', broker["id"], self.xgruppi + 10, self.ygruppi, fout["id"] )

                    self.y_half_increment_GRUPPI()

                    mqqtout2 = self.Mqtt_out(subflow_gruppi["id"], 'AWS-IN', '/scsshield/AWSIOT/in', broker["id"], self.xgruppi + 490, self.ygruppi )
                    fin = self.function(subflow_gruppi["id"], "var value=msg.payload.toLowerCase();\n\nif(value===\"on\"){\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"ON\",\n\"tipo\": \"Alexa.PowerController\"\n}\n}else{\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"OFF\",\n\"tipo\":\"Alexa.PowerController\"\n}\n}\nreturn msg;", mqqtout2['id'], self.xgruppi + 310, self.ygruppi)
                    in_mqtt2 = self.Mqtt_in(subflow_gruppi["id"], nome, topicstatus, broker["id"], self.xgruppi + 70, self.ygruppi, fin["id"] )

                    self.y_increment_GRUPPI()

                    if(comment5_flag):
                        buildNode.append(comment0)
                        comment5_flag = False
                    buildNode.append(comment1)
                    buildNode.append(comment2)
                    buildNode.append(mqqtout)
                    buildNode.append(fout)
                    buildNode.append(in_mqtt)
                    buildNode.append(mqqtout2)
                    buildNode.append(fin)
                    buildNode.append(in_mqtt2)





        #append subflow in FLOW
        switch_FLOW_SubFlow = self.FLOW_SubFlow(subflow_switch["id"], tab["id"], "SWITCH", 120, 100)
        dimmer_FLOW_SubFlow = self.FLOW_SubFlow(subflow_dimmer["id"], tab["id"], "DIMMER", 120, 140)
        sensori_temperatura_FLOW_SubFlow = self.FLOW_SubFlow(subflow_sensori_temperatura["id"], tab["id"], "SENSORI_TEMPERATURA", 180, 180)
        termostati_FLOW_SubFlow = self.FLOW_SubFlow(subflow_termostati["id"], tab["id"], "TERMOSTATI", 130, 220)
        serrande_tapparelle_FLOW_SubFlow = self.FLOW_SubFlow(subflow_serrande_tapparelle["id"], tab["id"], "SERRANDE_TAPPARELLE", 180, 260)
        gruppii_FLOW_SubFlow = self.FLOW_SubFlow(subflow_gruppi["id"], tab["id"], "GRUPPI", 120, 380)
        serrature_FLOW_SubFlow = self.FLOW_SubFlow(subflow_serrature["id"], tab["id"], "SERRATURE", 130, 340)
        campanello_FLOW_SubFlow = self.FLOW_SubFlow(subflow_campanello_porta["id"], tab["id"], "CAMPANELLO", 140, 300)

        buildNode.append(subflow_switch)
        buildNode.append(subflow_dimmer)
        buildNode.append(subflow_sensori_temperatura)
        buildNode.append(subflow_termostati)
        buildNode.append(subflow_serrande_tapparelle)
        buildNode.append(subflow_gruppi)
        buildNode.append(subflow_serrature)
        buildNode.append(subflow_campanello_porta)

        buildNode.append(switch_FLOW_SubFlow)        
        buildNode.append(dimmer_FLOW_SubFlow)
        buildNode.append(sensori_temperatura_FLOW_SubFlow)
        buildNode.append(termostati_FLOW_SubFlow)
        buildNode.append(serrande_tapparelle_FLOW_SubFlow)
        buildNode.append(gruppii_FLOW_SubFlow)
        buildNode.append(serrature_FLOW_SubFlow)
        buildNode.append(campanello_FLOW_SubFlow)
        

        buildNode.append(aws_iot_device)
        buildNode.append(broker)
        return json.dumps(buildNode)




"""
    def main(self):
        print("main nodered esecute")
        node = nodered()
        js = node.gennera_NodeRed_database()
        
        print(os.popen("sudo node-red-stop").read() )

        with open('/home/pi/.node-red/flows_raspberrypi.json', 'w') as jsonfile:
            jsonfile.write(js)
        #print(os.popen("sudo node-red-start").read())

        process = subprocess.Popen(['node-red-start'],
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
        
        print(process)
        
        
        process = subprocess.Popen(['systemctl', 'status nodered.service'],
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)                        
        
        print(process)
"""    


if __name__ == "__main__":    
    print("*****node red AWS library*****")
    
    node = noderedAWS()
    #print ( node.genera())
    js = node.gennera_NodeRed_database()
    print(js)
    
    
    