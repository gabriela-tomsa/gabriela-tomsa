import tkinter as tk
from tkinter import ttk
import random
import time
import threading


class VizualizatorSortare:
    def __init__(self, root):
        self.root = root  # Salvează referința la fereastra principală
        self.root.title("Sortare Vizualizată")  # Setează titlul ferestrei

        # Inițializează variabilele de bază
        self.lista = []  # Lista care va fi sortată
        self.algoritm = tk.StringVar(value="Bubble Sort")  # Algoritm de sortare selectat (implicit Bubble Sort)
        self.viteza = tk.IntVar(value=5)  # Viteza de sortare (1-10)
        self.numar_elemente = tk.IntVar(value=10)  # Numărul de elemente din listă
        self.pauza = False  # Flag pentru pauză
        self.sortare_in_curs = False  # Flag care indică dacă o sortare este în curs
        self.stop_event = threading.Event()  # Event pentru a opri thread-ul de sortare
        self.thread = None  # Variabilă pentru a stoca thread-ul de sortare

        # Dicționar pentru a lega algoritmii de funcțiile lor
        self.algoritmi = {
            "Bubble Sort": self.bubble_sort,
            "Insertion Sort": self.insertion_sort,
            "Selection Sort": self.selection_sort
        }

        # Creează widgeturile UI
        self.creeaza_widgeturi()

    def creeaza_widgeturi(self):
        # Crează un cadru pentru controale (butone, combobox-uri etc.)
        frame_controale = tk.Frame(self.root, padx=10, pady=10)
        frame_controale.pack(fill=tk.X)  # Adaugă cadrul în fereastra principală

        # Opțiune pentru selectarea algoritmului
        ttk.Label(frame_controale, text="Algoritm:").grid(row=0, column=0, padx=5)
        ttk.Combobox(frame_controale, textvariable=self.algoritm,
                     values=["Bubble Sort", "Insertion Sort", "Selection Sort"], state="readonly").grid(row=0, column=1,
                                                                                                        padx=5)

        # Opțiune pentru setarea vitezei de sortare
        ttk.Label(frame_controale, text="Viteză:").grid(row=0, column=2, padx=5)
        ttk.Spinbox(frame_controale, from_=1, to=10, textvariable=self.viteza, width=5).grid(row=0, column=3, padx=5)

        # Opțiune pentru setarea numărului de elemente din listă
        ttk.Label(frame_controale, text="Elemente:").grid(row=0, column=4, padx=5)
        ttk.Spinbox(frame_controale, from_=5, to=50, textvariable=self.numar_elemente, width=5).grid(row=0, column=5,
                                                                                                     padx=5)

        # Buton pentru generarea listei de numere
        ttk.Button(frame_controale, text="Generează", command=self.genereaza_date).grid(row=0, column=6, padx=5)

        # Buton pentru a începe sortarea
        ttk.Button(frame_controale, text="Începe", command=self.ruleaza_sortarea).grid(row=0, column=7, padx=5)

        # Buton pentru a pune sortarea pe pauză/reluare
        ttk.Button(frame_controale, text="Pauză/Reluare", command=self.pauza_si_rezolva).grid(row=0, column=8, padx=5)

        # Buton pentru resetarea aplicației
        ttk.Button(frame_controale, text="Resetează", command=self.reseteaza).grid(row=0, column=9, padx=5)

        # Crează un canvas pentru a desena grafic lista
        self.canvas = tk.Canvas(self.root, bg="white", height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def genereaza_date(self):
        # Generează o listă de numere aleatoare între 1 și 100
        self.lista = [random.randint(1, 100) for _ in range(self.numar_elemente.get())]
        self.deseneaza_date()  # Desenează lista pe canvas

    def deseneaza_date(self, highlight=None):
        # Șterge tot ce este pe canvas și desenează noile valori ale listei
        self.canvas.delete("all")
        highlight = highlight or []  # Evită ca highlight să fie None
        latime_bara = self.canvas.winfo_width() / len(self.lista)  # Lățimea fiecărei bare pe canvas
        max_valoare = max(self.lista)  # Cea mai mare valoare din listă

        # Desenează fiecare bară
        for i, valoare in enumerate(self.lista):
            x0 = i * latime_bara  # Poziția de start a barei pe axa X
            y0 = self.canvas.winfo_height() - (
                        valoare / max_valoare) * self.canvas.winfo_height()  # Poziția de start pe axa Y
            x1 = (i + 1) * latime_bara  # Poziția finală pe axa X
            y1 = self.canvas.winfo_height()  # Poziția finală pe axa Y
            culoare = "lightblue" if i not in highlight else "pink"  # Dacă elementul este în highlight, schimbă culoarea
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=culoare, outline="")  # Creează un dreptunghi pe canvas

    def ruleaza_sortarea(self):
        # Începe sortarea dacă lista există și sortarea nu este deja în curs
        if self.lista and not self.sortare_in_curs:
            self.stop_event.clear()  # Resetează event-ul pentru oprire
            self.sortare_in_curs = True  # Marchează că sortarea este în curs
            self.thread = threading.Thread(
                target=self.algoritmi[self.algoritm.get()])  # Creează un thread pentru sortare
            self.thread.start()  # Pornește thread-ul

    def bubble_sort(self):
        # Algoritmul de sortare Bubble Sort
        for i in range(len(self.lista) - 1):
            for j in range(len(self.lista) - i - 1):
                if self.lista[j] > self.lista[j + 1]:  # Dacă elementul curent este mai mare decât următorul
                    self.lista[j], self.lista[j + 1] = self.lista[j + 1], self.lista[j]  # Schimbă elementele
                    self.actualizeaza_si_pauza([j, j + 1])  # Actualizează vizualizarea și pune pauză
                if self.stop_event.is_set(): return  # Dacă trebuie oprit sortarea, ieși din funcție

    def insertion_sort(self):
        # Algoritmul de sortare Insertion Sort
        for i in range(1, len(self.lista)):
            key = self.lista[i]  # Elementul curent
            j = i - 1
            while j >= 0 and self.lista[j] > key:  # Caută locul pentru elementul curent
                self.lista[j + 1] = self.lista[j]  # Mută elementele mai mari cu o poziție
                j -= 1
                self.actualizeaza_si_pauza([j + 1, i])  # Actualizează vizualizarea
            self.lista[j + 1] = key  # Plasează elementul curent la locul său
            self.actualizeaza_si_pauza([j + 1])  # Actualizează vizualizarea
            if self.stop_event.is_set(): return  # Dacă trebuie oprit sortarea, ieși din funcție

    def selection_sort(self):
        # Algoritmul de sortare Selection Sort
        for i in range(len(self.lista)):
            min_idx = i  # Presupune că minimul este elementul curent
            for j in range(i + 1, len(self.lista)):
                if self.lista[j] < self.lista[min_idx]:  # Găsește minimul
                    min_idx = j
                self.actualizeaza_si_pauza([i, min_idx, j])  # Actualizează vizualizarea
            self.lista[i], self.lista[min_idx] = self.lista[min_idx], self.lista[i]  # Schimbă elementele
            self.actualizeaza_si_pauza([i, min_idx])  # Actualizează vizualizarea
            if self.stop_event.is_set(): return  # Dacă trebuie oprit sortarea, ieși din funcție

    def actualizeaza_si_pauza(self, highlight):
        # Actualizează vizualizarea și pune pauză între pași
        if self.pauza:  # Dacă pauza este activă, așteaptă până când este dezactivată
            while self.pauza:
                time.sleep(0.1)
        self.deseneaza_date(highlight)  # Redesenare cu highlight-ul curent
        self.root.update()  # Actualizează fereastra
        time.sleep(1.0 / self.viteza.get())  # Pauza invers proporțională cu viteza aleasă

    def pauza_si_rezolva(self):
        # Inversează starea pauzei
        self.pauza = not self.pauza

    def reseteaza(self):
        # Oprește sortarea și resetează totul
        self.stop_event.set()  # Semnalizează thread-ul să oprească sortarea
        if self.thread:  # Așteaptă să se termine thread-ul
            self.thread.join()
        self.lista = []  # Resetează lista
        self.canvas.delete("all")  # Șterge tot ce este pe canvas
        self.sortare_in_curs = False  # Oprește sortarea
        self.pauza = False  # Dezactivează pauza


# Program Principal
if __name__ == "__main__":
    root = tk.Tk()  # Creează fereastra principală
    app = VizualizatorSortare(root)  # Creează aplicația
    root.mainloop()  # Lansează aplicația
