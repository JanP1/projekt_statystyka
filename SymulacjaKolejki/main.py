import random
import csv
import math

import methods


l_klientow_dziennie = int(input("Podaj ilu okolo klientow przyjdzie do banku kazdego dnia: "))
szybkosc_pracownik1 = int(input("Podaj sredni czas obslugi 1. pracownika: "))
szybkosc_pracownik2 = int(input("Podaj sredni czas obslugi 2. pracownika: "))
szybkosc_pracownik3 = int(input("Podaj sredni czas obslugi 3. pracownika: "))

szybkosc_pracownik = [szybkosc_pracownik1, szybkosc_pracownik2, szybkosc_pracownik3]


# ilosc cyfr w liczbie klientow na dzien potrzebna do generowania ID
cyfry = math.floor(math.log10(l_klientow_dziennie)) + 1

# --------------------------
# --- Nazwy kolumn w csv ---
dane_do_csv = [(
    "ID", 
    "Czas_przyjscia", 
    "Dlugosc kolejki w momencie przyjscia",
    "Czas_rozpoczecia_obslugi", 
    "Czas_zakonczenia_obslugi", 
    "Czas_oczekiwania",
    "Dzien",
    "Stanowisko"
    )]
# --------------------------
# --------------------------

'''

Wizualizacja kolejki

            [1]      [2]      [3]
                      o        o
                    
                      o
                      o
                      o
                      o
                      o


'''

# ============================================================================================
# =========================== Glowna petla symulacji ========================================
# ============================================================================================


for dzien in range(1, 6): # 5 dni roboczych

# 'lista_klientow' przechowuje wartosci bedace jednostkami czasu po ktorych dany 
# klient przyszedl do banku - czas oznacza 
# wartosc minutowa jaka uplynela od godziny 9:00 rownoznacznej wartosci 0
    lista_klientow = []

# lista zostaje wypełniona, losowane zostaja minuty po ktorych klient przyjdzie do banku

    l_klientow_tego_dnia = methods.w_okolicach_wartosci(l_klientow_dziennie)
    print(dzien, 'dnia: ', l_klientow_tego_dnia, 'klientow')
    
    for i in range(l_klientow_tego_dnia):
        czas_przyjscia = int(random.gauss(240, 200))  # średnia=240, odchylenie=80
        if 0 <= czas_przyjscia <= 479:
            lista_klientow.append(czas_przyjscia)
        else:
            lista_klientow.append(random.randint(0, 480))

# lista zostaje posortowana w celu ustawienia godzin przyjscia do banku w sposob rosnacy
    lista_klientow.sort()

# zmienna okreslajaca czas w ktorym kasjer jest wolny - czas oznacza 
# wartosc minutowa jaka uplynela od godziny 9:00 rownoznacznej wartosci 0
    czas_dostępny_pracownika = [0, 0, 0]


# lista 'kolejka' przechowywac bedzie indeksy klientow stojacych obecnie 
# w kolejce oraz czas po jakim przyszli do banku - (id, minuty)
# kazdy klient ma indeks odpowiadajacy pozycji w liscie 'lista_klientow'
    kolejka = []


    id_klienta = 1 # ID okreslajace kazdego klienta w koncowym pliku csv

    klient_index = 0  # indeks klienta w liście - ustawiony na 0 oznacza pierwsza osobe z listy 'lista_klientow'

    for minuta in range(480):  # 480 iteracji - kazda reprezentuje jedna minute - w sumie 8 godzin



# Petla sprawdzajaca czy sa jeszcze jacys klienci oraz czy sa to klienci, ktorzy wedlug symulacji
# pojawia sie w obecnej chwili (mozliwe jest przybycie kilku o tej samej porze)
        while klient_index < len(lista_klientow) and lista_klientow[klient_index] == minuta:

            # Jezeli istnieje klient ktory mial przyjsc o tej porze, zostaje dodany do kolejki
            kolejka.append((id_klienta, minuta))

            # nastepnie zwiekszany jest indeks w celu sprawdzenia nastepnego klienta
            id_klienta += 1
            klient_index += 1

        # Jezeli nie ma juz wiecej klientow ktorzy mieli przyjsc o tej porze, program
        # sprawdza czy pracownik banku jest wolny - jesli tak, przechodzi do obslugi osoby,
        # ktora pierwsza czeka w kolejce (FIFO)


        for stanow in range(3):
            
            # czy jakis nowy klient zaczal byc obslugiwany w tej minucie
            if minuta >= czas_dostępny_pracownika[stanow] and kolejka:
                # przechowywane zostaja informacje o ID klienta oraz o czasie jego przybycia do banku
                klient_id, czas_przyjscia = kolejka.pop(0)

                # czas rozpoczecia obslugi zostaje przypisany jako obecna minuta
                czas_rozpoczecia = minuta

                # losowany zostaje czas potrzebny pracownikowi na obsluzenie klienta
                czas_obslugi = round(methods.rozklad_wykladniczy(1 / szybkosc_pracownik[stanow]))

                '''
                
                'czas_obslugi' wylosowany zostaje z rozkladu wykladniczego
                Odwrotnosc wartosci lambda wyrazenia 
                        
                        -math.log(u) / lambd

                (gdzie u to losowa liczba z rozkładu jednostajnego (równomiernego) na przedziale (0,1))
                oznacza srednia ilosc minut potrzebnych na obsluge
                '''

                # Zapewniony jest rowniez minimalny czas obslugi - 1 minuta
                if czas_obslugi <=1:
                    czas_obslugi = 1

                # obliczenie kiedy pracownik bedzie znow dostepny
                # oraz ile klient musial czekac w kolejce
                czas_zakonczenia = czas_rozpoczecia + czas_obslugi
                czas_oczekiwania = czas_rozpoczecia - czas_przyjscia

                dane_do_csv.append((str(klient_id + dzien*(10**cyfry)), 
                                    str(czas_przyjscia), 
                                    str(len(kolejka)),
                                    str(czas_rozpoczecia), 
                                    str(czas_zakonczenia), 
                                    str(czas_oczekiwania),
                                    str(dzien), 
                                    str(stanow + 1)
                                    ))

                czas_dostępny_pracownika[stanow] = czas_zakonczenia

# =============================================================================================
# =============================================================================================


# =============================================================================================
# ======================== Zapisanie danych do plikow csv =====================================
# =============================================================================================

with open("symulacja_banku_godziny.csv", "w", newline="") as plik:
    writer = csv.writer(plik)
    writer.writerow([
        "ID", 
        "Czas_przyjscia", 
        "Dlugosc kolejki w momencie przyjscia",
        "Czas_rozpoczecia_obslugi", 
        "Czas_zakonczenia_obslugi", 
        "Czas_oczekiwania",
        "Dzien",
        "Stanowisko"
    ])

    for wiersz in dane_do_csv[1:]:  # Pomijamy nagłówek
        klient_id = wiersz[0]
        przyjscie = methods.minuty_na_godzine(int(wiersz[1]))
        dlugosc_kolejki = wiersz[2]
        start = methods.minuty_na_godzine(int(wiersz[3]))
        koniec = methods.minuty_na_godzine(int(wiersz[4]))
        oczekiwanie = wiersz[5]
        dzien = wiersz[6]
        stanowisko = wiersz[7]

        writer.writerow([klient_id, przyjscie, dlugosc_kolejki, start, koniec, oczekiwanie, dzien, stanowisko])



with open("symulacja_banku.csv", "w", newline="") as plik:
    writer = csv.writer(plik)
    writer.writerows(dane_do_csv)

# =============================================================================================
# =============================================================================================
print("Symulacja zakończona.")
