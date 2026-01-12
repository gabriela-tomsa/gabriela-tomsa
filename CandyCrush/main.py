import argparse  # importam modulul pentru citirea argumentelor din linia de comanda
import csv       # importam modulul pentru a scrie fisierul CSV
import os        # importam modulul pentru lucrul cu fisiere si directoare
import random    # importam modulul pentru generare de numere aleatoare

# scoruri pentru diferite tipuri de formatiuni
SCOR_LINIE_3 = 5    # puncte pentru o linie de 3
SCOR_LINIE_4 = 10   # puncte pentru o linie de 4
SCOR_LINIE_5 = 50   # puncte pentru o linie de 5
SCOR_L = 20         # puncte pentru o forma L
SCOR_T = 30         # puncte pentru o forma T

# patternuri pentru forma L relativ la un "centru" (0,0)
PATRON_L = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],      # L orientat intr-o directie
    [(-2, 0), (-1, 0), (0, 0), (0, 1), (0, 2)],    # L rotit
    [(-2, 0), (-1, 0), (0, -2), (0, -1), (0, 0)],  # L rotit
    [(0, -2), (0, -1), (0, 0), (1, 0), (2, 0)],    # L rotit
]

# patternuri pentru forma T relativ la un "centru" (0,0)
PATRON_T = [
    [(-1, 0), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (1, 0)],  # T in pozitie orizontala
    [(-2, 0), (-1, 0), (0, -1), (0, 0), (0, 1), (1, 0), (2, 0)],  # T in pozitie verticala
]


def este_in_tabla(tabla, r, c):
    """Verifica daca pozitia (r,c) este in interiorul tablei."""
    return 0 <= r < len(tabla) and 0 <= c < len(tabla[0])  # intoarce True daca randul si coloana sunt valide


def creeaza_tabla_random(randuri, coloane):
    """Creeaza o tabla cu valori aleatoare intre 1 si 4."""
    return [[random.randint(1, 4) for _ in range(coloane)] for _ in range(randuri)]  # lista de liste cu valori 1..4


def copiaza_tabla(tabla):
    """Creeaza o copie a tablei."""
    return [rand[:] for rand in tabla]  # copiem fiecare rand al listei


# -------- detectie formatiuni -------- #

