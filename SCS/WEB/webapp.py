#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
from tornado import websocket
import json
import os
import shutil
import paho.mqtt.client as mqtt
import re
import janus
import asyncio


import sys
#sys.path.append('/home/pi/SCS/APP')
#import databaseAttuatori
#import nodered

import importlib.machinery
#sys.path.append('/home/pi/SCS/WEB')
#import webapp

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path_weblist = dir_path.split('/')
s = ''
for i, _ in enumerate(dir_path_weblist):
    if((len(dir_path_weblist)-1) != i):
        s = s + _ + '/'
dir_path_app = s + 'APP/'



databaseAttuatori = importlib.machinery.SourceFileLoader('databaseAttuatori', dir_path_app + 'databaseAttuatori.py').load_module()
nodered = importlib.machinery.SourceFileLoader('nodered', dir_path_app + 'nodered.py').load_module()
noderedAWS = importlib.machinery.SourceFileLoader('noderedAWS', dir_path_app + 'noderedAWS.py').load_module()




dbm = databaseAttuatori.configurazione_database()


cl = []     #websocket connessioni


q = None
q_nodered = None


#        for c in cl:
#           c.write_message(data)

class SocketHandler(websocket.WebSocketHandler):
    nodolast_temp = None

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)
        #self.write_message("HELLO WEBSOCKET")

    def on_close(self):
        if self in cl:
            cl.remove(self)

    def on_message(self, message):              
        #data = json.loads(message) 
        #print("sochet message: ", message)
        pass


#HOME
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.render('site/main.html')
        self.render('site/build/index.html')
class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        #self.render('site/main.html')
        self.render('site/build/index.html')


#PAGE
class ConfigurazioneHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('site/build/index.html')

class Testandler(tornado.web.RequestHandler):
    def get(self):
        self.render('site/build/index.html')

class noderedAlexaandler(tornado.web.RequestHandler):
    def get(self):
        self.render('site/build/index.html')
class noderedHomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('site/build/index.html')
class NoderedAlexaAWSHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('site/build/index.html')



#REACT PAGE X TEST
class reactMain(tornado.web.RequestHandler):
    def get(self):
        self.render('site/build/test3.html')
"""        
class reactImagelamp_spenta(tornado.web.RequestHandler):
    def get(self):
        self.render('site/build/lamp_spenta.svg')
class reactImagelamp_accesa(tornado.web.RequestHandler):
    def get(self):
        self.render('site/build/lamp_accesa.svg')

"""







