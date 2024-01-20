import os

def zmien_nazwy_zdjec(folder_sciezka):
    if not os.path.exists(folder_sciezka):
        print("Podany folder nie istnieje.")
        return

    lista_plikow = [plik for plik in os.listdir(folder_sciezka) if plik.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not lista_plikow:
        print("Brak plików graficznych w folderze.")
        return

    for indeks, stary_plik in enumerate(lista_plikow, start=1):
        nowa_nazwa = f"zdjecie{indeks}{os.path.splitext(stary_plik)[1]}"
        stary_pelny_path = os.path.join(folder_sciezka, stary_plik)
        nowy_pelny_path = os.path.join(folder_sciezka, nowa_nazwa)

        try:
            os.rename(stary_pelny_path, nowy_pelny_path)
            print(f"Zmieniono nazwę: {stary_plik} -> {nowa_nazwa}")
        except Exception as e:
            print(f"Błąd podczas zmiany nazwy pliku {stary_plik}: {e}")

if __name__ == "__main__":
    folder_do_zmiany = input("Podaj ścieżkę do folderu, w którym chcesz zmienić nazwy zdjęć: ")
    zmien_nazwy_zdjec(folder_do_zmiany)