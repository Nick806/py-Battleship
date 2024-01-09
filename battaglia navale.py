"""

Significato dei simboli nelle tabelle:

    Tabella di attacco (caratteri):
        "O" = non noto / non ancora sparato
        "A" = Acqua
        "X" = Colpito ma non affondato
        "Y" = Colpito e affondato

    Tabella di difesa (int):
        0 = vuoto
        1 = nave da 2
        2 = nave da 2
        3 = nave da 2
        4 = nave da 3
        5 = nave da 3
        6 = nave da 4
        7 = nave da 4
        8 = nave da 5


"""
#definizioni

COLONNE = 10
RIGHE = 10

NAVI = [2,2,2,2,3,3,3,4,4,5]
#ogni numero corrisponde alla lunghezza di una nave


import random
import time


################################################################################
#Sezione con funzioni base e di gioco
################################################################################


#gerela la tabella con tutti i valori incogniti
def crea_tabella(righe, colonne, elementi):
    tabella = [[elementi for _ in range(colonne)] for _ in range(righe)]
    return tabella

#stampa la tabella su seriale
def stampa_tabella(tabella):
    for riga in tabella:
        for elemento in riga:
            print(elemento, end=" ")
        print()

def attacco(tabella_di_attacco, tabella_di_difesa, riga, colonna):
    riga -= 1
    colonna -= 1

    if tabella_di_attacco[riga][colonna] != "O":
        #queste coordinate sono già state colpite, mossa illegale
        return 0
    elif tabella_di_difesa[riga][colonna] == 0:
        tabella_di_attacco[riga][colonna] = "A"
    else:
        tabella_di_attacco[riga][colonna] = "X"

    return 1


def colpito_e_affondato(tabella_di_attacco, tabella_di_difesa, riga, colonna):

    riga -= 1
    colonna -= 1

    numero_barca = tabella_di_difesa[riga][colonna]

    if numero_barca == 0:
        return 0

    #controlla se ci sono pezzi di barca rimanenti
    for rig in range(len(tabella_di_difesa)):
        for col in range(len(tabella_di_difesa[0])):
            if tabella_di_difesa[rig][col] == numero_barca:
                if tabella_di_attacco[rig][col] == "O":
                    return 0
                    #se ci sono fine funzione

    #altrimenti continua
    #e cambia tutti i pezzi della barca con il simbolo colpito e affondato
    for rig in range(len(tabella_di_difesa)):
        for col in range(len(tabella_di_difesa[0])):
            if tabella_di_difesa[rig][col] == numero_barca:
                tabella_di_attacco[rig][col] = "Y"

    return 1


def win(tabella_di_attacco, tabella_di_difesa):

    #contiene tutte le parti ancora da colpire
    tabella_sovrapposizione = crea_tabella(len(tabella_di_attacco), len(tabella_di_attacco[0]), 0)

    #confronto le due tabelle
    for rig in range(len(tabella_sovrapposizione)):
        for col in range(len(tabella_sovrapposizione[0])):
            if tabella_di_attacco[rig][col] == "O":
                tabella_sovrapposizione[rig][col] = tabella_di_difesa[rig][col]

    #vedo se ci sono parti mancanti
    for rig in range(len(tabella_sovrapposizione)):
        for col in range(len(tabella_sovrapposizione[0])):
            if tabella_sovrapposizione[rig][col] != 0:
                return 0
                #non hai ancora vinto

    return 1 #hai vinto


def calcola_navi_rimanenti(tabella_di_attacco, tabella_di_difesa, navi):
    #contiene tutte le parti ancora da colpire
    tabella_sovrapposizione = crea_tabella(len(tabella_di_attacco), len(tabella_di_attacco[0]), 0)

    #confronto le due tabelle
    for rig in range(len(tabella_sovrapposizione)):
        for col in range(len(tabella_sovrapposizione[0])):
            if tabella_di_attacco[rig][col] == "O":
                tabella_sovrapposizione[rig][col] = tabella_di_difesa[rig][col]

    navi_rimanenti=[]
    for nav in range(len(navi)):
        if conta_elemento_in_tabella(tabella_sovrapposizione, nav+1) > 0:
            navi_rimanenti.append(navi[nav])

    return navi_rimanenti



#restituisce il numero di volte che un elemento è contenuto in una tabella
def conta_elemento_in_tabella(tabella, elemento):
    conteggio = 0

    for riga in tabella:
        conteggio += riga.count(elemento)

    return conteggio


################################################################################
#Sezione con funzioni di gioco
################################################################################

