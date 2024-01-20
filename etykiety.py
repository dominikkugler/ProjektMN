import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import json

class AplikacjaEtykietowania:
    def __init__(self, root):
        self.root = root
        self.root.title("Narzędzie do Etykietowania")

        self.MAX_IMAGE_SIZE = (1400, 1000)

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)

        self.obrazy = []
        self.obecny_obraz_idx = 0
        self.obecny_obraz = None
        self.obecny_obrazTk = None
        self.prostokaty = []  # Lista prostokątów dla obecnego obrazu
        self.start_x = None
        self.start_y = None
        self.rysuje = False  # Flaga informująca, czy aktualnie rysujemy

        self.setup_gui()

    def setup_gui(self):
        self.licznik_zdjec_label = tk.Label(self.root, text="Zdjęcie: 0 z 0")
        self.licznik_zdjec_label.pack(side=tk.TOP, fill=tk.X)

        przycisk_otworz = tk.Button(self.root, text="Otwórz Zdjęcia", command=self.otworz_zdjecia, bg='lightblue', fg='black')
        przycisk_otworz.pack(side=tk.TOP, fill=tk.X)

        przycisk_znak = tk.Button(self.root, text="Znak", command=lambda: self.zapisz_etykietowanie(1), bg='lightgreen', fg='black')
        przycisk_znak.pack(side=tk.TOP, fill=tk.X)

        przycisk_brak_znaku = tk.Button(self.root, text="Brak Znaku", command=lambda: self.zapisz_etykietowanie(0), bg='lightcoral', fg='black')
        przycisk_brak_znaku.pack(side=tk.TOP, fill=tk.X)

        self.canvas.bind("<Button-1>", self.poczatek_rysowania)
        self.canvas.bind("<B1-Motion>", self.rysuj_prostokat)
        self.canvas.bind("<ButtonRelease-1>", self.koniec_rysowania)

    def otworz_zdjecia(self):
        sciezki_plikow = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if sciezki_plikow:
            self.obrazy = list(sciezki_plikow)
            self.obecny_obraz_idx = 0
            self.wczytaj_obraz()

    def wczytaj_obraz(self):
        if self.obecny_obraz_idx < len(self.obrazy):
            self.aktualizuj_licznik_zdjec()
            self.obecny_obraz = Image.open(self.obrazy[self.obecny_obraz_idx])
            self.obecny_obraz.thumbnail(self.MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
            self.obecny_obrazTk = ImageTk.PhotoImage(self.obecny_obraz)
            self.canvas.config(width=self.obecny_obrazTk.width(), height=self.obecny_obrazTk.height())
            self.canvas.create_image(0, 0, anchor="nw", image=self.obecny_obrazTk)

            # Usuń istniejące prostokąty, jeśli istnieją
            self.usun_prostokaty()
        else:
            messagebox.showinfo("Koniec", "Wszystkie zdjęcia zostały zaetykietowane.")

    def aktualizuj_licznik_zdjec(self):
        licznik_tekst = f"Zdjęcie: {self.obecny_obraz_idx + 1} z {len(self.obrazy)}"
        self.licznik_zdjec_label.config(text=licznik_tekst)

    def zapisz_etykietowanie(self, obecnosc_znaku):
        nazwa_pliku = os.path.basename(self.obrazy[self.obecny_obraz_idx])
        nazwa_pliku_bez_rozszerzenia = os.path.splitext(nazwa_pliku)[0]
        folder_etykiet = 'E:\Github repos\ProjektMetody\ProjektMN\Etykiety'
        if not os.path.exists(folder_etykiet):
            os.makedirs(folder_etykiet)
        sciezka_pliku = os.path.join(folder_etykiet, "etykiety.json")

        etykiety = []
        for prostokat in self.prostokaty:
            x1, y1, x2, y2 = self.canvas.coords(prostokat)
            etykieta = {"obecnosc_znaku": obecnosc_znaku, "x1": x1, "y1": y1, "x2": x2, "y2": y2}
            etykiety.append(etykieta)

        with open(sciezka_pliku, "a") as f:
            json.dump(etykiety, f)
            f.write("\n")

        print(f"Etykiety {etykiety} zapisane do {sciezka_pliku}")
        self.nastepne_zdjecie()

    def nastepne_zdjecie(self):
        self.obecny_obraz_idx += 1
        self.wczytaj_obraz()

    def poczatek_rysowania(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rysuje = True

    def rysuj_prostokat(self, event):
        if self.start_x is not None and self.start_y is not None and self.rysuje:
            current_x = self.canvas.canvasx(event.x)
            current_y = self.canvas.canvasy(event.y)

            # Usuń istniejące prostokąty dla obecnego obrazu
            self.usun_prostokaty()

            # Rysuj prostokąt aktualny
            prostokat = self.canvas.create_rectangle(
                self.start_x, self.start_y, current_x, current_y,
                outline="red", width=2, tags="prostokaty"
            )

            # Dodaj identyfikator prostokąta do listy prostokątów dla obecnego obrazu
            self.prostokaty.append(prostokat)

    def koniec_rysowania(self, event):
        self.rysuje = False

    def usun_prostokaty(self):
        # Usuń istniejące prostokąty dla obecnego obrazu
        for prostokat in self.prostokaty:
            self.canvas.delete(prostokat)
        self.prostokaty = []

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikacjaEtykietowania(root)
    root.mainloop()