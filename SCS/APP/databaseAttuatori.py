#!/usr/bin/env python3
from tinydb import TinyDB, Query
import os


#tinydb
#https://pypi.org/project/tinydb/#example-code
#https://github.com/msiemens/tinydb

"""

Struttura database

nome attuatore - tipo attuatore - indirizzo Ambiente - indirizzo PL

"""
dir_path = os.path.dirname(os.path.realpath(__file__))

FILE = dir_path + "/db.json"



class configurazione_database:
    def __init__(self):
        self.db = TinyDB(FILE)
        #print(self.db.all())
    
    def CHECHK_ESISTE_ATTUATORE(self,nome_attuatore):
        if(nome_attuatore != None):
            UUID = Query()
            val = self.db.search(UUID.nome_attuatore == nome_attuatore)
            #print('------')
            #print(val)
            #print(',,,,,,')
            if(len(val) > 0):
                return True
        return False

    def AGGIUNGI_ATTUATORE(self,nome_attuatore,tipo_attuatore,indirizzo_Ambiente,indirizzo_PL):
        if(self.CHECHK_ESISTE_ATTUATORE(nome_attuatore)==False):
            #Insert new
            self.db.insert({ 'nome_attuatore' : nome_attuatore , 
                'tipo_attuatore' : tipo_attuatore,
                'indirizzo_Ambiente' : indirizzo_Ambiente,
                'indirizzo_PL' : indirizzo_PL
                })
        else:
            #Update exist
            UUID = Query()
            self.db.update({'tipo_attuatore' : tipo_attuatore,
                'indirizzo_Ambiente' : indirizzo_Ambiente,
                'indirizzo_PL' : indirizzo_PL} ,
                UUID.nome_attuatore == nome_attuatore)


    

    def AGGIORNA_ATTUATORE_xNome(self,nome_attuatore,nuovo_attuatore):
        if(self.CHECHK_ESISTE_ATTUATORE(nome_attuatore)==True):
            if(self.CHECHK_ESISTE_ATTUATORE(nuovo_attuatore)==False):
                UUID = Query()
                self.db.update({ 'nome_attuatore' : nuovo_attuatore} ,
                    UUID.nome_attuatore == nome_attuatore)    
    def AGGIORNA_ATTUATORE_xTipo(self,nome_attuatore,tipo_attuatore):
        if(self.CHECHK_ESISTE_ATTUATORE(nome_attuatore)==True):
            UUID = Query()
            self.db.update({ 'tipo_attuatore' : tipo_attuatore} ,
                UUID.nome_attuatore == nome_attuatore)    
    def AGGIORNA_ATTUATORE_xindirizzo_Ambiente(self,nome_attuatore,indirizzo_Ambiente):
        if(self.CHECHK_ESISTE_ATTUATORE(nome_attuatore)==True):
            UUID = Query()
            self.db.update({ 'indirizzo_Ambiente' : indirizzo_Ambiente} ,
                UUID.nome_attuatore == nome_attuatore)                
    def AGGIORNA_ATTUATORE_xindirizzo_PL(self,nome_attuatore,indirizzo_PL):
        if(self.CHECHK_ESISTE_ATTUATORE(nome_attuatore)==True):
            UUID = Query()
            self.db.update({ 'indirizzo_PL' : indirizzo_PL} ,
                UUID.nome_attuatore == nome_attuatore)   
    def AGGIORNA_TIMER_SERRANDETAPPARELLE_UP(self,nome_attuatore,timer_salita):
        if(self.CHECHK_ESISTE_ATTUATORE(nome_attuatore)==True):
            UUID = Query()
            self.db.update({ 'timer_salita' : timer_salita} ,
                UUID.nome_attuatore == nome_attuatore)   
    def AGGIORNA_TIMER_SERRANDETAPPARELLE_DW(self,nome_attuatore,timer_discesa):
        if(self.CHECHK_ESISTE_ATTUATORE(nome_attuatore)==True):
            UUID = Query()
            self.db.update({ 'timer_discesa' : timer_discesa} ,
                UUID.nome_attuatore == nome_attuatore)   
    def AGGIORNA_ATTUATORE_x_AWS_ENDPOINT(self,nome_attuatore,nome_endpoint):
        if(self.CHECHK_ESISTE_ATTUATORE(nome_attuatore)==True):
            UUID = Query()
            self.db.update({ 'nome_endpoint' : nome_endpoint} ,
                UUID.nome_attuatore == nome_attuatore)   



    




    def RICHIESTA_ATTUATORE(self,nome_attuatore):
        if(self.CHECHK_ESISTE_ATTUATORE(nome_attuatore)==True):
            nodo = Query()
            val = self.db.search(nodo.nome_attuatore == nome_attuatore)
            return val[0]
        return None
    
    def RICHIESTA_TUTTI_ATTUATORI(self):
        query = self.db.all()
    
        #---------------------------------------------------
        all_att = list()
        #Sort "nome_attuatore" in ordine alfanumerico
        alldev_nome_attuatore = list()
        for q in query:
            alldev_nome_attuatore.append(q['nome_attuatore'])
        alldev_nome_attuatore.sort()
        #crea una nuova lista di device in ordine alfanumerico
        for nome_att in alldev_nome_attuatore:
            for q in query:
                if(q['nome_attuatore'] == nome_att):
                    all_att.append(q)
        #Ordina per tipo
        ordine_x_tipo = ['on_off','dimmer', 'serrande_tapparelle', 'sensori_temperatura', 'termostati', 'serrature', 'campanello_porta', 'gruppi']
        all_attuatori = list()
        for ord_tipo in ordine_x_tipo:
            for q in all_att:
                if(ord_tipo == q['tipo_attuatore']):
                    all_attuatori.append(q)

        return all_attuatori

    def RIMUOVE_ATTUATORE(self,nome_attuatore):
        if(self.CHECHK_ESISTE_ATTUATORE(nome_attuatore)==True):
            UUID = Query()
            self.db.remove(UUID.nome_attuatore == nome_attuatore)   



    


    def myprint(self):
        #self.db.purge()
        #print(self.db.all())
        #print(len(self.db))
        pass

if __name__ == "__main__":    
    dbm = configurazione_database()
    #dbm.AGGIUNGI_ATTUATORE('Faretti',"ON_OFF",4,2)
    #dbm.AGGIUNGI_ATTUATORE('Luce Camera',"ON_OFF",5,8)
    #dbm.AGGIUNGI_ATTUATORE('Luce Corridoio',"ON_OFF",6,1)

    #dbm.RIMUOVE_ATTUATORE('Faretti')

    #dbm.AGGIORNA_ATTUATORE_xNome("Luce Camera", "teees");
    #dbm.AGGIORNA_ATTUATORE_xTipo()

    #dbm.myprint()

    va = dbm.RICHIESTA_ATTUATORE('mvhjm')
    print(va)
    #print(va['nome_attuatorek']  )


    #print(type(va) == int )
    try:
        print(va['nome_atstuatore']  )
    except KeyError as k:
        print("Non ha il nome")
        pass
    #print(va.keys()[0] in 'nome_attuatore')