def detecteaza_linii(tabla):
    """Detecteaza linii orizontale si verticale de minim 3 elemente egale."""
    formatiuni = []                               # lista cu formatiunile gasite
    nr_randuri, nr_coloane = len(tabla), len(tabla[0])  # dimensiunea tablei

    # cautam pe orizontala
    for r in range(nr_randuri):                   # parcurgem fiecare rand
        c = 0                                     # pornim de la coloana 0
        while c < nr_coloane:                     # cat timp suntem in interiorul randului
            valoare = tabla[r][c]                 # valoarea din celula curenta
            if valoare == 0:                      # daca este gol (0), sarim peste
                c += 1                            # trecem la coloana urmatoare
                continue                          # sarim la urmatoarea iteratie
            start = c                             # retinem coloana de start a secventei
            while c + 1 < nr_coloane and tabla[r][c + 1] == valoare:  # cat timp urmatoarea celula este egala
                c += 1                            # avansam coloana
            lungime = c - start + 1               # calculam lungimea secventei
            if lungime >= 3:                      # daca avem macar 3 la rand
                if lungime >= 5:                  # daca sunt cel putin 5
                    lungime_efectiva = 5          # folosim 5 pentru scor
                elif lungime == 4:                # daca sunt exact 4
                    lungime_efectiva = 4          # folosim 4 pentru scor
                else:                             # altfel sunt exact 3
                    lungime_efectiva = 3          # folosim 3 pentru scor
                celule = [(r, start + i) for i in range(lungime_efectiva)]  # lista cu celulele din formatiune
                if lungime_efectiva == 3:         # alegem scorul in functie de lungime
                    scor = SCOR_LINIE_3           # scor linie de 3
                elif lungime_efectiva == 4:       # pentru linie de 4
                    scor = SCOR_LINIE_4           # scor linie de 4
                else:                             # pentru linie de 5
                    scor = SCOR_LINIE_5           # scor linie de 5
                formatiuni.append({               # adaugam formatiunea gasita in lista
                    "score": scor,                # scorul formatiunii
                    "cells": celule,              # celulele implicate
                    "type": "LINE",               # tipul este linie
                })
            c += 1                                # trecem la urmatoarea coloana

    # cautam pe verticala
    for c in range(nr_coloane):                   # parcurgem fiecare coloana
        r = 0                                     # pornim de la primul rand
        while r < nr_randuri:                     # cat timp suntem in interiorul coloanei
            valoare = tabla[r][c]                 # valoarea curenta din tabla
            if valoare == 0:                      # daca este gol
                r += 1                            # trecem la urmatorul rand
                continue                          # sarim la urmatoarea iteratie
            start = r                             # retinem randul de start
            while r + 1 < nr_randuri and tabla[r + 1][c] == valoare:  # cat timp urmatorul rand are aceeasi valoare
                r += 1                            # avansam pe randuri
            lungime = r - start + 1               # lungimea secventei verticale
            if lungime >= 3:                      # daca avem cel putin 3
                if lungime >= 5:                  # daca avem cel putin 5
                    lungime_efectiva = 5          # folosim 5
                elif lungime == 4:                # daca sunt exact 4
                    lungime_efectiva = 4          # folosim 4
                else:                             # altfel sunt 3
                    lungime_efectiva = 3          # folosim 3
                celule = [(start + i, c) for i in range(lungime_efectiva)]  # construim lista de celule
                if lungime_efectiva == 3:         # alegem scorul dupa lungime
                    scor = SCOR_LINIE_3           # scor pentru 3
                elif lungime_efectiva == 4:       # scor pentru 4
                    scor = SCOR_LINIE_4           # punctaj linie 4
                else:                             # scor pentru 5
                    scor = SCOR_LINIE_5           # punctaj linie 5
                formatiuni.append({               # adaugam formatiunea in lista
                    "score": scor,                # scor
                    "cells": celule,              # celule
                    "type": "LINE",               # tip linie
                })
            r += 1                                # trecem la randul urmator

    return formatiuni                             # intoarcem lista de formatiuni gasite


def detecteaza_L_T(tabla):
    """Detecteaza formatiuni L si T in tabla."""
    formatiuni = []                               # lista cu formatiuni L sau T
    nr_randuri, nr_coloane = len(tabla), len(tabla[0])  # dimensiunea tablei

    for r in range(nr_randuri):                   # parcurgem fiecare rand
        for c in range(nr_coloane):              # parcurgem fiecare coloana
            valoare = tabla[r][c]                # valoarea din celula curenta
            if valoare == 0:                     # daca este gol, sarim
                continue                         # trecem la urmatoarea coloana

            # calculam cat de lunga este linia orizontala prin (r,c)
            cnt_oriz = 1                         # numar minim de elemente orizontale (include celula curenta)
            cc = c - 1                           # ne uitam la stanga
            while cc >= 0 and tabla[r][cc] == valoare:  # cat timp valorile la stanga sunt egale
                cnt_oriz += 1                    # crestem numarul
                cc -= 1                          # mergem mai la stanga
            cc = c + 1                           # ne uitam la dreapta
            while cc < nr_coloane and tabla[r][cc] == valoare:  # cat timp valorile la dreapta sunt egale
                cnt_oriz += 1                    # crestem numarul
                cc += 1                          # mergem mai la dreapta

            # calculam cat de lunga este linia verticala prin (r,c)
            cnt_vert = 1                         # numar minim de elemente verticale
            rr = r - 1                           # ne uitam in sus
            while rr >= 0 and tabla[rr][c] == valoare:  # cat timp valorile de sus sunt egale
                cnt_vert += 1                    # crestem numarul
                rr -= 1                          # urcam mai sus
            rr = r + 1                           # ne uitam in jos
            while rr < nr_randuri and tabla[rr][c] == valoare:  # cat timp valorile de jos sunt egale
                cnt_vert += 1                    # crestem numarul
                rr += 1                          # coboram mai jos

            if cnt_oriz < 3 or cnt_vert < 3:     # daca nu avem cel putin 3 orizontal si vertical
                continue                         # nu putem avea L sau T centrat aici

            # verificam patternurile de L
            for pattern in PATRON_L:             # pentru fiecare model de L
                celule = []                      # lista pentru celulele din L
                ok = True                        # presupunem ca este valid
                for dr, dc in pattern:           # parcurgem fiecare deplasare din pattern
                    rr, cc = r + dr, c + dc      # calculam pozitia efectiva in tabla
                    if not este_in_tabla(tabla, rr, cc) or tabla[rr][cc] != valoare:  # daca iese din tabla sau nu are aceeasi valoare
                        ok = False               # marcam ca nu este valid
                        break                    # oprim verificarea pentru acest pattern
                    celule.append((rr, cc))      # adaugam celula in lista
                if ok:                           # daca patternul e valid
                    formatiuni.append({          # adaugam formatiunea L
                        "score": SCOR_L,         # scor pentru L
                        "cells": celule,         # celulele din L
                        "type": "L",             # tip L
                    })

            # verificam patternurile de T
            for pattern in PATRON_T:             # pentru fiecare model de T
                celule = []                      # lista de celule pentru T
                ok = True                        # presupunem ca este valid
                for dr, dc in pattern:           # parcurgem fiecare deplasare
                    rr, cc = r + dr, c + dc      # calculam pozitia in tabla
                    if not este_in_tabla(tabla, rr, cc) or tabla[rr][cc] != valoare:  # verificam limite si valoare
                        ok = False               # pattern invalid
                        break                    # oprim verificarea
                    celule.append((rr, cc))      # adaugam celula
                if ok:                           # daca patternul este valid
                    formatiuni.append({          # adaugam formatiunea T
                        "score": SCOR_T,         # scor pentru T
                        "cells": celule,         # celulele din T
                        "type": "T",             # tip T
                    })

    return formatiuni                             # intoarcem toate formatiunile L si T gasite


