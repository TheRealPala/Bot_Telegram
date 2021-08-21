import sys
from os import *
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dbHTTP import *
from tok import *
TOKEN = ""  # token di BotFather


def findWord(word, up, cont):
    db = DB()  # Istanza della classe Db definita in dbHTTP.py
    js = db.getJson(word)
    tmp, number = db.isThereWord(js)
    if(tmp == True):
        lang = db.getLanguage(js)
        if(lang == "IT"):
            up.message.reply_text(db.makeMsgIT(word, js))
        elif(lang == "EN"):
            up.message.reply_text(db.makeMsgEN(word, js))
        else:
            up.message.reply_text(db.makeMsgIT(word, js))
            up.message.reply_text(db.makeMsgEN(word, js))
    elif(tmp == 2):
        up.message.reply_text(
            "La parola non è presente nel database ma è stata proposta per l'inserimento!")
    elif(tmp == 3):
        up.message.reply_text(
            "La parola non è presente nel database ma è stata cercata per ben " + str(number) + " volte!")
    else:
        up.message.reply_text(
            "Parola non trovata :(\nIl nostro team la inserirà il prima possibile!")

# Funzione che viene lanciata al comando /define parola


def defineFunction(up, cont):
    string = inputBot(up, cont)  # ottiene la parola da ricercare
    string = string.strip()  # Elimina spazi bianchi da inizio e fine stringa!
    print("Parola richiesta: " + str(string))
    # se la parola è vuota o si è verificato qualche errore nell'input stampa il seguente errore
    if(len(string) == 0 or string == "-1"):
        up.message.reply_text(
            "Non hai inserito una parola da ricercare!\nSintassi: /def parola_da_definire")
    else:  # altrimenti cerca la parola nel database
        findWord(string, up, cont)  # Gestisce DB per cercare la parola


def delStr(buf, dele):
    if(buf == dele):
        return "-1"
    la = buf.split(" ")
    lb = dele.split(" ")
    lc = [x for x in la if x not in lb]
    stri = " ".join(lc)
    stri = stri.strip()  # Elimina spazi bianchi da inizio e fine stringa!
    return stri


# Funzione che, dato il comando, estrapola e fornisce la parola/le parole da cercare nel database.
def inputBot(up, cont):
    buf = up.message.text  # ottiene tutta la stringa del comando
    dele = "/def"
    if(buf == dele):
        return "-1"
    la = buf.split(" ")
    lb = dele.split(" ")
    # ciclo per gestire le parole con lo spazio ("San Valentino")
    lc = [x for x in la if x not in lb]
    # Prende tutte le parole presenti nella lista, le unisce in una sola stringa e le separa con il carattere " " ('32[10]', '0x20')
    stri = " ".join(lc)
    stri = stri.upper()
    #up.message.reply_text("Parola da ricercare: " + stri)
    return stri

# Funzione lanciata al comando /start


def start(up, cont):
    info = up.message.from_user
    nome = info['first_name']
    up.message.reply_text(
        "Ciao " + str(nome) + " !\nPer definire una parola digita: \n/def parola_da_definire (ES: /def virus)")


def getToken():
    t = tok()
    # Stampa variabili di ambiente
    try:
        print("Stampa variabili di ambiente: \nToken: " +
              str(t.getTokenEnv()) + "\tUrl: " + str(t.getUrlEnv()))
    except:
        print("\n\nERRORE!\nVariabili di ambiente non rilevate!\nPer editare le variabili di ambiente scommentare e modificare le ULTIME due righe del file DEL CONTAINER situtato nella directory: /root/.bashrc\nIl programma terminera' automaticamente per evitare utlteriori errori!\n\n")
        sys.exit()
    return t.getTokenEnv()


def main():
    print("In esecuzione! ")
    TOKEN = getToken()
    upd = Updater(TOKEN, use_context=True)
    disp = upd.dispatcher
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("def", defineFunction))
    upd.start_polling()  # Chiede a telegram se ci sono nuovi messaggi
    upd.idle()  # permette al bot di smettere la sua esecuzione tramite shortcut da tastiera CRTL + C (interrupt)


if __name__ == '__main__':
    main()  # Lancia la funzione main
