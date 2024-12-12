import turtle
import time

# Funcție pentru a desena barele corespunzătoare valorilor din listă
def deseneaza_bare(lista_valori, index_evidentiat=None, culoare_bara="skyblue"):
    turtle.clear()  # Șterge desenul anterior
    latime_bara = 400 // len(lista_valori)  # Calculează lățimea fiecărei bare
    turtle.penup()  # Ridică stiloul pentru a evita trasarea de linii inutile

    for index, inaltime in enumerate(lista_valori):  # Parcurge fiecare valoare și indice din listă
        turtle.goto(-200 + index * latime_bara, -200)  # Setează poziția de start a barei curente
        turtle.fillcolor("hotpink" if index == index_evidentiat else culoare_bara)  # Alege culoarea barei
        turtle.begin_fill()  # Începe desenarea și umplerea barei
        for directie, distanta in [(90, inaltime * 20), (0, latime_bara - 2), (270, inaltime * 20)]:  # Desenează laturile barei
            turtle.setheading(directie)  # Setează direcția stiloului
            turtle.forward(distanta)  # Mișcă stiloul în direcția și distanța specificată
        turtle.end_fill()  # Finalizează umplerea barei

# Funcție pentru a vizualiza procesul de sortare cu bule
def vizualizare_sortare_bule(lista_valori):
    turtle.speed(0)  # Setează viteza maximă a animației
    for pas in range(len(lista_valori)):  # Parcurge fiecare pas al sortării
        for i in range(len(lista_valori) - pas - 1):  # Compară elementele care nu sunt încă sortate
            deseneaza_bare(lista_valori, i)  # Desenează lista cu bara curentă evidențiată
            time.sleep(0.5)  # Pauză pentru a vizualiza modificarea
            if lista_valori[i] > lista_valori[i + 1]:  # Verifică dacă două elemente sunt în ordine greșită
                lista_valori[i], lista_valori[i + 1] = lista_valori[i + 1], lista_valori[i]  # Schimbă locurile elementelor
    deseneaza_bare(lista_valori, "lightgreen")  # Desenează lista sortată cu bare verzi
    time.sleep(2)  # Pauză pentru a vedea rezultatul final
    turtle.done()  # Închide fereastra Turtle

# Lista de valori de sortat
lista_valori = [8, 3, 5, 2, 9, 1, 4]  # Inițializează lista de test
vizualizare_sortare_bule(lista_valori)  # Apelează funcția de sortare și vizualizare