def gioco(tabella_attacco, tabella_difesa):

    while True:
        stampa_tabella(tabella_attacco)

        while True:
            try:
                riga = int(input("Riga: "))
                colonna = int(input("Colonna: "))
            except ValueError:
                print("Input non valido. Inserisci un numero intero.")
                continue  # Torna all'inizio del ciclo

            # Altri codici da eseguire se l'input è valido
            break  # Esce dal ciclo while se l'input è valido


        attacco(tabella_attacco, tabella_difesa, riga, colonna)
        colpito_e_affondato(tabella_attacco, tabella_difesa, riga, colonna)
        if win(tabella_attacco, tabella_difesa):
            print("Hai vinto!")
            return


def gioco_bot(tabella_attacco, tabella_difesa, navi):

    conta_mosse = 0

    while True:
        conta_mosse += 1

        """stampa_tabella(tabella_attacco)
        print("")
        print("Mossa numero " + str(conta_mosse))
        print("")
        #stampa_tabella(tabella_legal_mooves(tabella_attacco))
        #print("")
        #print(lista_legal_mooves(tabella_attacco))
        #print("")
        #print(len(lista_legal_mooves(tabella_attacco)))
        #print("")
        #print(calcola_navi_rimanenti(tabella_attacco, tabella_difesa, navi))
        #print("")
        stampa_tabella(calcola_tabella_probabilita(tabella_attacco, calcola_navi_rimanenti(tabella_attacco, tabella_difesa, navi)))
        print("")"""


        riga, colonna = my_bot(tabella_attacco, calcola_navi_rimanenti(tabella_attacco, tabella_difesa, navi))

        #print(str(riga) + " " + str(colonna))
        #print("")

        #time.sleep(0.05)


        attacco(tabella_attacco, tabella_difesa, riga, colonna)
        colpito_e_affondato(tabella_attacco, tabella_difesa, riga, colonna)
        if win(tabella_attacco, tabella_difesa):
            #print("Hai vinto!")
            return conta_mosse


################################################################################
#BOT
################################################################################			

def posiziona_navi(tabella, navi):
    righe = len(tabella)-1
    colonne = len(tabella[0])-1

    numero_nave = 0
    for lunghezza in navi:
        numero_nave += 1
        posizionata = False
        while not posizionata:
            orientamento = random.choice(['orizzontale', 'verticale'])
            if orientamento == 'orizzontale':
                colonna = random.randint(0, colonne - lunghezza)
                riga = random.randint(0, righe)
                if all(tabella[riga][colonna + i] == 0 for i in range(lunghezza)):
                    for i in range(lunghezza):
                        tabella[riga][colonna + i] = numero_nave
                    posizionata = True
            else:
                colonna = random.randint(0, colonne)
                riga = random.randint(0, righe - lunghezza)
                if all(tabella[riga + i][colonna] == 0 for i in range(lunghezza)):
                    for i in range(lunghezza):
                        tabella[riga + i][colonna] = numero_nave
                    posizionata = True


def estrai_navi(tabella):

    numero_barche = max(max(tabella, key=max))
    lista=[]

    for numero in range(numero_barche):
        lista.append(conta_elemento_in_tabella(tabella, numero+1))

    return lista


#circa 97.73176 tentativi in 21000 partite
def my_bot(tabella_attacco, navi_rimanenti):
    lista_mosse_legali = lista_legal_mooves(tabella_attacco)
    mossa = random.randint(0, len(lista_mosse_legali)-1)

    riga = lista_mosse_legali[mossa][0]
    colonna = lista_mosse_legali[mossa][1]

    return riga, colonna


#circa 77.907 tentativi in 20800 partite
def my_bot_2(tabella_attacco, navi_rimanenti):
    mosse_legali = tabella_legal_mooves(tabella_attacco)
    lista_mosse_legali = lista_legal_mooves(tabella_attacco)

    lista_X = tabella_to_lista(tabella_attacco, "X")

    if lista_X != 0:

        for indice in lista_X:
            indice1 = indice[0]
            indice2 = indice[1]

            intorno = coordinate_intorno(indice1, indice2)
            mossa = funzione_end(intorno, lista_mosse_legali)

            if len(mossa) > 0:
                riga = mossa[0][0]
                colonna = mossa[0][1]
                return riga, colonna


    mossa = random.randint(0, len(lista_mosse_legali)-1)

    riga = lista_mosse_legali[mossa][0]
    colonna = lista_mosse_legali[mossa][1]

    return riga, colonna


