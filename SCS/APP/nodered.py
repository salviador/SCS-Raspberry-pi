import time
import os
import databaseAttuatori
import uuid
import random
import json
import asyncio
import subprocess

class nodered():
    def __init__(self) -> None:
        self.ID_tab = self.genera_random_ID()
        self.ID_MQTT_broker = self.genera_random_ID()

        self.x = 90
        self.y = 20 #60
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
        
    def vsh_virtual_device(self, name, tipo, id_dichie_connesso, x, y) -> dict:
        w = dict()
        w["id"] = self.genera_random_ID()       
        w["type"] = "vsh-virtual-device"
        w["z"] = self.ID_tab
        w["name"] = name
        w["topic"] = ""
        w["connection"] = ""
        w["template"] = tipo
        w["passthrough"] = False
        w["diff"] = False
        w["filter"] = False
        w["x"] = x
        w["y"] = y
        w["wires"] = [id_dichie_connesso]
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

    def genera_random_ID(self) -> str:
        rd = random.Random()
        a = uuid.uuid1(rd.getrandbits(48))
        str_a = str(a)
        val = str(a)[:8] + "." + str(a)[9:12] + str(a)[26:29]
        return val












    def gennera_NodeRed_database(self):
        tab = self.Tab()
        broker = self.Mqtt_broker()
        buildNode = [tab]

        comment0_flag = True
        comment1_flag = True
        comment2_flag = True
        comment3_flag = True
        comment4_flag = True

        query = self.dbm.RICHIESTA_TUTTI_ATTUATORI()
        for q in query:
            if(q['tipo_attuatore'] == 'on_off'):
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
                mqqtout = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 780, self.y )
                fout = self.function("var value=msg.payload.directive;\n\nif(value===\"TurnOff\"){\nmsg.payload='off';\n}else{\nmsg.payload='on';\n}\n\nreturn msg;", mqqtout['id'], self.x + 570, self.y)
                alexa = self.vsh_virtual_device(nome, "SWITCH", [fout['id']], self.x + 400, self.y)
                fin = self.function("var value=msg.payload.toLowerCase();\n\nif(value===\"on\"){\nmsg.payload={\"powerState\":\"ON\"};\n}else{\nmsg.payload={\"powerState\":\"OFF\"};\n}\n\nreturn msg;", alexa['id'], self.x + 230, self.y)
                in_mqtt = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 30, self.y, fin["id"] )
                self.y_increment()

                if(comment0_flag):
                    buildNode.append(comment0)
                    comment0_flag = False
                buildNode.append(comment1)
                buildNode.append(comment2)
                buildNode.append(mqqtout)
                buildNode.append(fout)
                buildNode.append(alexa)
                buildNode.append(fin)
                buildNode.append(in_mqtt)
       
            elif(q['tipo_attuatore'] == 'dimmer'):
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
                mqqtout_1 = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 1010, self.y - 20 )
                mqqtout_2 = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 1010, self.y + 20 )
                fout_1 = self.function("var value=msg.payload;\n\nif(value.powerState.toLowerCase()===\"off\"){\nmsg.payload='off';\n}else{\nmsg.payload='on';\n}\nreturn msg;", mqqtout_1['id'], self.x + 780, self.y - 20)
                fout_2 = self.function("var value=msg.payload;\n\nif(value.powerState.toLowerCase()===\"on\"){\nmsg.payload=value.brightness;\nreturn msg;}", mqqtout_2['id'], self.x + 780, self.y + 20)
                alexa = self.vsh_virtual_device(nome, "DIMMABLE_LIGHT_BULB", [fout_1['id'],fout_2['id']], self.x + 630, self.y)
                fin_1 = self.function("var value=msg.payload.toLowerCase();\n\nif(value===\"on\"){msg.payload={\"powerState\":\"ON\"};\n}else{\nmsg.payload={\"powerState\":\"OFF\"};\n}\nreturn msg;", alexa['id'], self.x + 420, self.y - 20)
                fin_2 = self.function("var value=msg.payload;\nvar numv=parseInt(value);\n\nmsg.payload={\"powerState\":\"ON\", \"brightness\": numv};\nreturn msg;", alexa['id'], self.x + 420, self.y + 20)
                in_mqtt_1 = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 130, self.y - 20, fin_1["id"] )
                in_mqtt_2 = self.Mqtt_in(nome, topicstatusPerc, broker["id"], self.x + 130, self.y + 20, fin_2["id"] )
                self.y_increment()

                if(comment1_flag):
                    buildNode.append(comment0)
                    comment1_flag = False
                buildNode.append(comment1)
                buildNode.append(comment2)
                buildNode.append(comment3)                
                buildNode.append(mqqtout_1)
                buildNode.append(mqqtout_2)
                buildNode.append(fout_1)               
                buildNode.append(fout_2)
                buildNode.append(alexa)
                buildNode.append(fin_1)
                buildNode.append(fin_2)
                buildNode.append(in_mqtt_1)
                buildNode.append(in_mqtt_2)

            elif(q['tipo_attuatore'] == 'sensori_temperatura'):
                nome = q['nome_attuatore']
                topicstatus = "/scsshield/device/" + nome + "/status"

                #Commento
                comment0 = self.Comment("SENSORE TEMPERATURA", self.x + 73, self.y)
                if(comment2_flag):
                    self.y_increment()
                comment1 = self.Comment("Alexa, qual è la temperatura del " + nome, self.x + 155, self.y)
                self.y_increment()

                #out
                alexa = self.vsh_virtual_device(nome, "TEMPERATURE_SENSOR", [], self.x + 480, self.y)
                fin = self.function("var value=msg.payload;\nvar numv=parseInt(value);\n\nmsg.payload={\"temperature\":numv, \"scale\": \"CELSIUS\"};\n\nreturn msg;", alexa['id'], self.x + 310, self.y)
                in_mqtt = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 120, self.y, fin["id"] )
                self.y_increment()

                if(comment2_flag):
                    buildNode.append(comment0)
                    comment2_flag = False
                buildNode.append(comment1)
                buildNode.append(alexa)
                buildNode.append(fin)
                buildNode.append(in_mqtt)

      
            elif(q['tipo_attuatore'] == 'termostati'):
                nome = q['nome_attuatore']
                topicstatus = "/scsshield/device/" + nome + "/status"       #temperatura ambiente misurata
                topicTemp_Termostato = "/scsshield/device/" + nome + "/temperatura_termostato_impostata" #temperatura ambiente misurata
                topiccomando = "/scsshield/device/" + nome + "/set_temp_termostato"      #set temp termostato

                #Commento
                comment0 = self.Comment("TERMOSTATO", self.x + 30, self.y)
                if(comment3_flag):
                    self.y_increment()
                comment1 = self.Comment("Alexa, imposta la temperatura del " + nome + " a 20°" , self.x + 570, self.y)
                comment2 = self.Comment("Alexa, qual è la temperatura del " + nome, self.x + 190, self.y)
                self.y_increment()

                #out
                mqqtout = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 860, self.y)
                fout = self.function("var value=msg.payload;\n\nmsg.payload=value.targetTemperature;\nreturn msg;", mqqtout['id'], self.x + 650, self.y)
                alexa = self.vsh_virtual_device(nome, "THERMOSTAT", [fout['id']], self.x + 480, self.y)
                fin_1 = self.function("var value=msg.payload;\nvar numv=parseInt(value);\nmsg.payload={\"temperature\":numv, \"scale\": \"CELSIUS\"};\nreturn msg;", alexa['id'], self.x + 310, self.y - 20)
                fin_2 = self.function("var value=msg.payload;\nvar numv=parseInt(value);\nmsg.payload={\"targetTemperature\":numv, \"targetScale\": \"CELSIUS\"};\nreturn msg;", alexa['id'], self.x + 310, self.y + 20)
                in_mqtt_1 = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 110, self.y - 20, fin_1["id"] )
                in_mqtt_2 = self.Mqtt_in(nome, topicTemp_Termostato, broker["id"], self.x + 110, self.y + 20, fin_2["id"] )
                self.y_increment()

                if(comment3_flag):
                    buildNode.append(comment0)
                    comment3_flag = False
                buildNode.append(comment1)
                buildNode.append(comment2)
                buildNode.append(mqqtout)
                buildNode.append(fout)
                buildNode.append(alexa)
                buildNode.append(fin_1)
                buildNode.append(fin_2)
                buildNode.append(in_mqtt_1)
                buildNode.append(in_mqtt_2)

            elif(q['tipo_attuatore'] == 'serrande_tapparelle'):
                nome = q['nome_attuatore']
                topicstatus = "/scsshield/device/" + nome + "/status"       
                topiccomando = "/scsshield/device/" + nome + "/percentuale" 

                #Commento
                comment0 = self.Comment("SERRANDE/TAPPARELLE", self.x + 60, self.y)
                if(comment4_flag):
                    self.y_increment()
                comment1 = self.Comment("Alexa, imposta le persiane " + nome + " al cinquanta percento" , self.x + 195, self.y)
                self.y_increment()

                #out
                mqqtout = self.Mqtt_out(nome, topiccomando, broker["id"], self.x + 860, self.y)
                fout = self.function("var value=msg.payload;\n\nmsg.payload=value.percentage;\nreturn msg;", mqqtout['id'], self.x + 650, self.y)
                alexa = self.vsh_virtual_device(nome, "BLINDS", [fout['id']], self.x + 480, self.y)
                fin = self.function("var value=msg.payload;\nvar numv=parseInt(value);\nnmsg.payload={\"percentage\": numv};\nreturn msg;", alexa['id'], self.x + 310, self.y)
                in_mqtt = self.Mqtt_in(nome, topicstatus, broker["id"], self.x + 110, self.y, fin["id"] )
                self.y_increment()

                if(comment4_flag):
                    buildNode.append(comment0)
                    comment4_flag = False
                buildNode.append(comment1)
                buildNode.append(fout)
                buildNode.append(alexa)
                buildNode.append(fin)
                buildNode.append(in_mqtt)









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
    print("*****node red library*****")
    
    node = nodered()
    #print ( node.genera())
    #js = node.gennera_NodeRed_database()
    #print(js)
    
    print(os.popen("sudo node-red-stop").read())

    
    #print(os.popen("sudo node-red-start").read())
    process = subprocess.Popen(['node-red-start'],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    
    print(process)
    
    
    process = subprocess.Popen(['systemctl', 'status nodered.service'],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)                        
    
    print(process)
    