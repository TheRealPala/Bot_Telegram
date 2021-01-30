from openpyxl import *
filename = "DataBase.xlsx" #nome del file exel da elaborare
sheetT = "Database" #nome del foglio da elaborare
sheetTNKW = "Nk" #nome del foglio per le parole non ancora definite
dir = load_workbook(filename)
sheet = dir[sheetT]


#Funzione di prova per scrivere un file xlsx
#def makeFile(f, s, str):
#dira = Workbook()
#file = dir.active
#file.title = s
#file["A4"] = str
#dira.save(f)

##########################
#Da finire: non funziona la scrittura sul secondo foglio (Nk)
def addNKW(s):
    try:
        #sh = dir.get_sheet_by_name(sheetTNKW)
        sh = dir[sheetTNKW]
    except:
        print("Non posso lavorare sul file perchè è già aperto dal sistema operativo!")
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

def findWord(stri):
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
        print("\nLa parola non è ancora presente nell'archivio!\nIl nostro team la aggiungerà il prima possibile!")
        addNKW(stri)
    else:
        print("La parola è presente!\nParola: "+ str(v) +"\nDefinizione: " + str(defi))    

def initRead(f, sh):
    dir = load_workbook(f)
    sheet = dir[sh]

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
def defineFunction():
    initRead(filename, sheetT)
    string = inputStr()
    string = string.capitalize()
    findWord(string)

if __name__ == "__main__":
    defineFunction()
   