# -------- eliminare + gravitatie + reumplere -------- #

def elimina_formatiuni(tabla, formatiuni):
    """Elimina formatiunile din tabla, respectand regula anti-dublare."""
    formatiuni = sorted(formatiuni, key=lambda x: x["score"], reverse=True)  # sortam descrescator dupa scor
    celule_folosite = set()                         # set cu celule deja folosite in alte formatiuni
    celule_de_sters = set()                         # set cu celule care vor fi sterse (puse pe 0)
    total_scor = 0                                  # totalul de puncte castigate in acest pas

    for form in formatiuni:                         # parcurgem fiecare formatiune
        celule = form["cells"]                      # lista de celule din formatiune
        if any(c in celule_folosite for c in celule):  # daca vreo celula este deja folosita
            continue                                # sarim peste formatiunea asta
        total_scor += form["score"]                 # adaugam scorul formatiunii
        for c in celule:                            # pentru fiecare celula din formatiune
            celule_folosite.add(c)                  # marcam ca folosita
            celule_de_sters.add(c)                  # o adaugam in lista de sters

    for r, c in celule_de_sters:                    # parcurgem celulele care trebuie sterse
        tabla[r][c] = 0                             # punem 0 (gol) pe acele pozitii

    return total_scor                               # intoarcem totalul de puncte castigate


def aplica_gravitatie(tabla):
    """Aplica gravitatia: bomboanele cad in jos pe coloane."""
    nr_randuri, nr_coloane = len(tabla), len(tabla[0])   # dimensiunile tablei
    for c in range(nr_coloane):                          # pentru fiecare coloana
        valori = []                                      # lista cu valori nenule din coloana
        for r in range(nr_randuri - 1, -1, -1):          # parcurgem coloana de jos in sus
            if tabla[r][c] != 0:                         # daca celula nu este goala
                valori.append(tabla[r][c])               # o adaugam in lista de valori
        r = nr_randuri - 1                               # pornim de jos
        for v in valori:                                 # pentru fiecare valoare gasita
            tabla[r][c] = v                              # o punem la baza coloanei
            r -= 1                                       # urcam un rand
        while r >= 0:                                    # restul randurilor de sus
            tabla[r][c] = 0                              # le punem pe 0 (gol)
            r -= 1                                       # urcam mai sus


