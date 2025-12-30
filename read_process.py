"""
Funkcje zajmujące się wczytywaniem i obróbką danych.
"""

import pandas as pd
import numpy as np
import requests, zipfile, io
from configs import GIOS_ARCHIVE_URL

def download_gios_archive(year, gios_id, filename) -> pd.DataFrame:
    # Pobranie archiwum ZIP do pamięci
    url = f"{GIOS_ARCHIVE_URL}{gios_id}"
    response = requests.get(url)
    response.raise_for_status()  # jeśli błąd HTTP, zatrzymaj
    
    # Otwórz zip w pamięci
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # znajdź właściwy plik z PM2.5
        if not filename:
            print(f"Błąd: nie znaleziono {filename}.")
        else:
            # wczytaj plik do pandas
            with z.open(filename) as f:
                try:
                    df = pd.read_excel(f, header=None)
                except Exception as e:
                    print(f"Błąd przy wczytywaniu {year}: {e}")
    return df

def download_metadata(meta_id: int) -> pd.DataFrame:
    url = f"{GIOS_ARCHIVE_URL}{meta_id}"
    response = requests.get(url)
    metadata = pd.read_excel(io.BytesIO(response.content))
    
    return metadata

def process_raw_df(dataframe: pd.DataFrame, year: int) -> pd.DataFrame:
    df = dataframe 
    if year in [2014,2015]: #ustlamy odpowiednie nazwy kolumn, usuwamy metadane o pomiarach, plik z 2014 ma inny format.
        df.columns = df.iloc[0]
        df = df.drop([0,1,2])
    else: 
        df.columns = df.iloc[1]
        df = df.drop([0,1,2,3,4,5])
        
    df['Measurment'] = pd.to_datetime(df.iloc[:,0])  # pierwsza kolumna -> datetime
    df = df.set_index('Measurment')
    df = df.drop(columns="Kod stacji")
    df = df.apply(pd.to_numeric, errors='coerce') # zmieniamy object -> float
    
    midn_mask = df.index.hour == 0 
    corrected_dates = df.index[midn_mask] - pd.Timedelta(seconds=1) #wszystkie wartości z północą przesuwamy o sekunde mniej

    df.index.values[midn_mask] = corrected_dates
    df = df.interpolate(method='time') #interpolujemy brakujące wartości

    return df

def process_metadata(metadata: pd.DataFrame) -> pd.DataFrame:
    old = 'Stary Kod stacji \n(o ile inny od aktualnego)'
    new = 'Kod stacji'
    #Niektóre wartości w metadanych to " " puste znaki, zamieniamy je na właściwe NaN
    met_old_station = metadata[old].astype(str).str.strip().replace({'nan': np.nan, '': np.nan})
    met_new_station = metadata[new].astype(str).str.strip().replace({'nan': np.nan, '': np.nan})
    metadata[old] = met_old_station
    metadata[new] = met_new_station
    #bierzemy pod uwage te wiersze gdzie zaszła zmiana kodów
    metadata = metadata.dropna(subset=[old, new])
    
    return metadata

def atomize_dict(mapper: dict[str, str]) -> dict[str, str]:
    dedup_station_map = {}
    for old_val, new_val in mapper.items():
        # Niektóre wartości rozdzielone "," np. ZpSzczecin002, ZpSzczPils02. Atomizujemy nasz dataframe.
        if old_val and ',' in old_val:
            old_codes = [code.strip() for code in str(old_val).split(',')]
            for code in old_codes:
                dedup_station_map[code] = new_val
        else:
            dedup_station_map[old_val] = new_val
            
    return dedup_station_map

def update_codes(df: pd.DataFrame, mapper: dict[str,str]) -> pd.DataFrame:
    # Używamy get, niektórych stacje, które nie zmieniały nazwy nie ma w naszym mapperze.
    df.columns = [mapper.get(col, col) for col in df.columns]
    
    return df

def merge_years(dfs: dict, metadata: pd.DataFrame) -> pd.DataFrame:
    merged = pd.concat(dfs.values(), join="inner")

    station_cities = dict(zip(metadata['Kod stacji'], metadata['Miejscowość']))

    merged.columns = pd.MultiIndex.from_tuples(
        [(station_cities.get(code, 'Unknown'), code) for code in merged.columns],
        names=['City', 'Station_Code']
    )

    return merged

