import random
import csv

import methods


# 'lista_klientow' przechowuje wartosci bedace jednostkami czasu po ktorych dany 
# klient przyszedl do banku
lista_klientow = []

for i in range(70):
    czas_przyjscia = int(random.gauss(240, 200))  # średnia=240, odchylenie=80
    if 0 <= czas_przyjscia <= 479:
        lista_klientow.append(czas_przyjscia)

# lista zostaje posortowana w celu ustawienia godzin przyjscia do banku w sposob rosnacy
lista_klientow.sort()

# zmienna okreslajaca czas w ktorym kasjer jest wolny - czas oznacza 
# wartosc minutowa jaka uplynela od godziny 9:00 rownoznacznej wartosci 0
czas_dostępny_pracownika = 0

# lista 'kolejka' przechowywac bedzie indeksy klientow stojacych obecnie 
# w kolejce oraz czas po jakim przyszli do banku - (id, minuty)
# kazdy klient ma indeks odpowiadajacy pozycji w liscie 'lista_klientow'
kolejka = []

# --------------------------
# --- Nazwy kolumn w csv ---
dane_do_csv = [(
    "ID", 
    "Czas_przyjścia", 
    "Czas_rozpoczęcia_obsługi", 
    "Czas_zakończenia_obsługi", 
    "Czas_oczekiwania"
    )]
# --------------------------
# --------------------------

id_klienta = 1 # ID okreslajace kazdego klienta w koncowym pliku csv

klient_index = 0  # indeks klienta w liście - ustawiony na 0 oznacza pierwsza osobe z listy 'lista_klientow'


# ============================================================================================
# =========================== Glowna petla symulacji ========================================
# ============================================================================================

for minuta in range(480):  # 480 iteracji - kazda reprezentuje jedna minute - w sumie 8 godzin

    # 
    while klient_index < len(lista_klientow) and lista_klientow[klient_index] == minuta:
        kolejka.append((id_klienta, minuta))
        id_klienta += 1
        klient_index += 1

    # Jeśli pracownik wolny i ktoś czeka w kolejce – obsłuż
    if minuta >= czas_dostępny_pracownika and kolejka:
        klient_id, czas_przyjscia = kolejka.pop(0)
        czas_rozpoczecia = minuta
        # czas_obsługi = random.randint(5, 15)
        czas_obsługi = int(methods.rozklad_wykladniczy(1 / 6))  # średnia 6 min, ale dużo 1–2 min i pojedyncze 20+

        if czas_obsługi <=1:
            czas_obsługi = 1

        czas_zakonczenia = czas_rozpoczecia + czas_obsługi
        czas_oczekiwania = czas_rozpoczecia - czas_przyjscia

        dane_do_csv.append((str(klient_id), 
                            str(czas_przyjscia), 
                            str(czas_rozpoczecia), 
                            str(czas_zakonczenia), 
                            str(czas_oczekiwania)))

        czas_dostępny_pracownika = czas_zakonczenia

# =============================================================================================
# =============================================================================================


# =============================================================================================
# ======================== Zapisanie danych do plikow csv =====================================
# =============================================================================================

with open("symulacja_banku_godziny.csv", "w", newline="") as plik:
    writer = csv.writer(plik)
    writer.writerow(["ID", "Czas_przyjścia", "Rozpoczęcie_obsługi", "Zakończenie_obsługi", "Czas_oczekiwania (min)"])

    for wiersz in dane_do_csv[1:]:  # Pomijamy nagłówek
        klient_id = wiersz[0]
        przyjscie = methods.minuty_na_godzine(int(wiersz[1]))
        start = methods.minuty_na_godzine(int(wiersz[2]))
        koniec = methods.minuty_na_godzine(int(wiersz[3]))
        oczekiwanie = wiersz[4]

        writer.writerow([klient_id, przyjscie, start, koniec, oczekiwanie])



with open("symulacja_banku.csv", "w", newline="") as plik:
    writer = csv.writer(plik)
    writer.writerows(dane_do_csv)

# =============================================================================================
# =============================================================================================
print("Symulacja zakończona.")