def reumple_tabla(tabla):
    """Pune bomboane noi (1..4) acolo unde tabla are 0."""
    nr_randuri, nr_coloane = len(tabla), len(tabla[0])   # dimensiuni
    for r in range(nr_randuri):                          # pentru fiecare rand
        for c in range(nr_coloane):                      # pentru fiecare coloana
            if tabla[r][c] == 0:                         # daca celula este goala
                tabla[r][c] = random.randint(1, 4)       # punem o valoare aleatoare intre 1 si 4


def rezolva_cascade(tabla):
    """Rezolva cascadele: detectie formatiuni, eliminare, gravitatie, reumplere, pana nu mai sunt formatiuni."""
    numar_cascade = 0                                    # numarul de cascade
    puncte_castigate = 0                                 # total puncte castigate in toate cascadele
    while True:                                          # bucla pana cand nu mai avem formatiuni
        linii = detecteaza_linii(tabla)                  # detectam mai intai liniile
        if not linii:                                    # daca nu avem nici o linie
            break                                        # nu mai avem formatiuni, oprim bucla
        formatiuni_L_T = detecteaza_L_T(tabla)           # detectam si formatiunile de tip L si T
        formatiuni = linii + formatiuni_L_T              # combinam toate formatiunile

        castig = elimina_formatiuni(tabla, formatiuni)   # eliminam formatiunile si aflam punctele castigate
        puncte_castigate += castig                       # adaugam la total
        aplica_gravitatie(tabla)                         # aplicam gravitatia
        reumple_tabla(tabla)                             # reumplem cu bomboane noi
        numar_cascade += 1                               # crestem numarul de cascade

    return numar_cascade, puncte_castigate               # intoarcem cate cascade au fost si cate puncte s-au castigat


def are_linie_la(tabla, r, c):
    """Verifica daca in jurul celulei (r,c) se formeaza o linie de minim 3."""
    nr_randuri, nr_coloane = len(tabla), len(tabla[0])   # dimensiunile tablei
    if not este_in_tabla(tabla, r, c):                   # daca (r,c) este in afara tablei
        return False                                     # nu avem linie
    valoare = tabla[r][c]                                # luam valoarea din celula
    if valoare == 0:                                     # daca este gol
        return False                                     # nu putem avea linie

    # verificam pe orizontala
    cnt = 1                                              # cel putin 1 (celula curenta)
    cc = c - 1                                           # mergem la stanga
    while cc >= 0 and tabla[r][cc] == valoare:           # cat timp la stanga sunt aceleasi valori
        cnt += 1                                         # marim numarul
        cc -= 1                                          # mai la stanga
    cc = c + 1                                           # mergem la dreapta
    while cc < nr_coloane and tabla[r][cc] == valoare:   # cat timp la dreapta sunt aceleasi valori
        cnt += 1                                         # marim numarul
        cc += 1                                          # mai la dreapta
    if cnt >= 3:                                         # daca avem cel putin 3 la orizontala
        return True                                      # exista o linie

    # verificam pe verticala
    cnt = 1                                              # resetam numarul pentru verticala
    rr = r - 1                                           # mergem in sus
    while rr >= 0 and tabla[rr][c] == valoare:           # cat timp sus sunt aceleasi valori
        cnt += 1                                         # marim numarul
        rr -= 1                                          # mai sus
    rr = r + 1                                           # mergem in jos
    while rr < nr_randuri and tabla[rr][c] == valoare:   # cat timp jos sunt aceleasi valori
        cnt += 1                                         # marim numarul
        rr += 1                                          # mai jos
    return cnt >= 3                                      # intoarcem True daca sunt cel putin 3 pe verticala


