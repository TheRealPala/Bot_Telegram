from openpyxl import *
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
filename = "DataBase.xlsx" #nome del file exel da elaborare
sheetT = "Database" #nome del foglio da elaborare
sheetTNKW = "Nk" #nome del foglio per le parole non ancora definite
TOKEN = "1524897969:AAFea-xo8G-xQvuoBhGUWXjQcdNAg7kQQpw"
dir = load_workbook(filename)
sheet = dir[sheetT]


#Funzione di prova per scrivere un file xlsx
#def makeFile(f, s, str):
#dira = Workbook()
#file = dir.active
#file.title = s
#file["A4"] = str
#dira.save(f)


def addNKW(s):
    try:
        #sh = dir.get_sheet_by_name(sheetTNKW)
        sh = dir[sheetTNKW]
    except:
        #print("Non posso lavorare sul file perchè è già aperto dal sistema operativo!")
        exit
    r = 1
    c = 1
    cmp = True
    while(sh.cell(r, c).value != None):
        if(sh.cell(r, c).value == s):
            cmp = False
            break
        r += 1
    r = 1
    if cmp:
        while(sh.cell(r, c).value != None):
            r += 1
        sh.cell(r, c, s)
        dir.save(filename)
        
def readFile(v, rows, coloumns): 
    v[0] = sheet.cell(rows, coloumns).value

def findWord(stri, up, cont):
    r = 2
    c = 1
    v = None
    defi = None
    while(sheet.cell(r, c).value != None):
        if(sheet.cell(r, c).value == stri):
            v = sheet.cell(r, c).value
            defi = sheet.cell(r, (c + 1)).value
            break
        else:
            r += 1
            v = None
    if(v == None):
        up.message.reply_text("\nLa parola non è ancora presente nell'archivio!\nIl nostro team la aggiungerà il prima possibile!")
        addNKW(stri)
    else:
        up.message.reply_text("La parola è presente!\nParola: "+ str(v) +"\nDefinizione: " + str(defi))    

def initRead(f, sh):
    dir = load_workbook(f)
    sheet = dir[sh]

'''
def inputStr():
    string = ""
    cmp = True
    while cmp:
        cmp = True
        string = input("\nInserire parola da ricercare: ")
        sn = input("Vuoi reinserire la parola da cercare? ")
        if(sn == "si" or sn == "Sì" or sn == "Si" or sn == "SI" or sn == "Si\'"):
            cmp = True
            continue
        elif(sn == "No" or sn == "NO" or sn == "no"):
            cmp = False
        else:
            print("Risposta non corretta!\nRiprova")
    return string
'''
def defineFunction(up, cont):
    initRead(filename, sheetT)
    string  = inputBot(up, cont)
    if(len(string) == 0 or string == "-1"):
        up.message.reply_text("Non hai inserito una parola da ricercare!\nSintassi: /definisci parola_da_definire")
    else:
        findWord(string, up, cont)

def inputBot(up, cont):
    stri = up.message.text
    if(stri == "/definisci"):
        return "-1"
    stri = stri.split()[1].strip()
    stri = stri.casefold()
    stri = stri.capitalize()
    up.message.reply_text("Parola da ricercare: " + stri)
    return stri

'''
def HelloBot(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    name = msg["from"]["first_name"]
    bot.sendMessage(chat_id, 'Ciao %s, \nQuesta è una prova del bot che definisce le parole!'%name)
    bot.sendMessage(chat_id, 'definisci per iniziare\n/quit per andarsene'%name)
    while True:
        content_type, chat_type, chat_id = telepot.glance(msg)
        txt = msg['text']
        if(txt == "definisci"):
            defineFunction()
        elif txt == "/quit":
            break
        else:
            bot.sendMessage(chat_id, 'Comando non disponibile!\n/start per iniziare\n/quit per andarsene'%name)
        
def Amain():
    msg = ""
    HelloBot(msg)
    if msg  == "/quit":
        bot.leaveChat()
    else:
        defineFunction()
'''

def start(up, cont):
    info = up.message.from_user
    nome = info['first_name']
    up.message.reply_text("Ciao" + str(nome) +  ", per definire una parola digita: \n/definisci parola_da_definire")


def main():
    upd= Updater(TOKEN, use_context=True)
    disp=upd.dispatcher
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("definisci", defineFunction))
    upd.start_polling()
    upd.idle()

if __name__=='__main__':
   main()