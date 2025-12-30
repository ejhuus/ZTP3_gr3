"""
Funkcje do wizualizacji.
"""

import matplotlib.pyplot as plt
import pandas as pd

def plot_city_trends(monthly_df: pd.DataFrame, years_to_plot: list[int], cities_to_plot: list[str]) -> None:
    trends_data = {}

    for year in years_to_plot:
        for city in cities_to_plot:
            if city in monthly_df.columns and year in monthly_df.index.get_level_values(0):
                
                data_series = monthly_df.loc[year, city]
                trends_data[(city, year)] = data_series
    # Rysowanie wykresu trendów
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for (city, year), data in trends_data.items():
        # Miesiące na osi X
        months = range(1, 13)
        ax.plot(months, data.values, marker='o', linestyle='--', label=f'{city} {year}')
    
    # Ustawienia wykresu
    ax.set_title('Średnie miesięczne stężenie PM2.5 w Warszawie i Katowicach (2014 vs 2024)')
    ax.set_xlabel('Miesiąc')
    ax.set_ylabel('Średnie stężenie PM2.5 (µg/m³)')
    ax.set_xticks(months)
    ax.legend(title='Miasto i Rok')
    ax.grid(True)
    
    plt.tight_layout()
    plt.show()