def gaseste_swap_valid(tabla):
    """Cauta o mutare (swap) valida care creeaza cel putin o linie de 3."""
    nr_randuri, nr_coloane = len(tabla), len(tabla[0])       # dimensiunile tablei
    for r in range(nr_randuri):                              # parcurgem randurile
        for c in range(nr_coloane):                          # parcurgem coloanele
            # incercam sa schimbam cu dreapta
            if c + 1 < nr_coloane and tabla[r][c] != tabla[r][c + 1]:  # daca exista vecin la dreapta si valorile sunt diferite
                tabla[r][c], tabla[r][c + 1] = tabla[r][c + 1], tabla[r][c]  # facem swap temporar
                if are_linie_la(tabla, r, c) or are_linie_la(tabla, r, c + 1):  # daca dupa swap apare o linie
                    tabla[r][c], tabla[r][c + 1] = tabla[r][c + 1], tabla[r][c]  # refacem tabla la forma initiala
                    return r, c, r, c + 1                                  # intoarcem coordonatele mutarii
                tabla[r][c], tabla[r][c + 1] = tabla[r][c + 1], tabla[r][c]  # refacem swap-ul daca nu e bun

            # incercam sa schimbam cu jos
            if r + 1 < nr_randuri and tabla[r][c] != tabla[r + 1][c]:     # daca exista vecin in jos si valorile sunt diferite
                tabla[r][c], tabla[r + 1][c] = tabla[r + 1][c], tabla[r][c]  # facem swap temporar
                if are_linie_la(tabla, r, c) or are_linie_la(tabla, r + 1, c):  # daca se formeaza o linie
                    tabla[r][c], tabla[r + 1][c] = tabla[r + 1][c], tabla[r][c]  # refacem tabla
                    return r, c, r + 1, c                                      # intoarcem mutarea
                tabla[r][c], tabla[r + 1][c] = tabla[r + 1][c], tabla[r][c]    # refacem swap-ul

    return None                                             # daca nu exista nici o mutare valida, intoarcem None


# -------- jocuri predefinite (optional) -------- #

def incarca_table_predefinite(cale, randuri, coloane):
    """Incarca table predefinite dintr-un fisier text, daca exista."""
    liste_table = []                                        # lista cu toate tablele incarcate
    if not os.path.exists(cale):                            # daca fisierul nu exista
        return liste_table                                  # intoarcem lista goala

    tabla_curenta = []                                      # tabla pe care o construim acum
    with open(cale, "r", encoding="utf-8") as f:            # deschidem fisierul pentru citire
        for linie in f:                                     # parcurgem fiecare linie
            linie = linie.strip()                           # eliminam spatiile de la inceput si sfarsit
            if not linie:                                   # daca linia este goala
                if len(tabla_curenta) == randuri:           # daca am adunat exact numarul de randuri
                    liste_table.append(tabla_curenta)       # adaugam tabla in lista
                tabla_curenta = []                          # resetam tabla curenta
                continue                                    # trecem la urmatoarea linie
            parti = linie.split()                           # impartim linia in bucati separate prin spatiu
            if len(parti) != coloane:                       # daca numarul de coloane nu corespunde
                continue                                    # ignoram linia
            rand_valori = [int(x) for x in parti]           # convertim textul in numere intregi
            tabla_curenta.append(rand_valori)               # adaugam randul in tabla
            if len(tabla_curenta) == randuri:               # daca am ajuns la numarul de randuri
                liste_table.append(tabla_curenta)           # adaugam tabla
                tabla_curenta = []                          # resetam pentru urmatoarea tabla
    if len(tabla_curenta) == randuri:                       # daca dupa terminarea fisierului mai avem o tabla completa
        liste_table.append(tabla_curenta)                   # o adaugam
    return liste_table                                      # intoarcem lista de table predefinite


# -------- un singur joc -------- #

