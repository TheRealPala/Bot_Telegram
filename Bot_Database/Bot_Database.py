import sys
from os import *
import json
sys.path.append(getcwd())
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dbhandler import *
from tok import *
TOKEN = "" #token di BotFather
we = WordExtractor("localhost", "root", "palaqwe123", "DBTMM")#Istanza della classe per database

def getOutput(word):
    out = ""
    out += ("Parola da ricercare: " + str(word))
    #Ottengo la descrizione
    out += "\n\nDescrizione:"
    for w in we.getDescriptions(word):
        out += ("\n" + str(w[3]))
    #Ottengo i sinonimi
    out += "\n\nSinonimi: "
    for w in we.getSynonyms(word):
        out += ("\n" + str(w[0]))
    out += "\n\nEsempi: "
    #Ottengo la esempi
    for w in we.getExamples(word):
        out += ("\n" + str(w[0]))
    #Ottengo la lingua
    out += "\n\nLingua: "
    lang = ""
    for w in we.getWordLanguages(word):
        l = str(w[0])
        print(l)
        if l == "{'IT'}":
            out += ("\nItaliano")
            lang = "IT"
        else:
            out += ("\nInglese")
            lang = "EN"
    #Ottengo la traduzione
    out += "\n\nTraduzione: "
    for w in we.getTranslations(word, lang):
         out += ("\n" + str(w))
    print("\n" + out)
    return out 

def findWord(stri, up, cont):
    word = ""
    for elem in we.getWord(stri):
        word = elem[0]
    if(word == None or len(word) == 0):
        up.message.reply_text("\nLa parola non è ancora presente nell'archivio!\nIl nostro team la aggiungerà il prima possibile!")
    else:
        up.message.reply_text(getOutput(word))

#Funzione che viene lanciata al comando /define parola 
def defineFunction(up, cont):
    string  = inputBot(up, cont)  #ottiene la parola da ricercare
    if(len(string) == 0 or string == "-1"): #se la parola è vuota o si è verificato qualche errore nell'input stampa il seguente errore
        up.message.reply_text("Non hai inserito una parola da ricercare!\nSintassi: /def parola_da_definire")
    else: #altrimenti cerca la parola nel database 
        findWord(string, up, cont)#cerca la parola nel file excel

def delStr(buf, dele):
    if(buf == dele):
        return "-1"
    la = buf.split(" ")
    lb = dele.split(" ")
    lc = [x for x in la if x not in lb]
    stri = " ".join(lc)
    return stri


#Funzione che, dato il comando, estrapola e fornisce la parola/le parole da cercare nel database. 
def inputBot(up, cont):
    buf = up.message.text #ottiene tutta la stringa del comando
    dele = "/def" 
    if(buf == dele):
        return "-1"
    la = buf.split(" ")
    lb = dele.split(" ")
    lc = [x for x in la if x not in lb]#ciclo per gestire le parole con lo spazio ("San Valentino")
    stri = " ".join(lc)# Prende tutte le parole presenti nella lista, le unisce in una sola stringa e le separa con il carattere " " ('32[10]', '0x20')
    stri = stri.casefold()#fa diventare tutta la stringa minuscola
    stri = stri.capitalize()#fa diventare la prima lettera maiuscola
    #up.message.reply_text("Parola da ricercare: " + stri)
    return stri

#Funzione lanciata al comando /start
def start(up, cont):
    info = up.message.from_user
    nome = info['first_name']
    up.message.reply_text("Ciao " + str(nome) +  ", per definire una parola digita: \n/def parola_da_definire (ES: /def virus)")

def getToken():
    t = tok()
    return t.getToken()

def main():
    print("In esecuzione! ")
    TOKEN = getToken()
    upd= Updater(TOKEN, use_context=True)
    disp=upd.dispatcher
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("def", defineFunction))
    upd.start_polling()#Chiede a telegram se ci sono nuovi messaggi
    upd.idle() #permette al bot di smettere la sua esecuzione tramite shortcut da tastiera CRTL + C (interrupt)

if __name__=='__main__':
    main() #Lancia la funzione main 