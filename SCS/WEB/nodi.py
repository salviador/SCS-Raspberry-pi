#!/usr/bin/env python3

import tornado.httpserver
import tornado.ioloop
import tornado.web
import json

import sys
sys.path.append('/home/pi/programma')
import database

dbm = database.nodi_database()


class GetListaNodiSettingHandler(tornado.web.RequestHandler):
    def get(self):
        #***************************************
        #***************************************
        #***************************************
        #recupera nodi dal server e inviala al main.html
        #leggi il setting dal database
        #***************************************
        #***************************************
        #***************************************
        #test --->
        """
        nodi = {
            "UUID":{"nome":"campanello", "tipo":"1", "pulsante_stato" : [{"ch1":"false","ch2":"true"}] },
            "UUID":{"nome":"campanello", "tipo":"1", "pulsante_stato" : [{"ch1":"false","ch2":"true"}] },
               }


        Struttura database

        UUID - nome assegnato - typeNodo - pulsante stato 1 , ..., contatore

        """

        lista_nodi = {}

        all_nodi = dbm.Get_All_Nodi()
        for item in all_nodi:
            lista_nodi[item['UUID']] = {'UUID' : item['UUID'] ,'nome': item['nome'], 'chAudio' : item['chaudio'] ,'type': item['type'], 'stato': item['stato'] }
        
        #print("*****" , lista_nodi)

        self.write(json.dumps(lista_nodi)) 




class AggiungiNodo_nodoHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
       
        if ("UUID" in data and "nome" in data and "type" in data and "stato" in data and "chAudio" in data):
            dbm.AggiungioUpdate_Nodo_inDatabase(data['UUID'],data['nome'],data['chAudio'],data['type'],data['stato'],0)


        


class RimuoviNodo_nodoHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
       
        if ("UUID" in data):
            dbm.Rimuovi_Nodo(data['UUID'])


        