def ruleaza_un_joc(id_joc, randuri, coloane, tinta, tabla_initiala=None):
    """Ruleaza un singur joc Candy Crush automatizat."""
    if tabla_initiala is not None:                          # daca primim o tabla initiala predefinita
        tabla = copiaza_tabla(tabla_initiala)               # facem o copie a tablei initiale
    else:                                                   # altfel
        tabla = creeaza_tabla_random(randuri, coloane)      # cream o tabla aleatoare

    total_puncte = 0                                        # punctele acumulate in joc
    numar_mutari = 0                                        # numarul de swap-uri facute
    total_cascade = 0                                       # numarul total de cascade
    tinta_atinsa = False                                    # daca tinta de 10000 a fost atinsa
    mutari_pana_la_10000 = None                             # cate mutari au fost necesare pana la tinta

    # cascada initiala dupa generare
    numar_casc, castig = rezolva_cascade(tabla)             # rezolvam toate formatiunile initiale
    total_cascade += numar_casc                             # adaugam numarul de cascade
    total_puncte += castig                                  # adaugam punctele castigate

    if total_puncte >= tinta:                               # daca deja am atins tinta
        tinta_atinsa = True                                 # marcam ca tinta a fost atinsa
        mutari_pana_la_10000 = 0                            # 0 mutari pana la tinta
        return {                                            # intoarcem rezumatul jocului
            "game_id": id_joc,                              # id-ul jocului
            "points": total_puncte,                         # punctele totale
            "swaps": numar_mutari,                          # numarul de mutari
            "total_cascades": total_cascade,                # numarul de cascade
            "reached_target": tinta_atinsa,                 # daca am atins tinta
            "stopping_reason": "REACHED_TARGET",            # motivul opririi
            "moves_to_10000": mutari_pana_la_10000,         # mutari pana la tinta
        }

    while True:                                             # bucla principala de joc
        if total_puncte >= tinta:                           # daca am atins tinta
            tinta_atinsa = True                             # marcam tinta atinsa
            motiv = "REACHED_TARGET"                        # motiv oprire: tinta atinsa
            break                                           # iesim din bucla

        mutare = gaseste_swap_valid(tabla)                  # cautam o mutare valida
        if mutare is None:                                  # daca nu exista mutari valide
            tinta_atinsa = total_puncte >= tinta            # verificam daca tinta a fost atinsa sau nu
            motiv = "NO_MOVES"                              # motiv oprire: nu mai sunt mutari
            break                                           # iesim din bucla

        r1, c1, r2, c2 = mutare                             # coordonatele celor doua celule de schimbat
        tabla[r1][c1], tabla[r2][c2] = tabla[r2][c2], tabla[r1][c1]  # facem swap-ul efectiv
        numar_mutari += 1                                   # crestem numarul de mutari

        numar_casc, castig = rezolva_cascade(tabla)         # rezolvam cascadele dupa mutare
        total_cascade += numar_casc                         # adaugam cascadele
        total_puncte += castig                              # adaugam punctele castigate

        if total_puncte >= tinta and mutari_pana_la_10000 is None:  # daca am atins tinta pentru prima data
            mutari_pana_la_10000 = numar_mutari             # retinem cate mutari au fost necesare

    return {                                                # dupa ce jocul s-a terminat
        "game_id": id_joc,                                  # id joc
        "points": total_puncte,                             # puncte totale
        "swaps": numar_mutari,                              # mutari
        "total_cascades": total_cascade,                    # cascade totale
        "reached_target": tinta_atinsa,                     # daca tinta a fost atinsa
        "stopping_reason": motiv,                           # motiv oprire
        "moves_to_10000": mutari_pana_la_10000,             # mutari pana la tinta (sau None)
    }