#circa 70.57 tentativi in 17700 partite
def my_bot_3(tabella_attacco, navi_rimanenti):
    tabella_mosse_legali = tabella_legal_mooves(tabella_attacco)
    lista_mosse_legali = lista_legal_mooves(tabella_attacco)



    lista_X = tabella_to_lista(tabella_attacco, "X")

    if lista_X != 0:

        for indice in lista_X:
            indice1 = indice[0]
            indice2 = indice[1]

            intorno = coordinate_intorno(indice1, indice2)
            mossa = funzione_end(intorno, lista_mosse_legali)

            if len(mossa) > 0:
                riga = mossa[0][0]
                colonna = mossa[0][1]
                return riga, colonna


    min_nave = min(navi_rimanenti)

    lista_rete = tabella_to_lista(genera_rete(len(tabella_attacco), len(tabella_attacco[0]), min_nave), 1)

    lista_mosse = funzione_end(lista_rete, lista_mosse_legali)

    mossa = random.randint(0, len(lista_mosse)-1)

    riga = lista_mosse[mossa][0]
    colonna = lista_mosse[mossa][1]

    return riga, colonna


#circa 64.6 mosse in 354 partite DIVERSE
def my_bot_4(tabella_attacco, navi_rimanenti):
    tabella_mosse_legali = tabella_legal_mooves(tabella_attacco)
    lista_mosse_legali = lista_legal_mooves(tabella_attacco)



    lista_X = tabella_to_lista(tabella_attacco, "X")

    if lista_X != 0:

        for indice in lista_X:
            indice1 = indice[0]
            indice2 = indice[1]

            intorno = coordinate_intorno(indice1, indice2)
            mossa = funzione_end(intorno, lista_mosse_legali)

            if len(mossa) > 0:
                riga = mossa[0][0]
                colonna = mossa[0][1]
                return riga, colonna


    """min_nave = min(navi_rimanenti)

    lista_rete = tabella_to_lista(genera_rete(len(tabella_attacco), len(tabella_attacco[0]), min_nave), 1)

    lista_mosse = funzione_end(lista_rete, lista_mosse_legali)

    mossa = random.randint(0, len(lista_mosse)-1)

    riga = lista_mosse[mossa][0]
    colonna = lista_mosse[mossa][1]"""

    return trova_coordinate_massimo(calcola_tabella_probabilita(tabella_attacco, navi_rimanenti))
	

def trova_coordinate_massimo(tabella):

    righe = len(tabella)
    colonne = len(tabella[0])

    indice_riga_massimo = 0
    indice_colonna_massimo = 0
    valore_massimo = tabella[0][0]

    for i in range(righe):
        for j in range(colonne):
            if tabella[i][j] > valore_massimo:
                valore_massimo = tabella[i][j]
                indice_riga_massimo = i
                indice_colonna_massimo = j

    return indice_riga_massimo+1, indice_colonna_massimo+1

def area_barca(righe, colonne, riga, colonna, lunghezza, orientamento):
	tabella = crea_tabella(righe, colonne, 0)
	if orientamento:
		#verticale
		for x in range(lunghezza):
			tabella[riga-1+x][colonna-1]=1
			
	else:
		#orizzontale
		for x in range(lunghezza):
			tabella[riga-1][colonna-1+x]=1
	
	return tabella


def elimina_duplicati(lista):
	nuova_lista = []
	for element in lista:
		if element not in nuova_lista:
			nuova_lista.append(element)
	
	return nuova_lista


def lista_con_tutte_le_navi(righe, colonne, navi_rimanenti):
	navi = elimina_duplicati(navi_rimanenti)
	lista = []
	
	for lunghezza in navi:
		for rig in range(righe-lunghezza+1):
			for col in range(colonne):
				lista.append([rig+1,col+1,lunghezza,1])
		for col in range(colonne-lunghezza+1):
			for rig in range(righe):
				lista.append([rig+1,col+1,lunghezza,0])
	
	return lista


def lista_navi_possibili(tab_attacco, lista_tutte_navi):
	lista_nav_possibili = []
	for nave in lista_tutte_navi:
		posizionata = True
		tab_nave = area_barca(len(tab_attacco), len(tab_attacco[0]), nave[0], nave[1], nave[2], nave[3])
		
		for indice1,lis in enumerate(tab_nave):
			for indice2,elemento in enumerate(lis):
				if elemento: #se è 1 c'è una barca
					if (tab_attacco[indice1][indice2] == "A") or (tab_attacco[indice1][indice2] == "Y"):
						posizionata = False
						break
			if not posizionata:
				break
	
		if posizionata:
			lista_nav_possibili.append(nave)
	
	return lista_nav_possibili


