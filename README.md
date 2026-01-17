Repo dla projektu 3.

## 1. O projekcie

Celem projektu jest analiza danych dotyczących godzinnych pomiarów stężenia pyłu zawieszonego PM2.5 w Polsce, pochodzących z archiwów GIOŚ. Obecnie porównywane są dane między miastami dla różnych lat - 2015, 2018, 2021 i 2024. 
Dane pochodzą z oficjalnych archiwów GIOŚ:

* <b>Dane pomiarowe PM2.5</b> – pliki Excel spakowane w archiwa ZIP,
* <b>Metadane stacji pomiarowych</b> – informacje o lokalizacji i zmianach kodów stacji.

Projekt ma strukturę modularną gdzie posczególne części odpowiadają za daną funkcjonalność.

## 2. Opis modułów i plików:

* ```main.ipynb``` <p>
  Główny interfejs projektu, jego zadaniem jest uruchamianie poszczególnych funkcjonalności oraz ich integracja. Zawiera on wyniki, w tym wszystkie wykresy oraz interpretację analiz.

* ```configs.py``` <p>
  Jest to plik konfiguracyjny w, którym zawarte są wszystkie stałe/linki używane potem w innych modułach. Możliwe jest zdefiniowanie w nim interesujących nas lat analizy (np. dla Zadania 2) czy też zmienienie danych stałych min. adresów URL, indentyfikatorow plików, interesujących nas lat analizy czy też normy WHO.

* ```read_process.py``` <p>
  Moduł ten odpowiedzialny jest za pobieranie danych pomiarowych oraz metadanych. Jego kolejną główną funkcjonalnością jest odpowiednia obróbka pobranych danych min. konwersję danych do formatu czasowego, ujednolicenie kodów stacyjnych, łączenie danych w jeden zbiór.

* ```calculations.py``` <p>
  Jest to głównie moduł obliczeniowy zawierający funkcję potrzebnę do uzyskania odpowiedniego formatu danych do np. wizualizacji. Większość metod agregacji, obliczania średnich itp. jest zawarta tutaj.

* ```visualizations.py``` <p>
  Zgodnie z nazwą moduł ten odpowiada za wizualizację posczególnych wykresów - głównie przy użyciu biblioteki matplotlib czy też seaborn.

* ```tests/``` <p>
  Katalog zawierający testy jednostkowe przygotowane z użyciem pytest, sprawdzające poprawność kluczowych funkcji (np. przetwarzania danych, agregacji).

## 3. Opis przetwarzania danych

### 1. Pobranie plików
Dane są pobierane bezpośrednio z archiwów GIOŚ w formie plików ZIP lub excel za pomocą funkcji download_gios_archive().

### 2. Czyszczenie danych
* automatyczne wykrywanie wiersza nagłówka
* usuwanie niepoprawnych dat
* konwersja indeksu dataframe na datetime
* korekta pomiarów z godziny 00:00

### 3. Ujednolicenie kodów stacji

Na podstawie metadanych stare kody stacji są mapowane na aktualne, a także odpowiednio dostosowane. 

## 4. Testy i wymagania

Wszystkie potrzebne biblioteki do uruchomienia programu znajdują się w pliku ```requirements.txt```. Można pobrać je prosto za pomocą komendy:
```bash
pip install -r requirements.txt
```

Testy....

```bash
pytest -q
```








