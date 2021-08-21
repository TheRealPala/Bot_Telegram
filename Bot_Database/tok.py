import json
import os


class tok:

    def getToken(self):
        # apre il file di configurazione
        json_conf = open(os.getcwd() + '/codice.json')
        conf = json.load(json_conf)  # parsa il json
        json_conf.close()  # chiude il file
        prova = conf["codice"]
        return prova

    def getUrl(self):
        # apre il file di configurazione
        json_conf = open(os.getcwd() + '/codice.json')
        conf = json.load(json_conf)  # parsa il json
        json_conf.close()  # chiude il file
        url = conf["url"]
        return url

    def getUrlEnv(self):
        return str(os.environ['URL'])

    def getTokenEnv(self):
        return str(os.environ['CODICE'])
