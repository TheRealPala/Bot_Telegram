import requests
import httplib2
import json
import io
from tok import *

class DB:
    def __init__(self):
        t = tok()
        self.url = t.getUrl()
    
    def getJson(self, word):
        word = str(word.upper())
        requ = self.url + word
        h = httplib2.Http("__pycache__")
        r, content = h.request(requ, "GET")
        fix_bytes_value = content.replace(b"'", b'"')
        js = json.load(io.BytesIO(fix_bytes_value))  
        return js
    
    def getDescription(self, word, lang):
        js = self.getJson(word)
        stri = ""
        count = 1
        for w in js["data"]["usable"]:
            for i in w["Descriptions"]:
                if(i["LangDesc"] == lang):
                    stri += ( str(count) + ") " + i["Description"] + "\n\n")
                    count += 1
        return stri
    
    def getLanguage(self, word):
        js = self.getJson(word)
        stri = ""
        for w in js["data"]["usable"]:
            stri += ( w["Word"]["Language"] + "\n")
        return stri
    
    def getExample(self, word, lang):
        js = self.getJson(word)
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
            elif(lang == "EN"):
                stri = "There are no examples available in our database!"
        else:
            for w in js["data"]["usable"]:
                for i in w["Examples"]:
                    if(i["LangExample"] == lang):
                        stri += ( str(count) + ")  " + i["Example"] + "\n\n")
                        count += 1
        return stri

    def isThereWord(self, word):
        js = self.getJson(word)
        if(js["status"] == "FoundWord"):
            return True
        elif(js["status"] == "NotUsableWord"):
            return 2
        return False
    
    def getSinonimsIT(self, word):
        js = self.getJson(word)
        count = 0
        stri = ""
        for i in js["data"]["usable"]:
            for j in i["SinonimsIT"]:
                count += 1
                if(count >= 0):
                    break
        if (count == 0):
            stri = "La parola ricercata non ha sinonimi inseriti nel nostro database!"
        else:
            count = 1
            for i in js["data"]["usable"]:
                for j in i["SinonimsIT"]:
                    stri += ( str(count) + ")  " + j + "\n\n")
                    count += 1
        return stri

    def getSinonimsEN(self, word):
        js = self.getJson(word)
        count = 0
        stri = ""
        for i in js["data"]["usable"]:
            for j in i["SinonimsEN"]:
                count += 1
                if(count >= 0):
                    break
        if (count == 0):
            stri = "The word you are looking for has no synonyms in our database!"
        else:
            count = 1
            for i in js["data"]["usable"]:
                for j in i["SinonimsEN"]:
                    stri += ( str(count) + ")  " + j + "\n\n")
                    count += 1
        return stri
    
    def getTranslationIT(self, word):
        js = self.getJson(word)
        count = 0
        stri = ""
        for i in js["data"]["usable"]:
            for j in i["TranslasionsIT"]:
                count += 1
                if(count >= 0):
                    break
        if (count == 0):
            stri = "La parola ricercata non ha traduzioni inserite nel nostro database!"
        else:
            count = 1
            for i in js["data"]["usable"]:
                for j in i["TranslasionsIT"]:
                    stri += ( str(count) + ")  " + j + "\n\n")
                    count += 1
        return stri
   
    def getTranslationEN(self, word):
        js = self.getJson(word)
        count = 0
        stri = ""
        for i in js["data"]["usable"]:
            for j in i["TranslasionsEN"]:
                count += 1
                if(count >= 0):
                    break
        if (count == 0):
            stri = "The word you are looking for has no translations in our database!"
        else:
            count = 1
            for i in js["data"]["usable"]:
                for j in i["TranslasionsEN"]:
                    stri += ( str(count) + ")  " + j + "\n\n")
                    count += 1
        return stri

    def makeMsgIT(self, word):
        stri = ""
        lang = "IT"
        stri += "Parola: " + word + "\n"
        stri += "Lingua: Italiano\n"
        stri += "Descrizioni: \n" + self.getDescription(word, lang)
        stri += "Esempi: \n" + self.getExample(word, lang)
        stri += "Sinonimi: \n" + self.getSinonimsIT(word)
        stri += "Traduzione: \n" + self.getTranslationIT(word)
        return stri

    
    def makeMsgEN(self, word):
        stri = ""
        lang = "EN"
        stri += "Word: " + word + "\n"
        stri += "Language: English\n"
        stri += "Descriptions: \n" + self.getDescription(word, lang)
        stri += "Examples: \n" + self.getExample(word, lang)
        stri += "Synonyms: \n" + self.getSinonimsEN(word)
        stri += "Translations: \n" + self.getTranslationEN(word)
        return stri
    
 #Esempio di istanza della classe

if __name__ == '__main__':
    db = DB()
    word = "Virus"
    tmp = db.isThereWord(word)
    if(tmp):
        if(db.getLanguage == "IT"):
            print(db.makeMsgIT(word))
        elif(db.getLanguage == "EN"):
            print(db.makeMsgEN(word))
        else:
            print(db.makeMsgIT(word))
            print( "\n---------------\n")
            print(db.makeMsgEN(word))
    elif(tmp == 2):
        print("La parola è in fase di inserimento!")
    else:
        print("Parola non trovata! Il nostro team la inserirà il prima possibile!")