def tabella_probabilita(righe, colonne, lista_navi_possibili, lista_navi_mancanti):
	tabella = crea_tabella(righe, colonne, 0)
	
	lunghezza_navi_possibili = []
	for nave in lista_navi_possibili:
		lunghezza_navi_possibili.append(nave[2])
	
	navi_esistenti = elimina_duplicati(lista_navi_mancanti)
	
	for nave in navi_esistenti:
		mancanti = lista_navi_mancanti.count(nave)
		possibili = lunghezza_navi_possibili.count(nave)
		
		probabilita = mancanti/possibili
		
		for nave_possibile in lista_navi_possibili:
			if nave_possibile[2] == nave:
				tab_nave = area_barca(righe, colonne, nave_possibile[0], nave_possibile[1], nave_possibile[2], nave_possibile[3])
				
				for indice1,lis in enumerate(tab_nave):
					for indice2,elemento in enumerate(lis):
						if elemento: #se è 1 c'è una barca
							tabella[indice1][indice2] += probabilita
	return tabella

	

def calcola_tabella_probabilita(tab_attacco, navi_rimanenti):
	righe = len(tab_attacco)
	colonne = len(tab_attacco[0])
	
	return tabella_probabilita(righe, colonne, lista_navi_possibili(tab_attacco, lista_con_tutte_le_navi(righe, colonne, navi_rimanenti)), navi_rimanenti)
	
	
def genera_rete(righe, colonne, dimensione_nave):
    tabella = crea_tabella(righe, colonne, 0)
    for r in range(righe):
        for c in range(colonne):
            if (c+r)%dimensione_nave==0:
                tabella[r][c] = 1
    return tabella


def funzione_end(tab1, tab2):
    elementi_comuni = []
    for t1 in tab1:
        for t2 in tab2:
            if t1 == t2:
                elementi_comuni.append(t1)

    return elementi_comuni


def coordinate_intorno(x, y):
    intorno = [
        [x - 1, y],  # Sinistra
        [x + 1, y],  # Destra
        [x, y - 1],  # Sopra
        [x, y + 1]   # Sotto
    ]
    return intorno

def tabella_to_lista(tabella, elemento):
    coordinate = []
    for indice1, lista in enumerate(tabella):
        for indice2, valore in enumerate(lista):
            if valore == elemento:
                coordinate.append([indice1+1, indice2+1])
    return coordinate



#tabella con tutte le mosse legali (0 = non legale, 1 = legale)
def tabella_legal_mooves(tabella_attacco):
    tabella = crea_tabella(len(tabella_attacco), len(tabella_attacco[0]), 0)

    for rig in range(len(tabella)):
        for col in range(len(tabella[0])):
            if tabella_attacco[rig][col] == "O":
                tabella[rig][col] = 1

    return tabella

#lista di mosse legali = [righe],[colonne]
def lista_legal_mooves(tabella_attacco):
    tabella = tabella_legal_mooves(tabella_attacco)
    lista=[]
    for rig in range(len(tabella)):
        for col in range(len(tabella[0])):
            if tabella [rig][col] == 1:
                lista.append([rig+1,col+1])

    return lista


def loop():
    conta_giochi = 0
    somma_mosse = 0

    tabella_difesa = crea_tabella(RIGHE, COLONNE, 0)
    navi = NAVI
    posiziona_navi(tabella_difesa, navi)


    while True:
        conta_giochi += 1

        if conta_giochi%10 == 0:
            tabella_difesa = crea_tabella(RIGHE, COLONNE, 0)
            posiziona_navi(tabella_difesa, navi)

        tabella_attacco = crea_tabella(RIGHE, COLONNE, "O")

        mosse = gioco_bot(tabella_attacco, tabella_difesa, navi)

        somma_mosse += mosse

        #stampa_tabella(tabella_attacco)

        if conta_giochi%100 == 0:
            print(str(somma_mosse/conta_giochi) + " -   " + str(mosse)+ "   -   " + str(conta_giochi))

        #if mosse < 80:
        #    print(str(mosse)+ "  " + str(conta_giochi))
        #    return



if __name__ == "__main__":



    """tabella_attacco = crea_tabella(RIGHE, COLONNE, "O")
    tabella_difesa = crea_tabella(RIGHE, COLONNE, 0)
    navi = NAVI

    posiziona_navi(tabella_difesa, navi)

    stampa_tabella(tabella_difesa)
    print("")

    gioco_bot(tabella_attacco, tabella_difesa, navi)

    #gioco(tabella_attacco, tabella_difesa)

    stampa_tabella(tabella_attacco)"""

    loop()

    #stampa_tabella(genera_rete(RIGHE, COLONNE, 3))
    #input("Finito")


