"""
Funkcje do grupowania, liczenia średnich itp.
"""

import pandas as pd
import numpy as np

def group_monthly_cities(final_df: pd.DataFrame) -> pd.DataFrame:

    monthly = final_df.groupby([final_df.index.year, final_df.index.month]).mean()
    monthly_cities = monthly.T.groupby(level='City').mean().T

    return monthly_cities

def create_long_format(plot_data: pd.DataFrame, YEARS: list[int]) -> pd.DataFrame:
    # Przekształcamy dane do formatu 'long'
    plot_data_long = plot_data.melt(
        id_vars=['City', 'Station_Code'],
        value_vars=YEARS, 
        var_name='Year',
        value_name='Exceeding_Days'
    )
    
    # Tworzymy etykiety dla osi X łącząc miasto i kod stacji
    plot_data_long['Station_Label'] = plot_data_long['City'] + '\n(' + plot_data_long['Station_Code'] + ')'

    return plot_data_long

def create_norm_exceeding_df(daily_means_df: pd.DataFrame, YEARS: list[int], WHO_NORM: int) -> pd.DataFrame:
    exceedances = daily_means_df > WHO_NORM
    exceeding_counts = exceedances.groupby(exceedances.index.year).sum()
    
    # Filtrujemy tylko lata z konfiguracji YEARS, aby uniknąć włączenia niepełnych lat (np. 2016)
    exceeding_counts = exceeding_counts[exceeding_counts.index.isin(YEARS)]
    display(exceeding_counts)
    
    # Transponujemy, aby uzyskać stacje w wierszach i lata w kolumnach
    exceeding_df = exceeding_counts.T
    exceeding_df = exceeding_df.reset_index()

    return exceeding_df

def group_cities_yearly_and_monthly(long_df: pd.DataFrame) -> pd.DataFrame:

    city_monthly_avg = long_df.groupby(
    [
        long_df.index.get_level_values('City'),
        long_df.index.get_level_values('Measurment').year,
        long_df.index.get_level_values('Measurment').month
    ]
    ).mean()

    city_monthly_avg.index.names = ['City', 'Year', 'Month']
    city_monthly_avg = city_monthly_avg.reset_index()

    return city_monthly_avg