def ruleaza_jocuri(numar_jocuri, randuri, coloane, tinta, foloseste_predefinite, cale_iesire):
    """Ruleaza mai multe jocuri si salveaza rezultatele in fisier CSV."""
    table_predefinite = []                                  # lista cu table predefinite
    if foloseste_predefinite:                               # daca este setata optiunea de predefinite
        table_predefinite = incarca_table_predefinite(      # incarcam tablele din fisier
            os.path.join("data", "predefined_boards.txt"),  # calea catre fisier
            randuri, coloane                                # dimensiunea tablelor
        )

    rezultate = []                                          # lista cu rezultatele pentru fiecare joc
    for id_joc in range(numar_jocuri):                      # parcurgem de la 0 la numar_jocuri - 1
        print(f"-> Jocul {id_joc + 1}/{numar_jocuri} incepe...")
        if table_predefinite:                               # daca avem table predefinite
            tabla_initiala = table_predefinite[id_joc % len(table_predefinite)]  # luam o tabla in functie de id
        else:                                               # daca nu avem predefinite
            tabla_initiala = None                           # vom genera aleator o tabla

        rezumat = ruleaza_un_joc(                           # rulam un joc
            id_joc,                                         # id-ul jocului
            randuri, coloane, tinta,                        # dimensiunea si tinta
            tabla_initiala                                  # tabla initiala (sau None)
        )
        rezultate.append(rezumat)                           # adaugam rezultatul in lista

    director_iesire = os.path.dirname(cale_iesire)          # extragem directorul din calea fisierului CSV
    if director_iesire:                                     # daca exista un director
        os.makedirs(director_iesire, exist_ok=True)         # il cream daca nu exista deja

    with open(cale_iesire, "w", newline="", encoding="utf-8") as f:  # deschidem fisierul CSV pentru scriere
        writer = csv.writer(f)                              # cream un writer CSV
        writer.writerow([                                   # scriem antetul CSV exact ca in cerinta
            "game_id", "points", "swaps", "total_cascades",
            "reached_target", "stopping_reason", "moves_to_10000",
        ])
        for rez in rezultate:                               # parcurgem fiecare rezultat
            writer.writerow([                               # scriem o linie in CSV
                rez["game_id"],                             # id joc
                rez["points"],                              # puncte
                rez["swaps"],                               # mutari
                rez["total_cascades"],                      # cascade totale
                str(rez["reached_target"]),                 # tinta atinsa (True/False)
                rez["stopping_reason"],                     # motiv oprire
                "" if rez["moves_to_10000"] is None else rez["moves_to_10000"],  # mutari pana la tinta sau gol
            ])

    total_puncte = sum(rez["points"] for rez in rezultate)  # suma punctelor pentru toate jocurile
    total_mutari = sum(rez["swaps"] for rez in rezultate)   # suma mutarilor pentru toate jocurile
    medie_puncte = total_puncte / numar_jocuri if numar_jocuri else 0  # media punctelor
    medie_mutari = total_mutari / numar_jocuri if numar_jocuri else 0  # media mutarilor

    jocuri_cu_tinta = [rez for rez in rezultate             # lista cu jocurile care au atins tinta
                       if rez["reached_target"] and rez["moves_to_10000"] is not None]
    if jocuri_cu_tinta:                                     # daca exista jocuri care au atins tinta
        medie_mutari_10000 = sum(                           # calculam media mutarilor pana la 10000
            rez["moves_to_10000"] for rez in jocuri_cu_tinta
        ) / len(jocuri_cu_tinta)
    else:                                                   # altfel
        medie_mutari_10000 = 0                              # media este 0 (nu are sens, dar punem 0)

    print(f"Jocuri rulate: {numar_jocuri}")                 # afisam cate jocuri s-au rulat
    print(f"Puncte medii: {medie_puncte:.2f}")              # afisam media punctelor
    print(f"Swap-uri medii: {medie_mutari:.2f}")            # afisam media mutarilor (swap-uri)
    if jocuri_cu_tinta:                                     # daca au fost jocuri cu tinta atinsa
        print(f"Swap-uri medii pana la 10000 (doar jocurile care au atins tinta): {medie_mutari_10000:.2f}")  # media
    else:                                                   # daca nu a atins niciun joc tinta
        print("Niciun joc nu a atins tinta de 10000 de puncte.")  # mesaj corespunzator

    print(f"\nRezultatele au fost salvate in: {cale_iesire}\n")  # afisam calea fisierului CSV


def citeste_argumente():
    """Citeste argumentele din linia de comanda."""
    parser = argparse.ArgumentParser(                       # cream un parser pentru argumente
        description="Automatizare joc Candy Crush 11x11"   # descrierea aplicatiei
    )
    parser.add_argument("--games", type=int, default=100)  # numarul de jocuri (implicit 100)
    parser.add_argument("--rows", type=int, default=11)    # numarul de randuri (implicit 11)
    parser.add_argument("--cols", type=int, default=11)    # numarul de coloane (implicit 11)
    parser.add_argument("--target", type=int, default=10000)  # tinta de puncte (implicit 10000)
    parser.add_argument("--input_predefined", action="store_true")  # daca folosim table predefinite
    parser.add_argument("--out", type=str, default=os.path.join( "summary.csv"))  # fisier CSV
    return parser.parse_args()                             # intoarcem argumentele citite


def main():
    """Functia principala a programului."""
    args = citeste_argumente()                             # citim argumentele din linia de comanda
    random.seed(42)                                        # setam o samanta fixa pentru aleator (determinism)
    ruleaza_jocuri(                                        # rulam toate jocurile
        args.games,                                        # numarul de jocuri
        args.rows,                                         # randuri
        args.cols,                                         # coloane
        args.target,                                       # tinta
        args.input_predefined,                             # daca folosim table predefinite
        args.out                                           # calea fisierului CSV
    )


if __name__ == "__main__":                                 # daca fisierul este rulat direct
    main()                                                 # apelam functia main