#GET_DATA
class GetConfigurazione_JSON(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        lista_attuatori = {}
        all = dbm.RICHIESTA_TUTTI_ATTUATORI()
        for item in all:
            s = item['nome_attuatore']
            #smod = re.sub("\s+", "_", s.strip())
            smod = s

            if (("timer_salita" in item) and ("timer_discesa" in item)):
                lista_attuatori[smod] = {'nome_attuatore' : s ,'tipo_attuatore': item['tipo_attuatore'], 'indirizzo_Ambiente' : item['indirizzo_Ambiente'] ,'indirizzo_PL': item['indirizzo_PL'], 'timer_salita': item['timer_salita'], 'timer_discesa': item['timer_discesa']}
            else:
                lista_attuatori[smod] = {'nome_attuatore' : s ,'tipo_attuatore': item['tipo_attuatore'], 'indirizzo_Ambiente' : item['indirizzo_Ambiente'] ,'indirizzo_PL': item['indirizzo_PL']}

        #print("*****" , lista_attuatori)
        self.write(json.dumps(lista_attuatori))
                
class GetConfigurazione_JSONreact(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        lista_attuatori = []
        all = dbm.RICHIESTA_TUTTI_ATTUATORI()
        for item in all:
            s = item['nome_attuatore']
            #smod = re.sub("\s+", "_", s.strip())
            smod = s

            temp = dict()

            temp['nome_attuatore'] = s
            temp['tipo_attuatore'] = item['tipo_attuatore']
            temp['indirizzo_Ambiente'] = item['indirizzo_Ambiente']
            temp['indirizzo_PL'] = item['indirizzo_PL']

            if (("timer_salita" in item) and ("timer_discesa" in item)):
                temp['timer_salita'] = item['timer_salita']
                temp['timer_discesa'] = item['timer_discesa']

            if ("nome_endpoint" in item) :
                temp['nome_endpoint'] = item['nome_endpoint']

            lista_attuatori.append(temp)
            """
            if (("timer_salita" in item) and ("timer_discesa" in item)):
                lista_attuatori.append({'nome_attuatore' : s ,'tipo_attuatore': item['tipo_attuatore'], 'indirizzo_Ambiente' : item['indirizzo_Ambiente'] ,'indirizzo_PL': item['indirizzo_PL'], 'timer_salita': item['timer_salita'], 'timer_discesa': item['timer_discesa']})
            else:
                lista_attuatori.append({'nome_attuatore' : s ,'tipo_attuatore': item['tipo_attuatore'], 'indirizzo_Ambiente' : item['indirizzo_Ambiente'] ,'indirizzo_PL': item['indirizzo_PL']})
            """

        #print("*****" , lista_attuatori)
        self.write(json.dumps(lista_attuatori))   


class AGGIORNA_NOME_ATTUATORE_JOSN(tornado.web.RequestHandler):
    global q
    #x react
    def options(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')        
        self.set_status(204)
        self.finish()

    async def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        global q
        data = json.loads(self.request.body)        
        if ("nome_attuatore" in data and "nuovo_nome" in data):
            old_attuatore = dbm.RICHIESTA_ATTUATORE(data['nome_attuatore'])
            dbm.AGGIORNA_ATTUATORE_xNome(data['nome_attuatore'],data['nuovo_nome'])           
            await q.put(old_attuatore)

class AGGIORNA_INDIRIZZO_PL_JOSN(tornado.web.RequestHandler):
    global q
    #x react
    def options(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')        
        self.set_status(204)
        self.finish()

    async def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        global q
        data = json.loads(self.request.body)
        if ("nome_attuatore" in data and "indirizzo_PL" in data):
            dbm.AGGIORNA_ATTUATORE_xindirizzo_PL(data['nome_attuatore'],data['indirizzo_PL'])
            await q.put(1)
class AGGIORNA_INDIRIZZO_A_JOSN(tornado.web.RequestHandler):
    global q
    #x react
    def options(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')        
        self.set_status(204)
        self.finish()

    async def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        global q
        data = json.loads(self.request.body)
        if ("nome_attuatore" in data and "indirizzo_Ambiente" in data):
            dbm.AGGIORNA_ATTUATORE_xindirizzo_Ambiente(data['nome_attuatore'],data['indirizzo_Ambiente'])
            await q.put(1)
class AGGIORNA_TIPO_ATTUATORE_JOSN(tornado.web.RequestHandler):
    global q
    #x react
    def options(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')        
        self.set_status(204)
        self.finish()

    async def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        global q
        data = json.loads(self.request.body)
        if ("nome_attuatore" in data and "tipo_attuatore" in data):
            old_attuatore = dbm.RICHIESTA_ATTUATORE(data['nome_attuatore'])
            dbm.AGGIORNA_ATTUATORE_xTipo(data['nome_attuatore'],data['tipo_attuatore'].lower())
            await q.put(old_attuatore)
class RIMUOVI_ATTUATORE_JOSN(tornado.web.RequestHandler):
    global q
    #x react
    def options(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')        
        self.set_status(204)
        self.finish()
    
    async def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        global q
        data = json.loads(self.request.body)       
        if ("nome_attuatore" in data):
            old_attuatore = dbm.RICHIESTA_ATTUATORE(data['nome_attuatore'])
            dbm.RIMUOVE_ATTUATORE(data['nome_attuatore'])
            await q.put(old_attuatore)
class AGGIUNGI_ATTUATORE_JOSN(tornado.web.RequestHandler):
    global q
    #x react
    def options(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')        
        self.set_status(204)
        self.finish()

    async def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        global q
        data = json.loads(self.request.body)
        if ("nome_attuatore" in data and "tipo_attuatore" in data and "indirizzo_Ambiente" in data and "indirizzo_PL" in data):
            dbm.AGGIUNGI_ATTUATORE(data['nome_attuatore'],data['tipo_attuatore'].lower(),data['indirizzo_Ambiente'],data['indirizzo_PL'])
            if ("timer_salita" in data and "timer_discesa" in data):
                dbm.AGGIORNA_TIMER_SERRANDETAPPARELLE_UP(data['nome_attuatore'],data['timer_salita'])
                dbm.AGGIORNA_TIMER_SERRANDETAPPARELLE_DW(data['nome_attuatore'],data['timer_discesa'])
            await q.put(1)
class AGGIORNA_TIMER_SERRANDETAPPARELLE_JOSN(tornado.web.RequestHandler):
    global q
    #x react
    def options(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')        
        self.set_status(204)
        self.finish()

    async def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        global q
        data = json.loads(self.request.body)
        if ("nome_attuatore" in data and "timer_salita" in data):
            dbm.AGGIORNA_TIMER_SERRANDETAPPARELLE_UP(data['nome_attuatore'],data['timer_salita'])
            await q.put(1)
        if ("nome_attuatore" in data and "timer_discesa" in data):
            dbm.AGGIORNA_TIMER_SERRANDETAPPARELLE_DW(data['nome_attuatore'],data['timer_discesa'])
            await q.put(1)
class GetDeviceConfigurazione_JOSN(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        data = json.loads(self.request.body)
        dev_obj = dbm.RICHIESTA_ATTUATORE(data['nome_attuatore'])
        self.write(json.dumps(dev_obj))   






class Send_to_NodeRed(tornado.web.RequestHandler):
    global q_nodered
    async def get(self):
        global q_nodered
        self.set_header("Access-Control-Allow-Origin", "*")
        await q_nodered.put(1)
        self.write(json.dumps({'status':'ok'}))
def rec_queque_NODERED(jqueqe):
    global q_nodered
    q_nodered = jqueqe
class Get_NodeRed_manual_flow(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        n = nodered.nodered()
        js = n.gennera_NodeRed_database()

        self.write(js)
class Get_NodeRedAWS_manual_flow(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        n = noderedAWS.noderedAWS()
        js = n.gennera_NodeRed_database()

        self.write(js)


# ******************** AWS **************************
# ******************** AWS **************************
# ******************** AWS **************************

# UPLOAD FILE CERTIFICATI
class AWSCertificatiploadHandler(tornado.web.RequestHandler):
    #x react
    def options(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')        
        self.set_status(204)
        self.finish()

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        #print(self.get_arguments('tipo')[0])
        #print(self.request.files)

        if(os.path.isdir('/home/pi/AWSConfig/') == False):
            #Crea directory
            try:
                os.mkdir('/home/pi/AWSConfig/')
            except Exception as e:
                pass

        if len(self.request.files) == 1:
            key = list(self.request.files)
            if(self.get_arguments('tipo')[0] == 'PRIVATE_KEY'):
                file_name = self.request.files[key[0]][0]['filename']
                fname, file_extension = os.path.splitext(file_name)
                if(file_extension.lower() == '.key'):
                    #rename and save
                    with open('/home/pi/AWSConfig/awsiot.private.key', 'wb') as f:
                        f.write(self.request.files[key[0]][0]['body'])

            if(self.get_arguments('tipo')[0] == 'CERT_PEM'):
                file_name = self.request.files[key[0]][0]['filename']
                fname, file_extension = os.path.splitext(file_name)
                if(file_extension.lower() == '.crt'):
                    #rename and save
                    with open('/home/pi/AWSConfig/awsiot.cert.pem', 'wb') as f:
                        f.write(self.request.files[key[0]][0]['body'])

            if(self.get_arguments('tipo')[0] == 'root-CA'):
                file_name = self.request.files[key[0]][0]['filename']
                fname, file_extension = os.path.splitext(file_name)
                if(file_extension.lower() == '.pem'):
                    #rename and save
                    with open('/home/pi/AWSConfig/root-CA.crt', 'wb') as f:
                        f.write(self.request.files[key[0]][0]['body'])

        self.write(json.dumps({'status':'ok'}))

# GET CONFIGURAZIONE AWS
class GetConfigurazionereactAWSHandler(tornado.web.RequestHandler):
    #x react
    def options(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')        
        self.set_status(204)
        self.finish()

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        print("GetConfigurazionereactAWS.json -> GET")

        EndPoint = ''
        if(os.path.isfile('/home/pi/AWSConfig/EndPoint') == True):
            with open('/home/pi/AWSConfig/EndPoint') as fp:
                EndPoint = fp.readline()

        PRIVATE_KEY = ''
        if(os.path.isfile('/home/pi/AWSConfig/awsiot.private.key') == True):
            PRIVATE_KEY = 'awsiot.private.key'

        CERT_PEM = ''
        if(os.path.isfile('/home/pi/AWSConfig/awsiot.cert.pem') == True):
            CERT_PEM = 'awsiot.cert.pem'

        CRT = ''
        if(os.path.isfile('/home/pi/AWSConfig/root-CA.crt') == True):
            CRT = 'root-CA.crt'

        js = json.dumps({'EndPoint': EndPoint, 'PRIVATE_KEY': PRIVATE_KEY, 'CERT_PEM': CERT_PEM, 'CRT':CRT})
        self.write(js)

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        data = json.loads(self.request.body)

        if(os.path.isdir('/home/pi/AWSConfig/') == False):
            #Crea directory
            try:
                os.mkdir('/home/pi/AWSConfig/')
            except Exception as e:
                pass
        with open('/home/pi/AWSConfig/EndPoint', 'w') as f:
            f.write(data['EndPoint'])

        self.write(json.dumps({'status':'ok'}))

# SET DEVICE ENDPOINT in AWS
class SetDeviceEndPointAWS(tornado.web.RequestHandler):
    #x react
    def options(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')        
        self.set_status(204)
        self.finish()

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        data = json.loads(self.request.body)
        if (("nome_attuatore" in data) and ("nome_endpoint" in data)):
            dbm.AGGIORNA_ATTUATORE_x_AWS_ENDPOINT(data['nome_attuatore'], data['nome_endpoint'])

        self.write(json.dumps({'status':'ok'}))






















def rec_queque(jqueqe):
    global q
    q = jqueqe
    #print(type(q))




def make_app():
    return tornado.web.Application([
        (r"/", HomeHandler),
        (r"/index.html", HomeHandler),

        (r"/test.html", Testandler),
        (r"/configurazione.html", ConfigurazioneHandler),
        (r"/noderedAlexa.html", noderedAlexaandler),
        (r"/noderedHome.html", noderedHomeHandler),
        (r"/NoderedAlexaAWS.html", NoderedAlexaAWSHandler),


        
        (r"/GetConfigurazionereact.json", GetConfigurazione_JSONreact),

        (r"/GetConfigurazione.json", GetConfigurazione_JSON),
        (r"/AGGIORNA_NOME_ATTUATORE.json", AGGIORNA_NOME_ATTUATORE_JOSN),
        (r"/AGGIORNA_INDIRIZZO_PL.json", AGGIORNA_INDIRIZZO_PL_JOSN),
        (r"/AGGIORNA_INDIRIZZO_A.json", AGGIORNA_INDIRIZZO_A_JOSN),
        (r"/AGGIORNA_TIPO_ATTUATORE.json", AGGIORNA_TIPO_ATTUATORE_JOSN),
        (r"/RIMUOVI_ATTUATORE.json", RIMUOVI_ATTUATORE_JOSN),
        (r"/AGGIUNGI_ATTUATORE.json", AGGIUNGI_ATTUATORE_JOSN),
        (r"/AGGIORNA_TIMER_SERRANDETAPPARELLE.json", AGGIORNA_TIMER_SERRANDETAPPARELLE_JOSN),
        (r"/GetDeviceConfigurazione.json", GetDeviceConfigurazione_JOSN),

        #Node red
        (r"/Send_to_NodeRed.json", Send_to_NodeRed),
        (r"/Get_NodeRed_manual_flow.json", Get_NodeRed_manual_flow),
        (r"/Get_NodeRedAWS_manual_flow.json", Get_NodeRedAWS_manual_flow),


 


        #AWS certificati Upload
        (r"/AWSCertificatiploadHandler.html", AWSCertificatiploadHandler),
        (r"/GetConfigurazionereactAWS.json", GetConfigurazionereactAWSHandler),
        (r"/SetDeviceEndPointAWS.json", SetDeviceEndPointAWS),



        #websocket
        (r'/ws', SocketHandler),

	    #(r'/site/js/(.*)', tornado.web.StaticFileHandler, {'path': '/home/pi/SCS/WEB/site/js/'}),
	    #(r'/site/css/(.*)', tornado.web.StaticFileHandler, {'path': '/home/pi/SCS/WEB/site/css/'}),
	    (r'/site/image/(.*)', tornado.web.StaticFileHandler, {'path': dir_path + '/site/build'}),




        #(r"/test.html", Testandler),
        #(r"/configurazione.html", ConfigurazioneHandler),

        #React x pagina test
        (r"/test3.html", reactMain),
        (r"/build(.*)", tornado.web.StaticFileHandler, {'path': dir_path + '/site/build/'}),
	    (r'/static/css/(.*)', tornado.web.StaticFileHandler, {'path': dir_path + '/site/build/static/css/'}),
	    (r'/static/js/(.*)', tornado.web.StaticFileHandler, {'path': dir_path + '/site/build/static/js/'})





    ], debug=True)



if __name__ == "__main__":    
    print("*****WEBAPP*****")
    print(tornado.version)
    
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()



