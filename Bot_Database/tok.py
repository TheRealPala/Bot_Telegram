import json
import os

class tok:
    def getToken(self):
        json_conf=open('codice.json')#apre il file di configurazione 
        conf=json.load(json_conf)#parsa il json
        json_conf.close()#chiude il file
        prova = conf["codice"]
        return prova      
    
    def getUrl(self):
        json_conf=open('codice.json')#apre il file di configurazione 
        conf=json.load(json_conf)#parsa il json
        json_conf.close()#chiude il file
        url = conf["url"]
        return url   
