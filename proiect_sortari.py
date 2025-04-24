import tkinter as tk
from tkinter import ttk
import random
import time
import threading


class VizualizatorSortare:
    def __init__(self, root):
        self.root = root
        self.root.title("Sortare Vizualizată")

        # Inițializează variabilele de bază
        self.lista = []
        self.algoritm = tk.StringVar(value="Bubble Sort")
        self.viteza = tk.IntVar(value=5)  # Viteza de sortare (1-10)
        self.numar_elemente = tk.IntVar(value=10)  # Numărul de elemente din listă
        self.pauza = False
        self.sortare_in_curs = False
        self.stop_event = threading.Event()
        self.thread = None

        # Leaga algoritmii de funcțiile lor
        self.algoritmi = {
            "Bubble Sort": self.bubble_sort,
            "Insertion Sort": self.insertion_sort,
            "Selection Sort": self.selection_sort
        }

        # Widgeturi UI
        self.creeaza_widgeturi()

    def creeaza_widgeturi(self):
        # Butoane
        frame_controale = tk.Frame(self.root, padx=10, pady=10)
        frame_controale.pack(fill=tk.X)

        # Selectarea algoritmului
        ttk.Label(frame_controale, text="Algoritm:").grid(row=0, column=0, padx=5)
        ttk.Combobox(frame_controale, textvariable=self.algoritm,
                     values=["Bubble Sort", "Insertion Sort", "Selection Sort"], state="readonly").grid(row=0, column=1,
                                                                                                        padx=5)

        # Setarea vitezei de sortare
        ttk.Label(frame_controale, text="Viteză:").grid(row=0, column=2, padx=5)
        ttk.Spinbox(frame_controale, from_=1, to=10, textvariable=self.viteza, width=5).grid(row=0, column=3, padx=5)

        # Setarea numărului de elemente din listă
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

        # Deseneaza grafic lista
        self.canvas = tk.Canvas(self.root, bg="white", height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def genereaza_date(self):
        # Generează o lista de numere intre 1 și 100
        self.lista = [random.randint(1, 100) for _ in range(self.numar_elemente.get())]
        self.deseneaza_date()  # Desenează lista pe canvas

    def deseneaza_date(self, highlight=None):
        # Șterge și deseneaza noile valori ale listei
        self.canvas.delete("all")
        highlight = highlight or []
        latime_bara = self.canvas.winfo_width() / len(self.lista)
        max_valoare = max(self.lista)

        # Desenează fiecare bară
        for i, valoare in enumerate(self.lista):
            x0 = i * latime_bara
            y0 = self.canvas.winfo_height() - (
                        valoare / max_valoare) * self.canvas.winfo_height()
            x1 = (i + 1) * latime_bara
            y1 = self.canvas.winfo_height()
            culoare = "lightblue" if i not in highlight else "pink"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=culoare, outline="")

    def ruleaza_sortarea(self):
        if self.lista and not self.sortare_in_curs:
            self.stop_event.clear()  # Resetează
            self.sortare_in_curs = True  # Marchează că sortarea este în curs
            self.thread = threading.Thread(
                target=self.algoritmi[self.algoritm.get()])
            self.thread.start()

    # Algoritmul de sortare Bubble Sort
    def bubble_sort(self):
        for i in range(len(self.lista) - 1):
            for j in range(len(self.lista) - i - 1):
                if self.lista[j] > self.lista[j + 1]:
                    self.lista[j], self.lista[j + 1] = self.lista[j + 1], self.lista[j]
                    self.actualizeaza_si_pauza([j, j + 1])
                if self.stop_event.is_set(): return

    # Algoritmul de sortare Insertion Sort
    def insertion_sort(self):
        for i in range(1, len(self.lista)):
            key = self.lista[i]
            j = i - 1
            while j >= 0 and self.lista[j] > key:
                self.lista[j + 1] = self.lista[j]
                j -= 1
                self.actualizeaza_si_pauza([j + 1, i])
            self.lista[j + 1] = key
            self.actualizeaza_si_pauza([j + 1])
            if self.stop_event.is_set(): return

    # Algoritmul de sortare Selection Sort
    def selection_sort(self):
        for i in range(len(self.lista)):
            min_idx = i
            for j in range(i + 1, len(self.lista)):
                if self.lista[j] < self.lista[min_idx]:
                    min_idx = j
                self.actualizeaza_si_pauza([i, min_idx, j])
            self.lista[i], self.lista[min_idx] = self.lista[min_idx], self.lista[i]
            self.actualizeaza_si_pauza([i, min_idx])
            if self.stop_event.is_set(): return

    def actualizeaza_si_pauza(self, highlight):
        if self.pauza:
            while self.pauza:
                time.sleep(0.1)
        self.deseneaza_date(highlight)
        self.root.update()
        time.sleep(1.0 / self.viteza.get())

    # Inversează starea pauzei
    def pauza_si_rezolva(self):
        self.pauza = not self.pauza

    # Oprește sortarea și resetează
    def reseteaza(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        self.lista = []
        self.canvas.delete("all")
        self.sortare_in_curs = False
        self.pauza = False


# Program Principal
if __name__ == "__main__":
    root = tk.Tk()  # Creează fereastra principală
    app = VizualizatorSortare(root)
    root.mainloop()
