import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

DATA_FILE = "books.json"


class BookManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Catalog de Cărți")
        self.geometry("600x400")
        self.resizable(True, True)

        self.books = []
        self.load_data()

        self.create_widgets()
        self.populate_list()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Listbox cu scrollbar pentru listarea cărților
        self.listbox = tk.Listbox(main_frame, height=15)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-Button-1>", self.on_edit)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Frame pentru butoane CRUD
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        btn_add = ttk.Button(btn_frame, text="Adaugă", command=self.on_add)
        btn_add.pack(fill=tk.X, pady=5)

        btn_edit = ttk.Button(btn_frame, text="Editează", command=self.on_edit)
        btn_edit.pack(fill=tk.X, pady=5)

        btn_delete = ttk.Button(btn_frame, text="Șterge", command=self.on_delete)
        btn_delete.pack(fill=tk.X, pady=5)

        btn_refresh = ttk.Button(btn_frame, text="Reîncarcă", command=self.reload_data)
        btn_refresh.pack(fill=tk.X, pady=5)

    def populate_list(self):
        self.listbox.delete(0, tk.END)
        for idx, book in enumerate(self.books):
            display_text = f"{book['titlu']} - {book['autor']} ({book['an']})"
            self.listbox.insert(tk.END, display_text)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except Exception as e:
                messagebox.showerror("Eroare", f"Nu s-au putut încărca datele:\n{e}")
                self.books = []
        else:
            self.books = []

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.books, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Eroare", f"Nu s-au putut salva datele:\n{e}")

    def on_add(self):
        BookForm(self, "Adaugă carte")

    def on_edit(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenție", "Selectați o carte pentru editare.")
            return
        index = selection[0]
        BookForm(self, "Editează carte", index)

    def on_delete(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenție", "Selectați o carte pentru ștergere.")
            return
        index = selection[0]
        book = self.books[index]
        confirm = messagebox.askyesno("Confirmare ștergere",
                                      f"Sunteți sigur că doriți să ștergeți cartea:\n{book['titlu']}?")
        if confirm:
            del self.books[index]
            self.save_data()
            self.populate_list()

    def reload_data(self):
        self.load_data()
        self.populate_list()


class BookForm(tk.Toplevel):
    def __init__(self, parent, title, book_index=None):
        super().__init__(parent)
        self.parent = parent
        self.book_index = book_index
        self.title(title)
        self.resizable(False, False)
        self.grab_set()  # face fereastra modală

        self.create_widgets()
        if book_index is not None:
            self.load_book_data()

    def create_widgets(self):
        pad = 10
        lbl_width = 10

        frame = ttk.Frame(self, padding=pad)
        frame.pack(fill=tk.BOTH, expand=True)

        # Titlu
        ttk.Label(frame, text="Titlu:", width=lbl_width, anchor=tk.W).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_titlu = ttk.Entry(frame, width=40)
        self.entry_titlu.grid(row=0, column=1, pady=5)

        # Autor
        ttk.Label(frame, text="Autor:", width=lbl_width, anchor=tk.W).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_autor = ttk.Entry(frame, width=40)
        self.entry_autor.grid(row=1, column=1, pady=5)

        # An apariție
        ttk.Label(frame, text="An apariție:", width=lbl_width, anchor=tk.W).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_an = ttk.Entry(frame, width=40)
        self.entry_an.grid(row=2, column=1, pady=5)

        # Butoane Salvare / Anulare
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)

        btn_save = ttk.Button(btn_frame, text="Salvează", command=self.on_save)
        btn_save.pack(side=tk.LEFT, padx=5)

        btn_cancel = ttk.Button(btn_frame, text="Anulează", command=self.destroy)
        btn_cancel.pack(side=tk.LEFT, padx=5)

    def load_book_data(self):
        book = self.parent.books[self.book_index]
        self.entry_titlu.insert(0, book["titlu"])
        self.entry_autor.insert(0, book["autor"])
        self.entry_an.insert(0, str(book["an"]))

    def on_save(self):
        titlu = self.entry_titlu.get().strip()
        autor = self.entry_autor.get().strip()
        an_str = self.entry_an.get().strip()

        if not titlu or not autor or not an_str:
            messagebox.showerror("Eroare", "Toate câmpurile sunt obligatorii!")
            return

        if not an_str.isdigit() or not (1000 <= int(an_str) <= 2100):
            messagebox.showerror("Eroare", "Anul apariției trebuie să fie un număr valid între 1000 și 2100.")
            return

        an = int(an_str)

        book_data = {"titlu": titlu, "autor": autor, "an": an}

        if self.book_index is None:
            # Adaugă carte nouă
            self.parent.books.append(book_data)
        else:
            # Actualizează carte existentă
            self.parent.books[self.book_index] = book_data

        self.parent.save_data()
        self.parent.populate_list()
        self.destroy()


if __name__ == "__main__":
    app = BookManagerApp()
    app.mainloop()
