import requests
import httplib2
import json
import io
from tok import *

class DB:
    def __init__(self):
        t = tok()
        self.url = t.getUrlEnv()
    
    def getJson(self, word):
        word = str(word.upper())
        requ = self.url + word
        h = httplib2.Http("__pycache__")
        r, content = h.request(requ, "GET")
        fix_bytes_value = content.replace(b"'", b'"')
        js = json.load(io.BytesIO(fix_bytes_value))  
        return js
    
    def getDescription(self, js, lang):
        stri = ""
        count = 1
        for w in js["data"]["usable"]:
            for i in w["Descriptions"]:
                if(i["LangDesc"] == lang):
                    stri += ( str(count) + ") " + i["Description"] + "\n\n")
                    count += 1
        return stri
    
    def getLanguage(self, js):
        stri = str(js["data"]["usable"][0]["Word"]["Language"])
        return stri
    
    def getExample(self, js, lang):
        stri = ""
        count = 0
        for w in js["data"]["usable"]:
            for i in w["Examples"]:
                if(i["LangExample"] == lang):
                    count += 1
                    break
        if(count == 0):
            if(lang == "IT"):
                stri = "Non ci sono esempi inseriti nel database!"
                stri = stri.upper()
                stri += "\n"
            elif(lang == "EN"):
                stri = "There are no examples available in our database!"
                stri = stri.upper()
                stri += "\n"
        else:
            for w in js["data"]["usable"]:
                for i in w["Examples"]:
                    if(i["LangExample"] == lang):
                        stri += ( str(count) + ")  " + i["Example"] + "\n\n")
                        count += 1
        return stri

    def isThereWord(self, js):
        if(js["status"] == "FoundWord"):
            return True, 0
        elif(js["status"] == "AddedWord"):
            return 2, 0
        elif(js["status"] == "NotUsableWord"):
            number = js["data"]["unusable"][0][1]
            return 3, number
        return False
    
    def getSinonimsIT(self, js):
        count = 0
        stri = ""
        for i in js["data"]["usable"]:
            for j in i["SinonimsIT"]:
                count += 1
                if(count >= 0):
                    break
        if (count == 0):
            stri = "La parola ricercata non ha sinonimi inseriti nel nostro database!"
            stri = stri.upper()
            stri += "\n"
        else:
            count = 1
            for i in js["data"]["usable"]:
                for j in i["SinonimsIT"]:
                    stri += ( str(count) + ")  " + j + "\n\n")
                    count += 1
        return stri

    def getSinonimsEN(self, js):
        count = 0
        stri = ""
        for i in js["data"]["usable"]:
            for j in i["SinonimsEN"]:
                count += 1
                if(count >= 0):
                    break
        if (count == 0):
            stri = "The word you are looking for has no synonyms in our database!"
            stri = stri.upper()
            stri += "\n"
        else:
            count = 1
            for i in js["data"]["usable"]:
                for j in i["SinonimsEN"]:
                    stri += ( str(count) + ")  " + j + "\n\n")
                    count += 1
        return stri
    
    def getTranslationIT(self, js):
        count = 0
        stri = ""
        for i in js["data"]["usable"]:
            for j in i["TranslasionsIT"]:
                count += 1
                if(count >= 0):
                    break
        if (count == 0):
           stri = "The word you are looking for has no translations in our database!"
           stri = stri.upper()
           stri += "\n"
        else:
            count = 1
            for i in js["data"]["usable"]:
                for j in i["TranslasionsIT"]:
                    stri += ( str(count) + ")  " + j + "\n\n")
                    count += 1
        return stri
   
    def getTranslationEN(self, js):
        count = 0
        stri = ""
        for i in js["data"]["usable"]:
            for j in i["TranslasionsEN"]:
                count += 1
                if(count >= 0):
                    break
        if (count == 0):
            stri = "La parola ricercata non ha traduzioni inserite nel nostro database!"
            stri = stri.upper()
            stri += "\n"
        else:
            count = 1
            for i in js["data"]["usable"]:
                for j in i["TranslasionsEN"]:
                    stri += ( str(count) + ")  " + j + "\n\n")
                    count += 1
        return stri

    def makeMsgIT(self, word, js):
        stri = ""
        lang = "IT"
        stri += "Parola: " + word + "\n\n"
        stri += "Lingua: Italiano\n\n"
        stri += "Descrizioni: \n" + self.getDescription(js, lang)
        stri += "Esempi: \n" + self.getExample(js, lang)
        stri += "Sinonimi: \n" + self.getSinonimsIT(js)
        stri += "Traduzioni (Inglese): \n" + self.getTranslationEN(js)
        return stri

    
    def makeMsgEN(self, word, js):
        stri = ""
        lang = "EN"
        stri += "Word: " + word + "\n\n"
        stri += "Language: English\n\n"
        stri += "Descriptions: \n" + self.getDescription(js, lang)
        stri += "Examples: \n" + self.getExample(js, lang)
        stri += "Synonyms: \n" + self.getSinonimsEN(js)
        stri += "Translations (Italian): \n" + self.getTranslationIT(js)
        return stri
    
 #Esempio di istanza della classe

if __name__ == '__main__':
    db = DB()
    word = "Virus"
    js = db.getJson(word)
    tmp, number = db.isThereWord(js)
    if(tmp == True):
        if(db.getLanguage(js) == "IT"):
            print(db.makeMsgIT(word, js))
        elif(db.getLanguage(js) == "EN"):
            print(db.makeMsgEN(word, js))
        else:
            print(db.makeMsgIT(word, js))
            print( "\n---------------\n")
            print(db.makeMsgEN(word, js))
    elif(tmp == 2):
       print("La parola non è presente nel database ma è stata proposta per l'inserimento!")
    elif(tmp == 3):
        print("La parola non è presente nel database ma è stata cercata per ben " + str(number) + " volte!")
    else:
        print("Parola non trovata! Il nostro team la inserirà il prima possibile!")


