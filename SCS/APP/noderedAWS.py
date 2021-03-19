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
  

    def Mqtt_in(self, nome, topic, id_broker, x, y, id_dichie_connesso) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "mqtt in"
        w["z"] = self.ID_tab
        w["name"] = nome
        w["topic"] = topic
        w["qos"] = "1"
        w["datatype"] = "auto"
        w["broker"] = id_broker
        w["x"] = x
        w["y"] = y
        w["wires"] = [[id_dichie_connesso]]
        return w

    def Mqtt_out(self, nome, topic, id_broker, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "mqtt out"
        w["z"] = self.ID_tab
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
    
    def Debug(self, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "debug"
        w["z"] = self.ID_tab
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

    def function(self, funct, id_dichie_connesso, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "function"
        w["z"] = self.ID_tab
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

      
    def Comment(self, name, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "comment"
        w["z"] = self.ID_tab
        w["name"] = name
        w["x"] = x
        w["y"] = y
        w["wires"] = []
        return w
        

    def y_increment(self):
        self.y = self.y + 70 #80
        return self.y
    def y_half_increment(self):
        self.y = self.y + 35 #80
        return self.y



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

        mqqtout_aws = self.Mqtt_out('AWS-OUT', '/scsshield/AWSIOT/out', broker["id"], self.x + 220, self.y )
        aws_mqtt_in = self.Aws_mqtt_in( aws_iot_device['id'] , mqqtout_aws['id'], self.x + 60 , self.y)
        buildNode.append(mqqtout_aws)
        buildNode.append(aws_mqtt_in)

        aws_mqtt_out = self.Aws_mqtt_out( aws_iot_device['id'], "ESP8266/in", self.x + 640, self.y )
        fin = self.function("msg.topic=\"ESP8266/in\";\n\nreturn msg;", aws_mqtt_out['id'], self.x + 500, self.y)
        in_mqtt = self.Mqtt_in('AWS-IN', '/scsshield/AWSIOT/in', broker["id"], self.x + 360, self.y, fin["id"] )
        buildNode.append(aws_mqtt_out)
        buildNode.append(fin)
        buildNode.append(in_mqtt)

        self.y_increment()




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
                    comment0 = self.Comment("SWITCH", self.x + 10, self.y)
                    if(comment0_flag):
                        self.y_increment()
                    comment1 = self.Comment("Alexa, accendi " + nome, self.x + 100, self.y)
                    comment2 = self.Comment("Alexa, spegni " + nome , self.x + 390, self.y)
                    self.y_increment()

                    #out
                    mqqtout = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 500, self.y )
                    fout = self.function("var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.PowerController\"){\nif(obj.stato.toLowerCase()==='turnon'){\nmsg.payload='on';\nreturn msg;\n}\nif(obj.stato.toLowerCase()==='turnoff'){\nmsg.payload='off';\nreturn msg;\n}\n}\n}\n\n", mqqtout['id'], self.x + 250, self.y)
                    in_mqtt = self.Mqtt_in('AWS-OUT', '/scsshield/AWSIOT/out', broker["id"], self.x + 10, self.y, fout["id"] )

                    self.y_half_increment()

                    mqqtout2 = self.Mqtt_out('AWS-IN', '/scsshield/AWSIOT/in', broker["id"], self.x + 490, self.y )
                    fin = self.function("var value=msg.payload.toLowerCase();\n\nif(value===\"on\"){\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"ON\",\n\"tipo\": \"Alexa.PowerController\"\n}\n}else{\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"OFF\",\n\"tipo\":\"Alexa.PowerController\"\n}\n}\nreturn msg;", mqqtout2['id'], self.x + 310, self.y)
                    in_mqtt2 = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 70, self.y, fin["id"] )

                    self.y_increment()

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
                    comment0 = self.Comment("DIMMER", self.x + 10, self.y)
                    if(comment1_flag):
                        self.y_increment()
                    comment1 = self.Comment("Alexa, accendi " + nome, self.x + 100, self.y)
                    comment2 = self.Comment("Alexa, spegni " + nome , self.x + 390, self.y)
                    comment3 = self.Comment("Alexa, imposta " + nome + " 30%", self.x + 670, self.y)
                    self.y_increment()

                    #out
                    mqqtout_1 = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 510, self.y)
                    fout_1 = self.function("var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.PowerController\"){\nif(obj.stato.toLowerCase()==='turnon'){\nmsg.payload='on';\nreturn msg;\n}\nif(obj.stato.toLowerCase()==='turnoff'){\nmsg.payload='off';\nreturn msg;\n}\n}\nif(tipo===\"Alexa.BrightnessController\"){\nif(obj.stato.toLowerCase()==='setbrightness'){\nvar val = parseInt(obj.p);\nmsg.payload=val;\nreturn msg;\n}\n}\n}\n\n", mqqtout_1['id'], self.x + 230, self.y )
                    in_mqtt_1 = self.Mqtt_in('AWS-OUT', "/scsshield/AWSIOT/out", broker["id"], self.x + 30, self.y, fout_1["id"] )
                    self.y_half_increment()
                    mqqtout_2 = self.Mqtt_out('AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.x + 510, self.y)
                    fout_2 = self.function("var value=msg.payload.toLowerCase();\n\nif(value===\"on\"){\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"ON\",\n\"tipo\": \"Alexa.PowerController\"\n}\n}else{\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"OFF\",\n\"tipo\":\"Alexa.PowerController\"\n}\n}\nreturn msg;", mqqtout_2['id'], self.x + 330, self.y )
                    in_mqtt_2 = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 60, self.y, fout_2["id"] )
                    self.y_half_increment()
                    mqqtout_3 = self.Mqtt_out('AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.x + 510, self.y)
                    fout_3 = self.function("var value=msg.payload.toLowerCase();\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": value.toString(),\n\"tipo\": \"Alexa.BrightnessController\"\n}\n\nreturn msg;", mqqtout_3['id'], self.x + 330, self.y )
                    in_mqtt_3 = self.Mqtt_in(nome + '-percentuale', topicstatusPerc, broker["id"], self.x + 60, self.y, fout_3["id"] )


                    self.y_increment()

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
                    comment0 = self.Comment("SERRANDE/TAPPARELLE", self.x + 60, self.y)
                    if(comment4_flag):
                        self.y_increment()
                    comment1 = self.Comment("Alexa, imposta le persiane " + nome + " al cinquanta percento" , self.x + 195, self.y)
                    comment2 = self.Comment("Alexa, apri " + nome , self.x + 350, self.y)
                    comment3 = self.Comment("Alexa, chiudi " + nome , self.x + 590, self.y)
                    self.y_increment()

                    #out
                    mqqtout_1 = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 510, self.y)
                    fout_1 = self.function("var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.RangeController\"){\nvar val = parseInt(obj.stato);\n\nmsg.payload=val;\nreturn msg;\n\n}\n}\n\n", mqqtout_1['id'], self.x + 230, self.y )
                    in_mqtt_1 = self.Mqtt_in('AWS-OUT', "/scsshield/AWSIOT/out", broker["id"], self.x + 30, self.y, fout_1["id"] )
                    self.y_half_increment()
                    mqqtout_2 = self.Mqtt_out('AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.x + 510, self.y)
                    fout_2 = self.function("var value=msg.payload.toLowerCase();\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": value.toString(),\n\"tipo\": \"Alexa.RangeController\"\n}\n\nreturn msg;", mqqtout_2['id'], self.x + 330, self.y )
                    in_mqtt_2 = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 60, self.y, fout_2["id"] )

                    self.y_increment()

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
                    comment0 = self.Comment("SENSORE TEMPERATURA", self.x + 73, self.y)
                    if(comment2_flag):
                        self.y_increment()
                    comment1 = self.Comment("Alexa, qual è la temperatura del " + nome, self.x + 155, self.y)
                    self.y_increment()

                    #out
                    mqqtout_2 = self.Mqtt_out('AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.x + 510, self.y)
                    fout_2 = self.function("var value=msg.payload.toLowerCase();\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": value.toString(),\n\"tipo\": \"Alexa.TemperatureSensor\"\n}\n\nreturn msg;", mqqtout_2['id'], self.x + 330, self.y )
                    in_mqtt_2 = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 60, self.y, fout_2["id"] )

                    self.y_increment()

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
                    comment0 = self.Comment("TERMOSTATO", self.x + 30, self.y)
                    if(comment3_flag):
                        self.y_increment()
                    comment1 = self.Comment("Alexa, imposta la temperatura del " + nome + " a 20°" , self.x + 570, self.y)
                    comment2 = self.Comment("Alexa, qual è la temperatura del " + nome, self.x + 190, self.y)
                    comment3 = self.Comment("Alexa, imposta il " + nome + " su CALDO" , self.x + 570, self.y)
                    comment4 = self.Comment("Alexa, imposta il " + nome + " su FREDDO" , self.x + 950, self.y)
                    comment5 = self.Comment("Alexa, imposta il " + nome + " su OFF" , self.x + 1330, self.y)
                    self.y_increment()

                    #out
                    mqqtout_1 = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 510, self.y)
                    fout_1 = self.function("var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.ThermostatController\"){\nif(obj.stato.toLowerCase()==='temp'){\nvar val = parseFloat(obj.t);\nmsg.payload=val;\nreturn msg;\n}\n}\n}\n\n", mqqtout_1['id'], self.x + 230, self.y )
                    in_mqtt_1 = self.Mqtt_in('AWS-OUT', "/scsshield/AWSIOT/out", broker["id"], self.x + 30, self.y, fout_1["id"] )
                    self.y_half_increment()
                    mqqtout_2 = self.Mqtt_out(nome, topiccomandomod, broker["id"], self.x + 510, self.y)
                    fout_2 = self.function("var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.ThermostatController\"){\nif(obj.stato.toLowerCase()==='mode'){\nvar val = obj.m;\nif(val === 'O'){\nmsg.payload='off';\nreturn msg;\n}else if(val === 'H'){\nmsg.payload='inverno';\nreturn msg;\n}else if(val === 'C'){\nmsg.payload='estate';\nreturn msg;\n}\n}\n}\n}\n\n", mqqtout_2['id'], self.x + 230, self.y )
                    in_mqtt_2 = self.Mqtt_in('AWS-OUT', "/scsshield/AWSIOT/out", broker["id"], self.x + 30, self.y, fout_2["id"] )
                    self.y_half_increment()
                    mqqtout_3 = self.Mqtt_out('AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.x + 510, self.y)
                    fout_3 = self.function("var value=msg.payload.toLowerCase();\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\" + \"_T\",\n\"stato\": value.toString(),\n\"tipo\": \"Alexa.ThermostatController\"\n}\n\nreturn msg;", mqqtout_3['id'], self.x + 330, self.y )
                    in_mqtt_3 = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 60, self.y, fout_3["id"] )
                    self.y_half_increment()
                    mqqtout_4 = self.Mqtt_out('AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.x + 510, self.y)
                    fout_4 = self.function("var value=msg.payload.toLowerCase();\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\" + \"_S\",\n\"stato\": value.toString(),\n\"tipo\": \"Alexa.ThermostatController\"\n}\n\nreturn msg;", mqqtout_4['id'], self.x + 330, self.y )
                    in_mqtt_4 = self.Mqtt_in(nome, topicTemp_Termostato, broker["id"], self.x + 60, self.y, fout_4["id"] )
                    self.y_half_increment()
                    mqqtout_5 = self.Mqtt_out('AWS-IN', "/scsshield/AWSIOT/in", broker["id"], self.x + 510, self.y)
                    fout_5 = self.function("var value=msg.payload.toLowerCase();\n\nvar m=\"\";\n\nif(value === 'off'){\nm=\"5\";\n}else if(value === 'inverno'){\nm=\"3\";\n}else if(value === 'estate'){\nm=\"4\";\n}\n\n\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\" + \"_M\",\n\"stato\": m,\n\"tipo\": \"Alexa.ThermostatController\"\n}\n\nreturn msg;", mqqtout_5['id'], self.x + 330, self.y )
                    in_mqtt_5 = self.Mqtt_in(nome, topicstatusmod, broker["id"], self.x + 60, self.y, fout_5["id"] )


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
                    comment0 = self.Comment("CAMPANELLO", self.x + 30, self.y)
                    if(comment6_flag):
                        self.y_increment()

                    aws_mqtt_outcamp = self.Aws_mqtt_out( aws_iot_device['id'], "ESP8266/out/event", self.x + 480, self.y )
                    fout_1 = self.function("var value=msg.payload.toLowerCase();\n\n\nmsg.payload={\n\"id\": \"doorbell-01\",\n\"stato\": \"PHYSICAL_INTERACTION\"\n}\nmsg.topic = \"ESP8266/out/event\"\nreturn msg;", aws_mqtt_outcamp['id'], self.x + 310, self.y )
                    in_mqtt_1 = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 60, self.y, fout_1["id"] )

                    self.y_increment()

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
                    comment0 = self.Comment("SERRATURE", self.x + 30, self.y)
                    if(comment7_flag):
                        self.y_increment()

                    mqqtout_1 = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 510, self.y)
                    fout_1 = self.function("var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.LockController\"){\nif(obj.stato.toLowerCase()==='unlock'){\n\nmsg.payload=\"sblocca\";\nreturn msg;\n}\n}\n}\n\n", mqqtout_1['id'], self.x + 230, self.y )
                    in_mqtt_1 = self.Mqtt_in('AWS-OUT', "/scsshield/AWSIOT/out", broker["id"], self.x + 30, self.y, fout_1["id"] )

                    self.y_increment()

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
                    comment0 = self.Comment("GRUPPI", self.x + 10, self.y)
                    if(comment5_flag):
                        self.y_increment()
                    comment1 = self.Comment("Alexa, accendi " + nome, self.x + 100, self.y)
                    comment2 = self.Comment("Alexa, spegni " + nome , self.x + 390, self.y)
                    self.y_increment()

                    #out

                    #out
                    mqqtout = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 500, self.y )
                    fout = self.function("var obj=JSON.parse(msg.payload);\n\nvar tipo=obj.tipo;\nvar identificativo=obj.identificativo;\n\n\nif(identificativo===\"" + nome_endpoint + "\"){\nif(tipo===\"Alexa.PowerController\"){\nif(obj.stato.toLowerCase()==='turnon'){\nmsg.payload='on';\nreturn msg;\n}\nif(obj.stato.toLowerCase()==='turnoff'){\nmsg.payload='off';\nreturn msg;\n}\n}\n}\n\n", mqqtout['id'], self.x + 250, self.y)
                    in_mqtt = self.Mqtt_in('AWS-OUT', '/scsshield/AWSIOT/out', broker["id"], self.x + 10, self.y, fout["id"] )

                    self.y_half_increment()

                    mqqtout2 = self.Mqtt_out('AWS-IN', '/scsshield/AWSIOT/in', broker["id"], self.x + 490, self.y )
                    fin = self.function("var value=msg.payload.toLowerCase();\n\nif(value===\"on\"){\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"ON\",\n\"tipo\": \"Alexa.PowerController\"\n}\n}else{\nmsg.payload={\n\"id\": \"" + nome_endpoint + "\",\n\"stato\": \"OFF\",\n\"tipo\":\"Alexa.PowerController\"\n}\n}\nreturn msg;", mqqtout2['id'], self.x + 310, self.y)
                    in_mqtt2 = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 70, self.y, fin["id"] )

                    self.y_increment()

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








        buildNode.append(aws_iot_device)
        buildNode.append(broker)
        return json.dumps(buildNode)





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
    


if __name__ == "__main__":    
    print("*****node red AWS library*****")
    
    node = noderedAWS()
    #print ( node.genera())
    js = node.gennera_NodeRed_database()
    print(js)
    
    
    