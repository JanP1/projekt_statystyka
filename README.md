# Projekt Statystyka
## Opis projektu: Symulacja systemu kolejkowego w banku

Projekt przedstawia symulację działania systemu kolejkowego w banku z trzema stanowiskami obsługi klienta. Celem projektu jest odwzorowanie i analiza procesu obsługi klientów w ujęciu stochastycznym z możliwością dalszej analizy danych statystycznych.

---

## Zawartość projektu

- `main.py` – główny plik z kodem symulacji
- `methods.py` – funkcje pomocnicze, m.in. rozkład wykładniczy i konwersje czasu
- `symulacja_banku.csv` – dane surowe z symulacji (czasy w minutach)
- `symulacja_banku_godziny.csv` – dane z konwersją czasu na format HH:MM

---

## Opis działania symulacji

- Symulacja obejmuje **5 dni roboczych**, każdy dzień trwa 480 minut (od 9:00 do 17:00).
- Liczba klientów dziennie jest losowana w pobliżu wartości zadanej przez użytkownika.
- Każdy klient otrzymuje czas przyjścia wygenerowany na podstawie rozkładu normalnego.
- Czas obsługi klienta jest generowany z **rozkładu wykładniczego**, zgodnie z modelem systemów kolejkowych M/M/c.
- Dane zapisywane dla każdego klienta to m.in.:
  - unikalne ID (zawierające numer dnia),
  - czas przyjścia,
  - długość kolejki w momencie przyjścia,
  - czas rozpoczęcia i zakończenia obsługi,
  - czas oczekiwania,
  - numer dnia i numer stanowiska.

---

## Zakładane efekty kształcenia

- Możliwość przeprowadzania testów statystycznych na danych wyjściowych, np. testy ANOVA w zależności od stanowiska lub dnia.
- Możliwość zastosowania regresji wielorakiej do modelowania wpływu długości kolejki, dnia i stanowiska na czas oczekiwania.
- Symulacja stanowi przykład zastosowania **systemu kolejkowego z charakterystyką stochastyczną (M/M/c)** w praktyce.

---

## Planowane rozszerzenia

- Dodanie skryptu do przeprowadzenia analizy statystycznej i regresji.
- Generowanie wykresów (np. rozkład oczekiwania, analiza obciążenia stanowisk).
